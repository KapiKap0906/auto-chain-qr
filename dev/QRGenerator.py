import qrcode

features = qrcode.QRCode(version=1, box_size=40, border=3)

features.add_data('S1005')
features.make(fit=True)
generate_image = features.make_image(fill_colour = "black", back_colour = "white")
generate_image.save('QR Codes/image5.png')