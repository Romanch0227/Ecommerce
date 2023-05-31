# Generated by Django 4.1.7 on 2023-05-03 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog_post',
            fields=[
                ('title', models.CharField(max_length=255)),
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('head0', models.CharField(default='', max_length=500)),
                ('contenthead0', models.CharField(default='', max_length=500)),
                ('head1', models.CharField(default='', max_length=500)),
                ('contenthead1', models.CharField(default='', max_length=500)),
                ('head2', models.CharField(default='', max_length=500)),
                ('contenthead2', models.CharField(default='', max_length=500)),
                ('image', models.ImageField(default='image', upload_to='shop/images')),
            ],
        ),
    ]
