from django.contrib import admin

# Register your models here.

from .models import Slide,SlideVersion


class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

admin.site.register(Slide, SlideAdmin)
admin.site.register(SlideVersion)