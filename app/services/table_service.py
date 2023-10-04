import base64
import io
import uuid

import qrcode
from PIL import Image
from sqlmodel import select
# from app.models.table_models import QRcodeData
# from app.services.db_service import db_service
# from app.models import Order, OrderState, Table

from models.table_models import QRcodeData
from services.db_service import db_service
from models import Order, OrderState, Table

async def generate_qrcode(table_id: int):
    uuid_code = str(uuid.uuid4())
    url = f'http://192.168.100.52:3000/{uuid_code}' #cambiar cuando tengamos variables de entorno

    qr = qrcode.QRCode(version=4, box_size=140, border=2)
    qr.add_data(url)
    qr.make()

    # Logo
    logofile = '../resources/logo-qr.png' # here goes the location of the chosen logo
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
    img.save(bytes)
    retval = bytes.getvalue()

    base64_image = base64.b64encode(retval).decode('utf-8')  # Encode the image in Base64

    return QRcodeData(table_id=table_id, uuid_code=uuid_code, qrcode=base64_image)

async def update_uuid(table_id: int, uuid_code: str):
    table_data: Table = db_service.get_object_by_id(Table, table_id)
    table_data.qr_id = uuid_code
    return db_service.update_object(Table, table_data)

async def get_current_orders(table_code: str):
    statement = select(Table).where(Table.qr_id == table_code)
    table: Table = db_service.get_with_filters(statement)[0]

    statement = select(Order).where(Order.table == table.id).where(Order.state != OrderState.closed).where(Order.state != OrderState.cancelled)
    return db_service.get_with_filters(statement)
    