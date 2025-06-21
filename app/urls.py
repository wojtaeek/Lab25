from django.urls import path, re_path
from app import views
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("index/", views.IndexView.as_view(), name="index"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    re_path(r"^$", lambda request: redirect("/index/", permanent=True)),
]


app_urls = [
    path("form_schema/", views.form_schema, name="form_schema"),
    path("save_form/", views.save_form, name="save_form"),
    path("save_schema/", views.save_schema, name="save_schema"),
    path("issues/", views.list_issues, name="list_issues"),
    path("issues/create/", views.create_issue, name="create_issue"),
    path("issues/<int:issue_id>/update/", views.update_issue, name="update_issue"),
    path("issues/<int:issue_id>/delete/", views.delete_issue, name="delete_issue"),
    path("categories/", views.get_categories, name="list_categories"),
    path("courses/", views.get_courses, name="list_courses"),
    path("courses/<int:category_id>/", views.get_courses, name="list_courses"),
    path(
        "courses/detail/<int:course_id>/",
        views.get_course_details,
        name="course_detail",
    ),
    path("panel/", views.panel, name="panel"),
    path("add_category/", views.add_category, name="add_category"),
    path("add_course/", views.add_course, name="add_course"),
    path("course_register/", views.register_course, name="course_register"),
    path("issues_json/", views.issues_json, name="issues_json"),
    path(
        "courses_json/",
        views.courses_registrations_json,
        name="courses_registrations_json",
    ),
    path(
        "courses_json/<int:registration_id>",
        views.course_registration_json,
        name="get_registration",
    ),
    path("list_forms", views.list_forms, name="list_forms"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += app_urls
