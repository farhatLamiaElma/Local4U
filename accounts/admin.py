from django.contrib import admin
from .models import CustomUser, Farmer, Customer, Admin


# Customize the Farmer admin to display CustomUser fields
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'get_email', 'get_address', 'get_contact_number', 'user_type')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_address(self, obj):
        return obj.user.address
    get_address.short_description = 'Address'

    def get_contact_number(self, obj):
        return obj.user.contact_number
    get_contact_number.short_description = 'Contact Number'

    def user_type(self, obj):
        return obj.user.user_type
    user_type.short_description = 'User Type'

# Register the models
admin.site.register(CustomUser)
admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Customer)
admin.site.register(Admin)


