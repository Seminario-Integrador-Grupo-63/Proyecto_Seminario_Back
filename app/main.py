import io
from fastapi import FastAPI, Response
import qrcode
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/qrcode")
async def generate_qr_code():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    qr = qrcode.QRCode(version = 1, box_size = 8, border = 8)
    qr.add_data(url)
    qr.make()
    img = qr.make_image(fill_color = 'black', back_color = 'white')
    bytes = io.BytesIO()
    img.save(bytes)
    retval = bytes.getvalue()
    return Response(content = retval, media_type="image/png")