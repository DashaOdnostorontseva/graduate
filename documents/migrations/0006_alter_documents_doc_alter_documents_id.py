# Generated by Django 4.2.1 on 2023-06-27 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_remove_documents_doc_sing_documents_doc_sign_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='doc',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
        migrations.AlterField(
            model_name='documents',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
