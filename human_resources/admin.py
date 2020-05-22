from django.contrib import admin

from .models import Employee, Comprobante, Nomina

admin.site.register(Comprobante)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nationality', 'active', 'hire_date', 'email', 'identification')
    list_filter = ('active', 'nationality', 'payment_method')
    search_fields = ('surname', 'middle_name', 'forename')


class NominaAdmin(admin.ModelAdmin):
    list_display = ('id', 'pay_period')


admin.site.register(Nomina, NominaAdmin)
admin.site.register(Employee, EmployeeAdmin)
