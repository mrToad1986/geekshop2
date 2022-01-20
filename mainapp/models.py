from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория(ю)'
        verbose_name_plural = 'Категории'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products_img', blank=True, null=True)
    short_desc = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} <> {self.category.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'
