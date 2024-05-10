from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
import os


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def save(self, *args, **kwargs):
        if self.pk:  # Проверяем, что продукт уже существует (имеет первичный ключ)
            old_product = Product.objects.get(pk=self.pk)
            # Если данные изменились, обновляем QR-код
            if self.name != old_product.name or self.description != old_product.description or self.price != old_product.price:
                # Создание строки с данными о продукте для QR-кода
                data = f"https://6efe-212-115-114-108.ngrok-free.app/product_info/?name={self.name}&description={self.description}&price={self.price}"

                # Создание QR-кода
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)

                # Создание изображения QR-кода
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer)
                self.qr_code.delete()  # Удаляем старый QR-код
                self.qr_code.save(f'qr_code_{self.pk}.png', File(buffer), save=False)

        else:  # Если продукт новый, создаем новый QR-код
            data = f"https://6efe-212-115-114-108.ngrok-free.app/product_info/?name={self.name}&description={self.description}&price={self.price}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer)
            self.qr_code.save(f'qr_code_{self.pk}.png', File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
