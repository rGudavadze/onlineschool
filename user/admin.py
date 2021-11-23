from django.contrib import admin
from .models import User, Profile, SellerProfile


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(SellerProfile)
