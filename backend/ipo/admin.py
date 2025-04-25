from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter
from .models import IPOListing, IPOApplication

class IPOListingResource(resources.ModelResource):
    class Meta:
        model = IPOListing
        fields = ('company_name', 'symbol', 'issue_price', 'lot_size', 'total_issue_size', 
                 'subscription_start', 'subscription_end', 'status')
        export_order = fields

@admin.register(IPOListing)
class IPOListingAdmin(ImportExportModelAdmin):
    resource_class = IPOListingResource
    list_display = ('company_name', 'symbol', 'issue_price', 'lot_size', 'status', 
                   'subscription_start', 'subscription_end', 'get_total_applications')
    list_filter = (
        'status',
        ('subscription_start', DateRangeFilter),
        ('subscription_end', DateRangeFilter),
    )
    search_fields = ('company_name', 'symbol')
    date_hierarchy = 'subscription_start'
    ordering = ('-subscription_start',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('company_name', 'symbol', 'issue_price', 'lot_size', 'total_issue_size')
        }),
        ('Subscription Details', {
            'fields': ('subscription_start', 'subscription_end', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_total_applications(self, obj):
        return obj.applications.count()
    get_total_applications.short_description = 'Total Applications'

    actions = ['mark_as_upcoming', 'mark_as_open', 'mark_as_closed']

    def mark_as_upcoming(self, request, queryset):
        queryset.update(status='upcoming')
    mark_as_upcoming.short_description = "Mark selected IPOs as upcoming"

    def mark_as_open(self, request, queryset):
        queryset.update(status='open')
    mark_as_open.short_description = "Mark selected IPOs as open"

    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
    mark_as_closed.short_description = "Mark selected IPOs as closed"

class IPOApplicationResource(resources.ModelResource):
    class Meta:
        model = IPOApplication
        fields = ('user', 'ipo', 'lots_applied', 'status', 'application_date')
        export_order = fields

@admin.register(IPOApplication)
class IPOApplicationAdmin(ImportExportModelAdmin):
    resource_class = IPOApplicationResource
    list_display = ('user', 'ipo', 'lots_applied', 'status', 'application_date', 'get_status_badge')
    list_filter = (
        'status',
        ('application_date', DateRangeFilter),
        ('ipo', DropdownFilter),
    )
    search_fields = ('user__username', 'ipo__company_name', 'ipo__symbol')
    date_hierarchy = 'application_date'
    ordering = ('-application_date',)
    readonly_fields = ('application_date', 'updated_at')
    fieldsets = (
        ('Application Details', {
            'fields': ('user', 'ipo', 'lots_applied', 'status')
        }),
        ('Timestamps', {
            'fields': ('application_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_status_badge(self, obj):
        status_colors = {
            'pending': 'warning',
            'approved': 'success',
            'rejected': 'danger'
        }
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            status_colors.get(obj.status, 'secondary'),
            obj.get_status_display()
        )
    get_status_badge.short_description = 'Status'
    get_status_badge.admin_order_field = 'status'

    actions = ['approve_applications', 'reject_applications']

    def approve_applications(self, request, queryset):
        queryset.update(status='approved')
    approve_applications.short_description = "Approve selected applications"

    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')
    reject_applications.short_description = "Reject selected applications" 