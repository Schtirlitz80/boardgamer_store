# Generated by Django 4.1.7 on 2023-03-19 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_productimage_image_alter_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_images', to='shop.product', to_field='slug'),
        ),
    ]
