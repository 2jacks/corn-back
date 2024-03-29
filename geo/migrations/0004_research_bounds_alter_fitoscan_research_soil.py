# Generated by Django 4.0.3 on 2022-03-27 13:36

from django.db import migrations, models
import django.db.models.deletion
import utils.file_management


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0003_alter_indexes_research'),
    ]

    operations = [
        migrations.AddField(
            model_name='research',
            name='bounds',
            field=models.JSONField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fitoscan',
            name='research',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geo.research'),
        ),
        migrations.CreateModel(
            name='Soil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('savi', models.FileField(upload_to=utils.file_management.user_field_path)),
                ('field', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geo.field')),
            ],
        ),
    ]
