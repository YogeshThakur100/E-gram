import qrcode
import os
import json
from qrcode import constants
from PIL import Image

class QRCodeGeneration:
    @staticmethod
    def createQRcode(data: dict, save_path: str) -> str:
        qr = qrcode.QRCode(
            version=1,  # size of the QR code (1 to 40)
            error_correction=constants.ERROR_CORRECT_H,
            box_size=4,
            border=2,
        )
        qr.add_data(json.dumps(data, ensure_ascii=False))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # Convert to PIL Image if not already
        if not isinstance(img, Image.Image):
            img = img.get_image()
        img = img.resize((128, 128))
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            img.save(f)
        return save_path
        