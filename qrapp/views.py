from django.shortcuts import render
import qrcode

from .models import Product


def generate_qr(request):
    name = "Ручка"
    description = "Ручка для письма"
    price = "200"

    url = f" https://d173-213-230-80-68.ngrok-free.app/product_info/?name={name}&description={description}&price={price}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("media/product_qr_code.png")

    return render(request, 'qrapp/generate_qr.html', {'url': url})


# def product_info(request):
#     name = request.GET.get('name')
#     description = request.GET.get('description')
#     price = request.GET.get('price')
#
#     return render(request, 'qrapp/product_info.html', {
#         'name': name,
#         'description': description,
#         'price': price,
#     })

def product_info(request):
    return render(request, 'qrapp/product_info.html')


def generate_home(request):
    products = Product.objects.all()
    return render(request, 'qrapp/home.html', {'products': products})