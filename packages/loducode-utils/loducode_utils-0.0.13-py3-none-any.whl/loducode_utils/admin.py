from django.contrib import admin

from loducode_utils.models import City, PaymentRecord


class AuditAdmin(admin.ModelAdmin):
    __readonly_audit_fields = (
        'created_at', 'modified_at', 'created_by', 'modified_by'
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(AuditAdmin, self).get_readonly_fields(request, obj)
        readonly_fields = readonly_fields + self.__readonly_audit_fields
        return readonly_fields

class AuditStackedInline(admin.StackedInline):
    __readonly_audit_fields = (
        'created_at', 'modified_at', 'created_by', 'modified_by'
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(AuditStackedInline, self).get_readonly_fields(request, obj)
        readonly_fields = readonly_fields + self.__readonly_audit_fields
        return readonly_fields

class AuditTabularInline(admin.TabularInline):
    __readonly_audit_fields = (
        'created_at', 'modified_at', 'created_by', 'modified_by'
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(AuditTabularInline, self).get_readonly_fields(request, obj)
        readonly_fields = readonly_fields + self.__readonly_audit_fields
        return readonly_fields

class ReadOnlyAdmin(AuditAdmin):
    pass

class ReadOnlyStackedInline(AuditStackedInline):
    pass

class ReadOnlyTabularInline(AuditTabularInline):
    pass


class CityAdmin(AuditAdmin):
    list_display = ("name","state")
    list_display_links = ("name","state")
    list_filter = ("state",)
    search_fields = ("name",)

admin.site.register(City, CityAdmin)