# Generated by Django 2.1.1 on 2019-10-04 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0004_auto_20190821_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='imagem',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
