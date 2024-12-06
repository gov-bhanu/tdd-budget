
from django.contrib import admin
from .models import DataRow

class DataRowAdmin(admin.ModelAdmin):
    list_display = (
        'unique_search',
        # 'department_code',
        'department_name',
        'head_name',
        'scheme_name',
        'soe_name',
        'sanctioned_budget',
        'revised_estimate_display',  # Use a custom method for displaying revised_estimate
        'last_change_date',
        'in_divisible',
        'divisible',
        'kinnaur',
        'lahaul',
        'spiti',
        'pangi',
        'bharmaur',
        'last_change_date',
    )
    search_fields = ('head_name', 'soe_name')  # Remove unique_search from search_fields
    list_filter = ('head_name',)

    # Custom method to display revised_estimate
    def revised_estimate_display(self, obj):
        # Ensure that revised_estimate is calculated correctly by using the saved value
        return obj.revised_estimate
    revised_estimate_display.admin_order_field = 'revised_estimate'  # Allow sorting by revised_estimate
    revised_estimate_display.short_description = 'Revised Estimate'

admin.site.register(DataRow, DataRowAdmin)