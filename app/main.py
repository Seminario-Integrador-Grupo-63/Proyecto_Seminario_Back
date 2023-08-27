import io
from fastapi import FastAPI, Response
import qrcode
from fastapi.middleware.cors import CORSMiddleware
import base64

from models import create_db_and_tables

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/qrcode")
async def generate_qr_code():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    # url = 'http://192.168.100.52:3000'
    # url = "https://www.google.com/"
    qr = qrcode.QRCode(version = 1, box_size = 12, border = 1)
    qr.add_data(url)
    qr.make()
    img = qr.make_image(fill_color = 'black', back_color='white')

    bytes = io.BytesIO()
    img.save(bytes)
    retval = bytes.getvalue()

    base64_image = base64.b64encode(retval).decode('utf-8')  # Encode the image in Base64

    return base64_image

    # return Response(content = retval, media_type="image/png")