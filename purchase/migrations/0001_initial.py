# Generated by Django 4.2.3 on 2023-09-04 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gold_type', models.CharField(choices=[('แหวนทองคำ', 'แหวนทองคำ'), ('สร้อยข้อมือทองคำ', 'สร้อยข้อมือทองคำ'), ('สร้อยคอทองคำ', 'สร้อยคอทองคำ'), ('กำไลทองคำ', 'กำไลทองคำ'), ('จี้ทองคำ', 'จี้ทองคำ'), ('ต่างหูทองคำ', 'ต่างหูทองคำ'), ('แท่งทองคำ', 'แท่งทองคำ')], max_length=255)),
                ('quantity', models.IntegerField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_card', models.CharField(max_length=13)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('address', models.TextField(blank=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(upload_to='purchase/')),
                ('employee', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'รับซื้อทองคำ',
                'verbose_name_plural': 'ข้อมูลรับซื้อทองคำ',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.purchase')),
            ],
        ),
    ]