# Generated by Django 3.1.6 on 2021-03-18 02:57

import apps.marketplace.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='marketplace.category', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Text')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('duration', models.PositiveSmallIntegerField(choices=[(1, '1 day'), (3, '3 days'), (7, '1 week'), (14, '2 weeks'), (30, '30 days')], default=7, help_text='Duration of trading.', verbose_name='Duration')),
                ('started_at', models.DateTimeField(auto_now_add=True, help_text='Date of creation of the lot and the start of trading.', verbose_name='Started at')),
                ('finished_at', models.DateTimeField(null=True, verbose_name='Finished at')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_private', models.BooleanField(default=False, help_text='If true, the lot will not be displayed in the lot feed.', verbose_name='Is private')),
                ('start_price', models.DecimalField(decimal_places=2, help_text='Bidding will start at this price.', max_digits=11, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Start price')),
                ('blitz_price', models.DecimalField(decimal_places=2, help_text='The lot can be redeemed at this price.', max_digits=11, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Blitz price')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', tinymce.models.HTMLField(verbose_name='Description')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lots', to='marketplace.category', verbose_name='Category')),
                ('commentators', models.ManyToManyField(related_name='commented_lots', through='marketplace.Comment', to=settings.AUTH_USER_MODEL, verbose_name='Commentators')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lots', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Lot',
                'verbose_name_plural': 'Lots',
                'ordering': ('-started_at',),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.marketplace.models.upload_lot_image_to, verbose_name='Image')),
                ('number', models.PositiveSmallIntegerField(db_index=True, default=0, help_text='Needed for ordering images.', verbose_name='Number')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='marketplace.lot', verbose_name='Lot')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'ordering': ('number',),
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='marketplace.lot', verbose_name='Lot'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='marketplace.comment', verbose_name='Parent'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Price')),
                ('is_top', models.BooleanField(default=True, verbose_name='Top')),
                ('lot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bids', to='marketplace.lot', verbose_name='Lot')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bids', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Bid',
                'verbose_name_plural': 'Bids',
                'ordering': ('-price',),
            },
        ),
    ]
