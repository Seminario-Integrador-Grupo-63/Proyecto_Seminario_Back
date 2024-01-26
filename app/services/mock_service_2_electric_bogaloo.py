
import base64
from datetime import timedelta
import random
import uuid
from models import *
from services.db_service import db_service
from resources.mock_data_2 import *

def encode_image(image_path: str):
     with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_string}"

def create_mocks_2():
    models_list = [User,OrderDetail, SideDishOptions, Dish, SideDish, Waiter, Order,Table, Category, TableSector, Restaurant]
    for model in models_list:
        db_service.delete_dable(model)

    
    restaurant_1 = Restaurant(name = "QResto", last_name = "Test")
    restaurant_1: Restaurant = db_service.create_object(restaurant_1)

    user_admin = User(user="admin", password="admin", email="qresto@gmail.com", role="admin", restaurant=restaurant_1.id)
    user_employee = User(user="Mozo", password="admin", email="qresto@gmail.com", role="employee", restaurant=restaurant_1.id)
    
    db_service.create_object(user_admin)
    db_service.create_object(user_employee)

    auxiliar_list = option_aux

    for side_dish in SideDish_resource:
        sd = SideDish(name=side_dish["name"], restaurant=restaurant_1.id)
        sd: SideDish = db_service.create_object(sd)
        for dish in side_dish["dishes"]:
            option_dict = {
                "id": sd.id,
                "extra": dish["extra"]
            }
            auxiliar_list[dish["dish"]].append(option_dict)

    dish_list = []
    for categorie in category_source:
        img = encode_image(categorie["image"])
        cat = Category(name=categorie["name"], image=img, restaurant=restaurant_1.id)
        cat = db_service.create_object(cat)

        for dish in categorie["dishes"]:
            img = encode_image(dish["image"])
            ds: Dish = Dish(name=dish["name"], description=dish["description"], image=img, preparationTime=dish["preparation_time"], price=dish["price"], category=cat.id, restaurant=restaurant_1.id)
            ds: Dish = db_service.create_object(ds)
            dish_list.append(ds)

            options = auxiliar_list.get(ds.name)

            if options:
                for option in options:
                    sdo = SideDishOptions(dish=ds.id, sideDish=option["id"], extraPrice=option["extra"])
                    db_service.create_object(sdo)
    
    ts_1 = TableSector(name="Planta Baja", restaurant=restaurant_1.id)
    ts_1: TableSector = db_service.create_object(ts_1)
    
    ts_2 = TableSector(name="Primer piso", restaurant=restaurant_1.id)
    ts_2: TableSector = db_service.create_object(ts_2)

    ts_3 = TableSector(name="Patio", restaurant=restaurant_1.id)
    ts_3: TableSector = db_service.create_object(ts_3)

    ts_list: list[TableSector] = [ts_1, ts_2, ts_3]

    """table_lists ={
        ts_1.id: [],
        ts_2.id: [],
        ts_3.id: []
    } """

    for sector in ts_list:
        table_list = []
        for i in range(0,16):
            table = Table(restaurant=restaurant_1.id, sector=sector.id,number=i+1, tableCode=str(uuid.uuid4()))
            table: Table = db_service.create_object(table)
            table_list.append(table)
        
        #Creo ordenes viejas
        for i in range(0,50):
            table = random.choice(table_list)
            state =random.choice([OrderState.closed, OrderState.cancelled])
            days = random.randint(0, 5)
            hours = random.randint(5, 10)
            minutes = random.randint(0,60)
            time = datetime.now() - timedelta(days=days, hours=hours, minutes=minutes)
            order = Order(table=table.id, createdAt=time, state=state, restaurant=restaurant_1.id)
            order: Order = db_service.create_object(order) 

            counter = 0.0
            for i in range(0,random.randint(2,5)):
                dish: Dish = random.choice(dish_list)
                options = auxiliar_list.get(ds.name)
                if options:
                    option = random.choice(options)
                else:
                    option = {"id": None, "extra": 0.0} 
                
                ammount = random.randint(1,3)
                sub_total =(dish.price+option["extra"]) * ammount
                name = random.choice(names)
                order_detail = OrderDetail(order=order.id, dish=dish.id, sideDish=option["id"],amount=ammount, subTotal=sub_total,customerName=name)
                counter+= order_detail.sub_total
                db_service.create_object(order_detail)
            
            order.total = counter
            db_service.update_object(Order, order)


        for i in range(0,6):
            table = random.choice(table_list)
            state = random.choice([OrderState.preparation, OrderState.waiting, OrderState.delivered])
            order = Order(table=table.id, createdAt=datetime.now(), state=state, restaurant=restaurant_1.id)
            order: Order = db_service.create_object(order)

            counter = 0.0
            for i in range(0,random.randint(2,5)):
                dish: Dish = random.choice(dish_list)
                options = auxiliar_list.get(ds.name)
                if options:
                    option = random.choice(options)
                else:
                    option = {"id": None, "extra": 0.0} 
                
                ammount = random.randint(1,3)
                sub_total =(dish.price+option["extra"]) * ammount
                name = random.choice(names)
                order_detail = OrderDetail(order=order.id, dish=dish.id, sideDish=option["id"],amount=ammount, subTotal=sub_total,customerName=name)
                counter+= order_detail.sub_total
                db_service.create_object(order_detail)
            
            order.total = counter
            db_service.update_object(Order, order)
            if state == OrderState.waiting:
                table.state = TableState.waiting
                db_service.update_object(Table, table)
            else:
                table.state = TableState.occupied
                db_service.update_object(Table, table)
            table_list.remove(table)
        
        #creo unas esperando el pago para que se vea en el mapa
        for i in range(0,random.randint(1,2)):
            table = random.choice(table_list)
            order = Order(table=table.id, createdAt=datetime.now(), state=OrderState.delivered, restaurant=restaurant_1.id)
            order: Order = db_service.create_object(order)

            counter = 0.0
            for i in range(0,random.randint(2,5)):
                dish: Dish = random.choice(dish_list)
                options = auxiliar_list.get(ds.name)
                if options:
                    option = random.choice(options)
                else:
                    option = {"id": None, "extra": 0.0} 
                
                ammount = random.randint(1,3)
                sub_total =(dish.price+option["extra"]) * ammount
                name = random.choice(names)
                order_detail = OrderDetail(order=order.id, dish=dish.id, sideDish=option["id"],amount=ammount, subTotal=sub_total,customerName=name)
                counter+= order_detail.sub_total
                db_service.create_object(order_detail)
            
            order.total = counter
            db_service.update_object(Order, order)
            table.state = TableState.payment_ready
            db_service.update_object(Table, table)
            table_list.remove(table)
    
    sector = random.choice(ts_list)
    table_qr_code = Table(restaurant = restaurant_1.id, qr_id = "a", sector=sector.id, number=55555)
    db_service.create_object(table_qr_code)
    return {"restaurant_id" : restaurant_1.id}
    



