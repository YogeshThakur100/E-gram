import qrcode
import os

class QRCodeGeneration:
    @staticmethod
    def createQRcode(data : dict):
        qr = qrcode.QRCode(
            version=1,  # size of the QR code (1 to 40)
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
            )
        
        qr.add_data(data)
        qr.make(fit=True)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__) , '..'))
        static_dir = os.path.join(base_dir , 'static')
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        img.save(os.path.join(static_dir , 'qrcode.png'))
        print("QR Code saved as 'qrcode.png'")
        