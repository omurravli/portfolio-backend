from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import admin_api
from .views import ContentView

router = DefaultRouter()
router.register("admin/stats", admin_api.StatViewSet)
router.register("admin/skill-categories", admin_api.SkillCategoryViewSet)
router.register("admin/skills", admin_api.SkillViewSet)
router.register("admin/timeline", admin_api.TimelineViewSet)
router.register("admin/process", admin_api.ProcessViewSet)
router.register("admin/projects", admin_api.ProjectViewSet)

urlpatterns = [
    # public
    path("content/", ContentView.as_view(), name="content"),
    # admin auth
    path("admin/login/", obtain_auth_token, name="admin-login"),
    path("admin/me/", admin_api.MeView.as_view(), name="admin-me"),
    path("admin/profile/", admin_api.SiteProfileView.as_view(), name="admin-profile"),
    # admin CRUD
    path("", include(router.urls)),
]
