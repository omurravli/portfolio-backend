"""Authenticated write API that powers the custom admin panel (/admin on the site)."""

from rest_framework import serializers, viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Project,
    ProcessStage,
    SiteProfile,
    Skill,
    SkillCategory,
    Stat,
    TimelineEntry,
)


# --- serializers (flat, all editable fields) ----------------------------------

class SiteProfileWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteProfile
        fields = [
            "name", "role", "location", "university",
            "email", "github", "linkedin", "cv_url",
            "hero_badge", "hero_heading_lead", "hero_heading_accent", "hero_subtitle",
        ]


class StatWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ["id", "value", "suffix", "label", "order"]


class SkillWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "category", "name", "order"]


class SkillCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = ["id", "label", "color", "order"]


class TimelineWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEntry
        fields = ["id", "title", "context", "description", "tag", "order"]


class ProcessWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStage
        fields = ["id", "title", "blurb", "order"]


class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "system", "status", "description",
            "stack", "accent", "url", "featured", "is_active", "order",
        ]


# --- viewsets (all require auth) ----------------------------------------------

class _AuthedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class StatViewSet(_AuthedViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatWriteSerializer


class SkillCategoryViewSet(_AuthedViewSet):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategoryWriteSerializer


class SkillViewSet(_AuthedViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillWriteSerializer


class TimelineViewSet(_AuthedViewSet):
    queryset = TimelineEntry.objects.all()
    serializer_class = TimelineWriteSerializer


class ProcessViewSet(_AuthedViewSet):
    queryset = ProcessStage.objects.all()
    serializer_class = ProcessWriteSerializer


class ProjectViewSet(_AuthedViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectWriteSerializer


class SiteProfileView(RetrieveUpdateAPIView):
    """Singleton profile: GET the current values, PATCH to update."""

    permission_classes = [IsAuthenticated]
    serializer_class = SiteProfileWriteSerializer

    def get_object(self):
        return SiteProfile.load()


class MeView(APIView):
    """Lets the admin frontend verify a token and greet the user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"username": request.user.get_username()})
