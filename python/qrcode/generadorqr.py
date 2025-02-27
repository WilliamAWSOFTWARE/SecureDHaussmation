import qrcode

# Datos que quieres codificar en el QR (puede ser texto o JSON)
data = '{"id": "FMWHNL311", "qr": 1}'

# Crear el objeto QR
qr = qrcode.QRCode(
    version=1,  # tamaño del QR
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Añadir los datos al QR
qr.add_data(data)
qr.make(fit=True)

# Crear la imagen del QR
img = qr.make_image(fill='black', back_color='white')

# Guardar la imagen en un archivo
img.save("codigo_qr.png")

# Mostrar el QR generado
img.show()
