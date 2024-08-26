from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import HttpRequest

from volt.models import InviteCode
from volt.models import Profile

# Since we have a custom User admin with the profile inline,
# we need to unregister the default User admin.
admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"
    fk_name = "user"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_select_related = ("profile",)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "graph_id", "created_at", "updated_at")
    search_fields = ("user__email",)


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'created_at', 'is_active', 'used_by', 'expires_at')
    list_filter = ('is_active', 'created_at', 'expires_at')
    search_fields = ('code', 'used_by__username')
    readonly_fields = ('code', 'created_at', 'updated_at', 'created_by', 'used_by')

    def save_model(self, request: HttpRequest, obj: InviteCode, form, change):
        if not obj.pk:  # This ensures that the `created_by` is set only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_selected.short_description = "Deactivate selected invite codes"  # type: ignore

    actions = [deactivate_selected]
