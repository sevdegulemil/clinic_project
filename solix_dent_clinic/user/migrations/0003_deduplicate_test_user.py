from django.db import migrations

def deduplicate_test_user(apps, schema_editor):
    """
    Finds all users with the email 'test@test.com', keeps the most recently created one,
    and deletes any others.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    users_to_check = User.objects.filter(email='test@test.com').order_by('-pk')
    
    if users_to_check.count() > 1:
        # Get the latest user (highest pk)
        latest_user = users_to_check.first()
        # Delete all other users with the same email
        User.objects.filter(email='test@test.com').exclude(pk=latest_user.pk).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_create_demo_user'),
    ]

    operations = [
        migrations.RunPython(deduplicate_test_user, migrations.RunPython.noop),
    ]