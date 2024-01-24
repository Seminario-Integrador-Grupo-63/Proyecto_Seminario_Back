import base64
from datetime import datetime, timedelta
import io
import os
import uuid
from fastapi import HTTPException

import qrcode
from PIL import Image
from sqlmodel import select
from models.order_models import CustomerList, CustomerOrderDetailData, FullOrderDTO, OrderDetailData, SideDishWithPrice

from models.table_models import QRcodeData, TableGridList
from services.db_service import db_service
from models import Dish, Order, OrderDetail, OrderState, SideDish, SideDishOptions, Table, TableSector, TableState
from services.order_service import get_full_order
from services.redis_service import redis_service


async def get_table_by_code(table_code: str):
    try:
        statement = select(Table).where(Table.qr_id == table_code)
        return db_service.get_with_filters(statement)[0]
    except Exception as e:
        message = f"No se pudo encontrar la mesa con codigo {table_code} error {e}"
        raise Exception(message)
    
async def change_table_state(table_code:str, current_state: TableState, new_state: TableState):
    table: Table = await get_table_by_code(table_code=table_code)

    if table.state == current_state:
        table.state = new_state
        return db_service.update_object(model=Table, body=table)
    

async def generate_qrcode(table_id: int):
    uuid_code = str(uuid.uuid4())
    
    # url = f'https://654d8f47be3cf11149bbf4bd--genuine-bavarois-cc292a.netlify.app/' + f'?table_code={uuid_code}' #cambiar cuando tengamos variables de entorno
    url = f'http:192.168.0.111:3001' + f'?table_code={uuid_code}'
    
    qr = qrcode.QRCode(version=4, box_size=140, border=2)
    qr.add_data(url)
    qr.make()

    # Logo
    logofile = '/code/resources/logo-qr.png' # here goes the location of the chosen logo
    """
    IMPORTANTE CAMBIAR EL LOGO POR VARIABLE DE ENTORNO
    """
    logo = Image.open(logofile)
    width = 1300
    widthpercentage = (width / float(logo.size[0]))
    height = int((float(logo.size[1]) * float(widthpercentage)))
    logo = logo.resize((width, height))

    fill = 'black' # Color of the QR itself
    back = 'white' # Color of the background
    img = qr.make_image(fill_color = fill, back_color=back).convert('RGB')

    # Middle position for the logo and fixing them together
    pos = ((img.size[0] - logo.size[0]) // 2,
           (img.size[1] - logo.size[1]) // 2)
    img.paste(logo, pos)

    bytes = io.BytesIO()
    img.save(bytes, format="PNG")
    retval = bytes.getvalue()

    base64_image = base64.b64encode(retval).decode('utf-8')  # Encode the image in Base64

    return QRcodeData(table_id=table_id, uuid_code=uuid_code, qrcode=base64_image)

async def update_uuid(table_id: int, uuid_code: str):
    table_data: Table = db_service.get_object_by_id(Table, table_id)
    table_data.qr_id = uuid_code
    return db_service.update_object(Table, table_data)

async def group_details(order_details:list[OrderDetail]):
    """
    returns
    {
    "customer_name":[order_detail]
    }
    """
    details_dict: dict[list[OrderDetail]] = {}
    for detail in order_details:

            if details_dict.get(detail.customer_name):
                details_dict[detail.customer_name].append(detail)
            else: 
                details_dict[detail.customer_name] = [detail]
    return details_dict

async def get_detail_data_list_and_price(details_dict:dict[list[OrderDetail]]):
    customer_order_data_list = []
    total_price = 0.0
    for key, customer_details in details_dict.items():
        customer_total = 0.0
        detail_data_list = []
        for detail in customer_details:
            dish: Dish = db_service.get_object_by_id(Dish, detail.dish)
            side_dish: SideDish = db_service.get_object_by_id(SideDish, detail.side_dish) if detail.side_dish else None
            if side_dish:
                statement = select(SideDishOptions).where(SideDishOptions.dish==dish.id)
                side_dish_options: list[SideDishOptions] =db_service.get_with_filters(statement)
                side_dish_2 = SideDishWithPrice(**side_dish.dict())
                if side_dish_options:
                    for option in side_dish_options:
                        if option.side_dish == side_dish.id:
                            side_dish_2.price = option.extra_price
            else:
                side_dish_2 = None
            order_detail_data = OrderDetailData(amount=detail.amount,
                                                dish=dish,
                                                side_dish= side_dish_2,
                                                sub_total=detail.sub_total,
                                                observation=detail.observation
                                                )
            total_price += detail.sub_total
            customer_total += detail.sub_total
            detail_data_list.append(order_detail_data)
        
        customer_order_data = CustomerOrderDetailData(customer=key, order_detail=detail_data_list, customer_total = customer_total)
        customer_order_data_list.append(customer_order_data)
    return total_price, customer_order_data_list

async def get_completed_orders(table: Table):
    dto_list: list[FullOrderDTO] = []
    statement = select(Order).where(Order.table == table.id).where(Order.state != OrderState.closed).where(Order.state != OrderState.cancelled)
    completed_orders: list[Order] = db_service.get_with_filters(statement)
    for order in completed_orders:

        statement = select(OrderDetail).where(OrderDetail.order == order.id)
        order_details: list[OrderDetail] = db_service.get_with_filters(statement)

        details_dict = await group_details(order_details)
        
        total_price, customer_order_data_list = await get_detail_data_list_and_price(details_dict)

        order_dto = FullOrderDTO(id=order.id,
                                    date_created=order.created_at.strftime("%d/%m/%Y"),
                                    time_created = order.created_at.strftime("%H:%M:%S"),
                                    total_customers = len(details_dict),
                                    confirmed_customers = len(details_dict),
                                    order_details = customer_order_data_list,
                                    total=total_price,
                                    state=order.state
                                )
        dto_list.append(order_dto)
    return dto_list

async def get_customer_list(total_customer: list, confirmed_customers: list):
    customer_list = []
    for customer in total_customer:
        data = CustomerList(customer=str(customer),
                            confirmed = True if customer in confirmed_customers else False)
        customer_list.append(data)
    return customer_list

async def get_cache_orders(table:Table):
    details_list = redis_service.get_data(table.qr_id)
    if not details_list:
        return None
    details_dict = await group_details(details_list)
    total_price, customer_order_data_list = await get_detail_data_list_and_price(details_dict)
    total_customers = redis_service.get_data(f"{table.qr_id}_customer")
    confirmed_customers = redis_service.get_data(f"{table.qr_id}_confirmed")
    confirmed_list = confirmed_customers if confirmed_customers else []
    customer_list: CustomerList = await get_customer_list(total_customers, confirmed_list)
    order_dto = FullOrderDTO(id=None,
                                date_created=(datetime.now() + timedelta(hours=-3)).strftime("%d/%m/%Y"),
                                time_created = (datetime.now() + timedelta(hours=-3)).strftime("%H:%M:%S"),
                                total_customers = len(total_customers),
                                confirmed_customers = len(confirmed_customers) if confirmed_customers else 0,
                                order_details = customer_order_data_list,
                                total=total_price,
                                state=OrderState.processing,
                                customerList=customer_list
                            )
    return order_dto

async def get_current_orders(table_code: str) -> list[FullOrderDTO]:
    table: Table = await get_table_by_code(table_code)
    dto_list = await get_completed_orders(table)

    current_order = await get_cache_orders(table)
    if current_order:
        dto_list.append(current_order)
    return dto_list

async def generate_billing(table_code: str) -> list[CustomerOrderDetailData]:
    table: Table = await get_table_by_code(table_code)
    statement = select(Order).where(Order.table == table.id).where(Order.state != OrderState.closed).where(Order.state != OrderState.cancelled).where(Order.state != OrderState.processing)
    orders: list[Order] = db_service.get_with_filters(statement)
    order_details_list = []
    customer_data_list = []
    for order in orders:

        statement = select(OrderDetail).where(OrderDetail.order == order.id)
        order_details: list[OrderDetail] = db_service.get_with_filters(statement)
        order_details_list.extend(order_details)

    detail_dict = await group_details(order_details_list)
        
    total_price, customer_order_data_list = await get_detail_data_list_and_price(detail_dict)
        
    customer_data_list.append(customer_order_data_list)
    
    await change_table_state(table_code, TableState.occupied, TableState.payment_ready)
    return customer_data_list[0]
    
        

async def init_table(table_code: str, customer_name: str):
    customers_sitted, saved = redis_service.save_set(f"{table_code}_sitted", customer_name)

    if not saved:
        raise HTTPException(status_code=400, detail="Ese nombre pertenece a otro miembro de la mesa")
    else:
        await change_table_state(table_code, TableState.free, TableState.occupied)
    
async def get_tables_grid(restaurant_id: int) -> list[TableGridList]:
    statement = select(Table).where(Table.restaurant == restaurant_id, Table.is_active==True)
    tables = db_service.get_with_filters(statement)

    sector_table_dict = {}
    for table in tables:
        if table.sector not in sector_table_dict:
            sector_table_dict[table.sector] = []
        sector_table_dict[table.sector].append(table)
    
    table_grid_list = [TableGridList(sector=sector, tables=tables) for sector, tables in sector_table_dict.items()]

    for sector in table_grid_list:
        sector_data: TableSector = db_service.get_object_by_id(TableSector, sector.sector)
        sector.sector = sector_data
    
    return table_grid_list

async def close_table(table_code: str):
    table: Table = await change_table_state(table_code, TableState.payment_ready , TableState.free)
    statement = select(Order).where(Order.table == table.id).where(Order.state != OrderState.closed).where(Order.state != OrderState.cancelled).where(Order.state != OrderState.processing)
    orders: list[Order] = db_service.get_with_filters(statement)
    for order in orders:
        order.state = OrderState.closed
        db_service.update_object(Order, order)
    redis_service.delete_data(f"{table_code}_sitted")
