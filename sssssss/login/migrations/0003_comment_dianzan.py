# Generated by Django 2.1.2 on 2018-10-15 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='dianzan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('number', models.CharField(max_length=128)),
            ],
        ),
    ]
