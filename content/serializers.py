from rest_framework import serializers

from .models import (
    Project,
    ProcessStage,
    SiteProfile,
    SkillCategory,
    Stat,
    TimelineEntry,
)


class SiteProfileSerializer(serializers.ModelSerializer):
    hero = serializers.SerializerMethodField()

    class Meta:
        model = SiteProfile
        fields = [
            "name",
            "role",
            "location",
            "university",
            "email",
            "github",
            "linkedin",
            "cv_url",
            "hero",
        ]

    def get_hero(self, obj):
        return {
            "badge": obj.hero_badge,
            "headingLead": obj.hero_heading_lead,
            "headingAccent": obj.hero_heading_accent,
            "subtitle": obj.hero_subtitle,
        }


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ["value", "suffix", "label"]


class SkillCategorySerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = SkillCategory
        fields = ["id", "label", "color", "skills"]

    def get_skills(self, obj):
        return [s.name for s in obj.skills.all()]


class TimelineEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEntry
        fields = ["title", "context", "description", "tag"]


class ProcessStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStage
        fields = ["id", "title", "blurb"]


class ProjectSerializer(serializers.ModelSerializer):
    stack = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "title", "system", "status", "description", "stack", "accent", "url", "featured"]

    def get_stack(self, obj):
        return [s.strip() for s in obj.stack.split(",") if s.strip()]
