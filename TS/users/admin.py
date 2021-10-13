from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (ContactUs, User, DeviceId, LoginLogoutFail,
                     OtherRequests, ResetRequests)


# Register your models here.
class UserAdmin(ImportExportModelAdmin):
	model = User
	list_display = ['id', 'username', 'created', 'updated', 'email', 'first_name', 'surname', 'phone']
admin.site.register(User, UserAdmin)


class ResetRequestsAdmin(ImportExportModelAdmin):
	model = ResetRequests
	list_display = ['id', 'user', 'token', 'created_at', 'consumed_at', 'use_case']
admin.site.register(ResetRequests, ResetRequestsAdmin)


class OtherRequestsAdmin(ImportExportModelAdmin):
	model = OtherRequests
	list_display = ['user', 'request_type', 'details', 'created_at']
admin.site.register(OtherRequests, OtherRequestsAdmin)


class DeviceIdAdmin(ImportExportModelAdmin):
	model = DeviceId
	list_display = ['user', 'created_at', 'device_type', 'active', 'device_id', 'deactivate_date']
admin.site.register(DeviceId, DeviceIdAdmin)


class ContactUsAdmin(ImportExportModelAdmin):
	model = ContactUs
	list_display = ['id', 'user', 'device_type','created_at', 'subject', 'message']
admin.site.register(ContactUs, ContactUsAdmin)


class LoginLogoutFailAdmin(ImportExportModelAdmin):
	model = LoginLogoutFail
	list_display = ['user', 'login', 'login_time', 'logout', 'logout_time', 'failed_login', 'failed_login_time']
admin.site.register(LoginLogoutFail, LoginLogoutFailAdmin)