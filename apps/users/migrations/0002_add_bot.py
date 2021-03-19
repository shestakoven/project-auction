from django.db import models, migrations


def add_bot(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.create(
        username='PyBot',
        email='bot@localhost',
        is_staff=True,
    )


def delete_bot(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.get(
        username='PyBot'
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_bot, reverse_code=delete_bot),
    ]
