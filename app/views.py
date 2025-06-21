from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from app.forms import RegisterForm, CourseRegisterForm
from django.urls import reverse_lazy
from app.models import Button, Issue, Category, Course, Registration
import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class IndexView(TemplateView):
    template_name = "index.html"


class Login(LoginView):
    template_name = "registration/login.html"


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def form_schema(request):
    buttons = Button.objects.all()
    items = [f for f in os.listdir(settings.MEDIA_ROOT)]
    files = []
    for item in items:
        files.append(
            {
                "name": item,
                "filetype": os.path.splitext(item)[1],
            }
        )
    context = {
        "buttons": buttons,
        "items": files,
    }
    return render(request, "partials/template.html", context)


@csrf_exempt
@require_POST
def save_form(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            existing = [
                f
                for f in os.listdir(settings.MEDIA_ROOT)
                if f.startswith("form_") and f.endswith(".json")
            ]
            nums = [int(f[5:-5]) for f in existing if f[5:-5].isdigit()]
            next_num = max(nums, default=0) + 1
            filename = f"form_{next_num}.json"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            with open(filepath, "w") as f:
                json.dump(data, f)

            return HttpResponse("Form saved successfully", status=200)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=400)
    return HttpResponse("Invalid request", status=400)


@csrf_exempt
@require_POST
def save_schema(request):
    if request.method == "POST":
        from django.http import HttpResponse

        try:
            existing = [
                f
                for f in os.listdir(settings.MEDIA_ROOT)
                if f.startswith("schema_") and f.endswith(".txt")
            ]
            nums = [int(f[7:-4]) for f in existing if f[7:-4].isdigit()]
            next_num = max(nums, default=0) + 1
            filename = f"schema_{next_num}.txt"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            schema_text = request.body.decode("utf-8")
            with open(filepath, "w") as f:
                f.write(schema_text)

            return HttpResponse("Schema saved successfully", status=200)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=400)
    return HttpResponse("Invalid request", status=400)


def list_issues(request):
    issues = Issue.objects.all()
    context = {
        "issues": issues,
    }
    return render(request, "partials/issue.html", context)


