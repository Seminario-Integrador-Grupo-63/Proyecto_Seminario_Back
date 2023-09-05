import base64
import io
import uuid

import qrcode
from models.table_models import QRcodeData

from services.db_service import db_service
from models import Table    

async def generate_qrcode(table_id: int):
    uuid_code = str(uuid.uuid4())
    url = f'http://192.168.100.52:3000/{uuid_code}' #cambiar cuando tengamos variables de entorno

    qr = qrcode.QRCode(version = 1, box_size = 12, border = 1)
    qr.add_data(url)
    qr.make()
    img = qr.make_image(fill_color = 'black', back_color='white')

    bytes = io.BytesIO()
    img.save(bytes)
    retval = bytes.getvalue()

    base64_image = base64.b64encode(retval).decode('utf-8')  # Encode the image in Base64

    return QRcodeData(table_id=table_id, uuid_code=uuid_code, qrcode=base64_image)

async def update_uuid(table_id: int, uuid_code: str):
    table_data: Table = db_service.get_object_by_id(Table, table_id)
    table_data.qr_id = uuid_code
    return db_service.update_object(Table, table_data)
    