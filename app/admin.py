from django.contrib import admin
from .models import Category, Course, Registration, Button


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "publish", "order", "parent_category")
    list_filter = ("publish",)
    search_fields = ("name",)
    ordering = ("order",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "publish", "order", "hours", "number", "price")
    list_filter = ("publish",)
    search_fields = ("title",)
    ordering = ("order",)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "course", "status", "date")
    list_filter = ("status",)
    search_fields = ("name", "surname", "email")
    ordering = ("-date",)


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
