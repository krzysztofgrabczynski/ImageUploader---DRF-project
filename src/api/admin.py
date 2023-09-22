from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from api.models import ImageModel, URLExpirationModel, UserTierModel, TierModel


admin.site.register(ImageModel)
admin.site.register(URLExpirationModel)


class UserTierModelInline(admin.StackedInline):
    model = UserTierModel
    can_delete = False


class CustomUserModelAdmin(UserAdmin):
    inlines = [UserTierModelInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserModelAdmin)


class TierModelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "thumbnail_sizes",
        "get_origin_img",
        "renew_url_perm",
        "get_tier_users",
    ]

    @admin.display(description="USERS")
    def get_tier_users(self, obj):
        return obj.get_tier_users()


admin.site.register(TierModel, TierModelAdmin)
