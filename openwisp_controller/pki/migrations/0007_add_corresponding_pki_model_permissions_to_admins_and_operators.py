from django.db import migrations 
from django.contrib.auth.models import Permission 


def assignPerm(apps, schema_editor): 
    Group= apps.get_model('openwisp_users', 'Group')
    admin = Group.objects.get(name='Administrator')
    operator = Group.objects.get(name='Operator')
    operators_read_only_admins_manage = ['ca', 'cert',]
    manage_operations = ['add', 'change', 'delete']

    for modelClass in operators_read_only_admins_manage:
        try:
            permission=Permission.objects.get(codename="view_{}".format(modelClass))
            operator.permissions.add(permission.pk )
        except Permission.DoesNotExist:
            pass   
        
        for operation in manage_operations: 
            admin.permissions.add(Permission.objects.get(codename="{}_{}".format(operation,modelClass)).pk, )


class Migration(migrations.Migration):
    dependencies=[
        ('openwisp_users', '0004_default_groups'),
        ('pki', '0006_add_x509_passphrase_field'),
    ]
    operations=[
    
        migrations.RunPython(assignPerm, reverse_code = migrations.RunPython.noop),

    ]