from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Project,
    ProcessStage,
    SiteProfile,
    SkillCategory,
    Stat,
    TimelineEntry,
)
from .serializers import (
    ProcessStageSerializer,
    ProjectSerializer,
    SiteProfileSerializer,
    SkillCategorySerializer,
    StatSerializer,
    TimelineEntrySerializer,
)


class ContentView(APIView):
    """Single public endpoint returning all editable site content in one payload.

    The Next.js frontend fetches this and falls back to its bundled data.ts if
    the request fails, so the site keeps working even if the backend is down.
    """

    def get(self, request):
        profile = SiteProfile.load()
        skills = SkillCategory.objects.prefetch_related("skills").all()
        projects = Project.objects.filter(is_active=True)

        return Response(
            {
                "profile": SiteProfileSerializer(profile).data,
                "stats": StatSerializer(Stat.objects.all(), many=True).data,
                "skillCategories": SkillCategorySerializer(skills, many=True).data,
                "timeline": TimelineEntrySerializer(TimelineEntry.objects.all(), many=True).data,
                "processStages": ProcessStageSerializer(ProcessStage.objects.all(), many=True).data,
                # empty list => frontend uses live GitHub repos instead
                "projects": ProjectSerializer(projects, many=True).data,
            }
        )
