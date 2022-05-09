# Generated by Django 4.0.3 on 2022-03-27 07:46

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import utils.file_management


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Culture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'cultures',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('area', models.FloatField(blank=True, null=True)),
                ('culture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.culture')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fields',
            },
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('rgb', models.FileField(upload_to=utils.file_management.user_research_path)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.field')),
            ],
            options={
                'db_table': 'researches',
            },
        ),
        migrations.CreateModel(
            name='Indexes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ndvi', models.FileField(upload_to=utils.file_management.user_indexes_path)),
                ('ndwi', models.FileField(upload_to=utils.file_management.user_indexes_path)),
                ('research', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.field')),
            ],
        ),
        migrations.CreateModel(
            name='FitoScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('n', models.FloatField(blank=True, null=True)),
                ('p', models.FloatField(blank=True, null=True)),
                ('k', models.FloatField(blank=True, null=True)),
                ('s', models.FloatField(blank=True, null=True)),
                ('ca', models.FloatField(blank=True, null=True)),
                ('mg', models.FloatField(blank=True, null=True)),
                ('b', models.FloatField(blank=True, null=True)),
                ('cu', models.FloatField(blank=True, null=True)),
                ('zn', models.FloatField(blank=True, null=True)),
                ('mn', models.FloatField(blank=True, null=True)),
                ('fe', models.FloatField(blank=True, null=True)),
                ('mo', models.FloatField(blank=True, null=True)),
                ('co', models.FloatField(blank=True, null=True)),
                ('j', models.FloatField(blank=True, null=True)),
                ('research', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.research')),
            ],
            options={
                'db_table': 'fitoscans',
            },
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=32)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AOI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('area', models.FloatField()),
                ('min_index', models.FloatField()),
                ('max_index', models.FloatField()),
                ('mean_index', models.FloatField()),
                ('research', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.research')),
            ],
            options={
                'db_table': 'areas_of_interest',
            },
        ),
    ]