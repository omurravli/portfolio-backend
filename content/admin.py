from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Project,
    ProcessStage,
    SiteProfile,
    Skill,
    SkillCategory,
    Stat,
    TimelineEntry,
)


@admin.register(SiteProfile)
class SiteProfileAdmin(ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("name", "role", "location", "university")}),
        ("Links", {"fields": ("email", "github", "linkedin", "cv_url")}),
        (
            "Hero copy",
            {"fields": ("hero_badge", "hero_heading_lead", "hero_heading_accent", "hero_subtitle")},
        ),
    )

    def has_add_permission(self, request):
        # singleton — edit the one row, never add another
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Stat)
class StatAdmin(ModelAdmin):
    list_display = ("label", "value", "suffix", "order")
    list_editable = ("value", "suffix", "order")


class SkillInline(TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(ModelAdmin):
    list_display = ("label", "color", "order")
    list_editable = ("color", "order")
    inlines = [SkillInline]


@admin.register(TimelineEntry)
class TimelineEntryAdmin(ModelAdmin):
    list_display = ("title", "context", "tag", "order")
    list_editable = ("order",)


@admin.register(ProcessStage)
class ProcessStageAdmin(ModelAdmin):
    list_display = ("title", "blurb", "order")
    list_editable = ("order",)


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ("title", "system", "status", "is_active", "featured", "order")
    list_editable = ("is_active", "featured", "order")
    list_filter = ("is_active", "featured")
