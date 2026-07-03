from django.db import models


class SingletonModel(models.Model):
    """Base for models that should only ever have one row (site-wide config)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteProfile(SingletonModel):
    # identity
    name = models.CharField(max_length=120, default="Ömür Ravlı")
    role = models.CharField(max_length=160, default="Multidisciplinary Engineer & Developer")
    location = models.CharField(max_length=120, default="Kayseri, Türkiye")
    university = models.CharField(max_length=160, blank=True, default="")
    # links
    email = models.EmailField(default="omurravli04@gmail.com")
    github = models.URLField(blank=True, default="")
    linkedin = models.URLField(blank=True, default="")
    cv_url = models.URLField("CV URL", blank=True, default="")
    # hero copy
    hero_badge = models.CharField(max_length=160, default="SYSTEMS ONLINE — KAYSERI, TÜRKİYE")
    hero_heading_lead = models.CharField(max_length=200, default="Ömür Ravlı builds where")
    hero_heading_accent = models.CharField(max_length=200, default="software meets machines")
    hero_subtitle = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"

    def __str__(self):
        return "Site profile"


class Stat(models.Model):
    value = models.IntegerField(default=0)
    suffix = models.CharField(max_length=8, blank=True, default="+")
    label = models.CharField(max_length=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.value}{self.suffix} — {self.label}"


class SkillCategory(models.Model):
    label = models.CharField(max_length=80)
    color = models.CharField(max_length=9, default="#8b5cf6", help_text="Hex color, e.g. #a78bfa")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Skill categories"

    def __str__(self):
        return self.label


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class TimelineEntry(models.Model):
    title = models.CharField(max_length=120)
    context = models.CharField(max_length=160)
    description = models.TextField()
    tag = models.CharField(max_length=40)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Timeline entries"

    def __str__(self):
        return self.title


class ProcessStage(models.Model):
    title = models.CharField(max_length=80)
    blurb = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Project(models.Model):
    """Curated projects. When none are active, the site falls back to live GitHub repos."""

    title = models.CharField(max_length=120)
    system = models.CharField(max_length=80, blank=True, default="", help_text="e.g. MOBILE / AI SYSTEM")
    status = models.CharField(max_length=80, blank=True, default="")
    description = models.TextField()
    stack = models.CharField(
        max_length=300, blank=True, default="", help_text="Comma-separated, e.g. Flutter, Firebase, OCR"
    )
    accent = models.CharField(max_length=9, default="#8b5cf6", help_text="Hex color")
    url = models.URLField(blank=True, default="")
    featured = models.BooleanField(default=False, help_text="Spans two columns")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
