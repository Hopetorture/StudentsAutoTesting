# Generated by Django 2.1.5 on 2019-03-04 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_reception', '0005_auto_20190304_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='correct_answer',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='stdin',
            field=models.TextField(default=''),
        ),
    ]
