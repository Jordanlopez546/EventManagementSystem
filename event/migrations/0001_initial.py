# Generated by Django 4.2.1 on 2023-06-30 17:26

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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('email', models.CharField(max_length=10000000)),
                ('bio', models.TextField(blank=True)),
                ('address', models.CharField(max_length=10000000)),
                ('profileimg', models.ImageField(default='blank-profile-picture.png', upload_to='user_profile_photos')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
