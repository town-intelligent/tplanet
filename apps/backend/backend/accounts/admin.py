from django.contrib import admin
from .models import Profile, SocialAccount

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "obj_user")

admin.site.register(Profile, ProfileAdmin)

class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "obj_users")

admin.site.register(SocialAccount, SocialAccountAdmin)