def create_issue(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        if title and description:
            Issue.objects.create(title=title, description=description)
            messages.success(request, "Issue created successfully")
            return redirect("list_issues")
        return HttpResponse("Invalid data", status=400)
    return HttpResponse("Method not allowed", status=405)


def update_issue(request, issue_id):
    if request.method == "POST":
        try:
            issue = Issue.objects.get(id=issue_id)
            issue.status = "closed"
            issue.save()
            messages.success(request, "Issue updated successfully")
            return redirect("list_issues")
        except Issue.DoesNotExist:
            return HttpResponse("Issue not found", status=404)
    return HttpResponse("Method not allowed", status=405)


def delete_issue(request, issue_id):
    if request.method == "POST":
        try:
            issue = Issue.objects.get(id=issue_id)
            issue.delete()
            messages.success(request, "Issue deleted successfully")
            return redirect("list_issues")
        except Issue.DoesNotExist:
            return HttpResponse("Issue not found", status=404)
    return HttpResponse("Method not allowed", status=405)


def get_categories(request):
    if request.GET.get("type") == "json" and request.user.is_authenticated:
        categories = Category.objects.all().order_by("order")
        return HttpResponse(
            json.dumps([{"id": cat.id, "name": cat.name} for cat in categories]),
            content_type="application/json",
        )
    categories = Category.objects.filter(publish=True).order_by("order")
    context = {
        "categories": categories,
    }

    return render(request, "partials/category.html", context)


def get_courses(request, category_id=None):
    if request.GET.get("type") == "json" and request.user.is_authenticated:
        courses = Course.objects.all().order_by("order")
        return HttpResponse(
            json.dumps(
                [
                    {
                        "id": course.id,
                        "title": course.title,
                        "description": course.description,
                        "hours": course.hours,
                        "number": course.number,
                        "price": course.price,
                    }
                    for course in courses
                ]
            ),
            content_type="application/json",
        )
    courses = (
        Course.objects.filter(category_id=category_id, publish=True).order_by("order")
        if category_id
        else Course.objects.all()
    )
    category = Category.objects.get(id=category_id) if category_id else None
    context = {
        "courses": courses,
        "category": category.name if category else None,
    }
    return render(request, "partials/course.html", context)


def get_course_details(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        context = {
            "course": course,
        }
        return render(request, "partials/course_detail.html", context)
    except Course.DoesNotExist:
        return HttpResponse("Course not found", status=404)


@login_required
def panel(request):
    return render(request, "partials/panel_oferta.html", {})


@login_required
def add_category(request):
    if request.method == "GET":
        categories = Category.objects.all().order_by("order")
        context = {
            "categories": categories,
        }
        return render(request, "partials/add_category.html", context)
    if request.method == "POST":
        name = request.POST.get("name")
        parent_category_id = request.POST.get("parent_category")
        order = request.POST.get("order")
        publish = request.POST.get("publish", "off") == "on"
        if Category.objects.filter(order=order).exists():
            messages.error(request, "Order must be unique.")
            return redirect("add_category")

        if not name or not order:
            messages.error(request, "Name and order are required.")
            return redirect("add_category")

        parent_category = (
            Category.objects.get(id=parent_category_id) if parent_category_id else None
        )

        Category.objects.create(
            name=name, parent_category=parent_category, order=order, publish=publish
        )
        messages.success(request, "Category created successfully")
        return redirect("add_category")

    return HttpResponse("Method not allowed", status=405)


@login_required
def add_course(request):
    if request.method == "GET":
        courses = Course.objects.all().order_by("order")
        context = {
            "courses": courses,
            "categories": Category.objects.all().order_by("order"),
        }
        return render(request, "partials/add_course.html", context)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        hours = request.POST.get("hours")
        number = request.POST.get("number")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        order = request.POST.get("order")
        if Course.objects.filter(order=order).exists():
            messages.error(request, "Order must be unique.")
            return redirect("add_course")

        if (
            not title
            or not description
            or not hours
            or not number
            or not price
            or not category_id
            or not order
        ):
            messages.error(request, "All fields are required.")
            return redirect("add_course")

        category = Category.objects.get(id=category_id)
        Course.objects.create(
            title=title,
            description=description,
            hours=hours,
            number=number,
            price=price,
            category=category,
            order=order,
            publish=request.POST.get("publish", "off") == "on",
        )
        messages.success(request, "Course created successfully")
        return redirect("panel_oferta")

    return HttpResponse("Method not allowed", status=405)


def register_course(request):
    context = {
        "form": CourseRegisterForm(),
    }
    if request.method == "GET":
        return render(request, "partials/register.html", context)
    if request.method == "POST":
        form = CourseRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect("course_register")
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    return render(request, "partials/register.html", context)


def issues_json(requst):
    issues = Issue.objects.all()
    issues_data = [
        {
            "id": issue.id,
            "title": issue.title,
            "description": issue.description,
            "created_at": issue.created_at.isoformat(),
        }
        for issue in issues
    ]
    return HttpResponse(json.dumps(issues_data), content_type="application/json")


def courses_registrations_json(request):
    registrations = Registration.objects.all()
    registrations_data = [
        {
            "id": reg.id,
            "course": reg.course.title,
            "name": reg.name,
            "surname": reg.surname,
            "phone": reg.phone,
            "email": reg.email,
            "status": reg.status,
            "date": reg.date.isoformat(),
        }
        for reg in registrations
    ]
    return HttpResponse(json.dumps(registrations_data), content_type="application/json")


def course_registration_json(request, registration_id):
    try:
        registration = Registration.objects.get(id=registration_id)
        registration_data = {
            "id": registration.id,
            "course": registration.course.title,
            "name": registration.name,
            "surname": registration.surname,
            "phone": registration.phone,
            "email": registration.email,
            "status": registration.status,
            "date": registration.date.isoformat(),
        }
        return HttpResponse(
            json.dumps(registration_data), content_type="application/json"
        )
    except Registration.DoesNotExist:
        return HttpResponse("Registration not found", status=404)


def list_forms(request):
    forms = [f for f in os.listdir(settings.MEDIA_ROOT)]
    forms_data = [
        {
            "name": form,
            "filetype": os.path.splitext(form)[1],
        }
        for form in forms
    ]
    return HttpResponse(json.dumps(forms_data), content_type="application/json")
