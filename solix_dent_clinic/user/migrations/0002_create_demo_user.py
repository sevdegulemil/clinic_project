from django.db import migrations

def create_demo_user(apps, schema_editor):
    """Creates the 'test' user with a predefined password."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if not User.objects.filter(username='test').exists():
        User.objects.create_user(
            username='test',
            email='test@test.com',
            password='1234'
        )

def remove_demo_user(apps, schema_editor):
    """Removes the 'test' user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user_to_delete = User.objects.filter(username='test').first()
    if user_to_delete:
        user_to_delete.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_demo_user, remove_demo_user),
    ]