from django.db import models
from django.urls import reverse
import qrcode
from io import BytesIO
from django.core.files import File


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)  # Сначала сохраняем объект, чтобы у него был установлен pk

        data = f"https://051e-212-115-114-108.ngrok-free.app/product_info/{self.pk}"
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

    def get_absolute_url(self):
        return reverse('product_info', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name