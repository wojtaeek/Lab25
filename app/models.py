from django.db import models


class Category(models.Model):
    # id domyślnie zostaje dodane
    publish = models.BooleanField(default=False)
    order = models.PositiveIntegerField(
        unique=True,
    )
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name="parent",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="courses"
    )
    publish = models.BooleanField(default=False)
    order = models.PositiveIntegerField(unique=True)
    hours = models.IntegerField()
    number = models.IntegerField()
    price = models.FloatField()
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Registration(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="registrations"
    )
    rodo = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        default="active",
    )
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone = models.CharField(max_length=9)
    email = models.EmailField()

    def __str__(self):
        return f"Registration {self.name} {self.surname} for {self.course.title}"


class Button(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Issue(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[("open", "Open"), ("closed", "Closed")],
        default="open",
    )

    def __str__(self):
        return self.title
