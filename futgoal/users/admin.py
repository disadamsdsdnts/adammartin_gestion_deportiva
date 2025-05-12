# """User models admin."""

# # Django
# from django.contrib import admin

# # Models
# from futgoal.users.models import User, ActionLogUser, CallToLead

# # Forms
# from futgoal.users.forms.user_form import UserAdmin

# from import_export.admin import ImportExportModelAdmin
# from import_export import resources, widgets, fields
# from import_export.fields import Field
# from rangefilter.filters import (
#     DateRangeFilterBuilder,
#     NumericRangeFilterBuilder,
#     DateRangeQuickSelectListFilterBuilder,
# )
# from import_export.admin import ExportMixin

# class UserResource(resources.ModelResource):
#     team = Field(
#         attribute="team",
#         column_name="Equipo",
#     )

#     crm_magiclink = Field(
#         attribute="crm_magiclink",
#         column_name="CRM Magic Link",
#     )

#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'team',
#             'crm_magiclink',
#         )
#         export_order = (
#             'username',
#             'team',
#             'crm_magiclink',
#         )

#     def dehydrate_crm_magiclink(self, user):
#         return user.magic_login_link

#     def dehydrate_team(self, user):
#         from django.contrib.auth.models import Group

#         sale_teams =  Group.objects.exclude(name__startswith='Closers').exclude(name__startswith='Lí').exclude(name__startswith='So').order_by('name')
#         for group in sale_teams:
#             if user.groups.filter(name=group.name).exists():
#                 return group.name



# @admin.register(User)
# class CustomUserAdmin(ExportMixin, admin.ModelAdmin):
#     list_display = (
#         "email",
#         "first_name",
#         "last_name",
#         "sale_team",
#         "is_staff",
#         "is_active",
#         "base_salary",
#     )
#     resource_class = UserResource
#     def get_export_queryset(self, request):
#         queryset = super().get_export_queryset(request)
#         return queryset.filter(is_active=True)

#     list_filter = (
#         'groups',
#         'is_staff',
#         'is_active',
#         'sale_team',
#     )

#     search_fields = ('email', 'first_name', 'last_name')



# # admin.site.register(User, UserAdmin)


# @admin.register(ActionLogUser)
# class ActionLogUserAdmin(admin.ModelAdmin):
#     model = ActionLogUser
#     list_display = ("created", "user", "action_description",)
#     readonly_fields = ("created",)



# @admin.register(CallToLead)
# class CallToLeadAdmin(admin.ModelAdmin):
#     model = CallToLead
#     list_display = (
#         "created",
#         "call_id",
#         "user",
#         "call_created",
#         "user_email",
#         "destiny",
#         "call_duration",
#         "schedule"
#     )
#     list_filter = (
#         ("call_created", DateRangeFilterBuilder()),
#         "user",
#         "user_email",
#     )
#     search_fields = ("user_email", 'destiny', )
#     readonly_fields = ("created",)
#     readonly_fields = ('schedule', )
