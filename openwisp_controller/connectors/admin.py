from django.contrib import admin
from openwisp_utils.admin import MultitenantOrgFilter, TimeReadonlyAdminMixin

from ..admin import MultitenantAdminMixin
from ..config.admin import DeviceAdmin as BaseDeviceAdmin, ConfigInline
from ..config.models import Device
from .models import Connector, DeviceConnector, DeviceIp


class ConnectorAdmin(MultitenantAdminMixin, TimeReadonlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'organization', 'connector', 'created', 'modified')
    list_filter = [('organization', MultitenantOrgFilter),
                   'connector']
    list_select_related = ('organization',)


class DeviceIpInline(admin.TabularInline):
    model = DeviceIp
    extra = 0

    def get_queryset(self, request):
        qs = super(DeviceIpInline, self).get_queryset(request)
        return qs.order_by('priority')


class DeviceConnectorInline(admin.StackedInline):
    model = DeviceConnector
    extra = 0


class DeviceAdmin(BaseDeviceAdmin):
    inlines = [DeviceIpInline, DeviceConnectorInline, ConfigInline]

    def save_model(self, request, obj, form, change):
        obj.save()
        qs = obj.deviceconnector_set.filter(enabled=True)
        if qs.count() > 0:
            c = qs.first().connector_instance
            c.push()


admin.site.register(Connector, ConnectorAdmin)
admin.site.unregister(Device)
admin.site.register(Device, DeviceAdmin)
