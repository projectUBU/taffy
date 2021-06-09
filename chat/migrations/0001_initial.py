# Generated by Django 2.2.7 on 2021-06-08 18:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ข้อความ:Message',
                'ordering': ('timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Handler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewe_value', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_handler', to=settings.AUTH_USER_MODEL)),
                ('rejected_m', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rejecter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ตัวจัดการ:Handler',
                'unique_together': {('member', 'rejected_m')},
            },
        ),
    ]
