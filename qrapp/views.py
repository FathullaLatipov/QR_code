from django.shortcuts import render
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
import os

from .models import Product


def generate_qr(request):
    product = Product.objects.last()  # Получаем последний созданный товар

    url = request.build_absolute_uri(product.get_absolute_url())  # Строим абсолютный URL страницы с информацией о товаре

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    product.qr_code.save(f'qr_code_{product.pk}.png', File(buffer), save=False)

    return render(request, 'qrapp/generate_qr.html', {'url': url})


def product_info(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'qrapp/product_info.html', {'product': product})


def generate_home(request):
    products = Product.objects.all()
    return render(request, 'qrapp/home.html', {'products': products})