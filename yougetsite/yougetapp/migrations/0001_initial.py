# Generated by Django 4.1.7 on 2023-03-25 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_name', models.CharField(max_length=3)),
                ('mime_type', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='FileData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('file_name', models.CharField(max_length=100)),
                ('img_url', models.CharField(max_length=200, null=True)),
                ('uploader', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SessionKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=130)),
            ],
        ),
        migrations.CreateModel(
            name='VideoQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('format_id', models.CharField(max_length=3)),
                ('resolution', models.CharField(max_length=4, null=True)),
                ('codec', models.CharField(max_length=50, null=True)),
                ('ext', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yougetapp.exttype')),
            ],
        ),
        migrations.CreateModel(
            name='DlData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('file_deleted', models.BooleanField(default=False)),
                ('downloaded_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yougetapp.filedata')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yougetapp.sessionkey')),
            ],
        ),
        migrations.CreateModel(
            name='AudioQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_quality', models.CharField(max_length=4)),
                ('ext', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yougetapp.exttype')),
            ],
        ),
    ]
