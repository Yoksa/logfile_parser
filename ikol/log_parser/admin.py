from django.contrib import admin

from .models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('ip', 'log_date', 'http_method', 'uri_request', 'response_code', 'response_len')
    search_fields = ('ip',)
    list_filter = ("log_date", 'http_method', 'response_code')


admin.site.register(Log, LogAdmin)
