"""Seed the database with the site's current content (mirrors the frontend's lib/data.ts).

Idempotent: rebuilds the list-based content each run and updates the singleton profile.
    python manage.py seed_content
"""

from django.core.management.base import BaseCommand

from content.models import (
    Project,
    ProcessStage,
    SiteProfile,
    Skill,
    SkillCategory,
    Stat,
    TimelineEntry,
)

STATS = [
    (2, "+", "Mobile Apps"),
    (3, "+", "IoT Prototypes"),
    (4, "+", "ML Workflows"),
    (2, "+", "Drone Systems"),
    (6, "+", "E-commerce Themes"),
]

SKILLS = [
    ("Programming", "#a78bfa", ["Python", "JavaScript", "TypeScript", "Java", "C++", "MATLAB", "Lua", "Dart"]),
    ("Frontend", "#22d3ee", ["React", "Next.js", "Tailwind CSS", "Responsive UI", "Motion Interfaces"]),
    ("Mobile", "#38bdf8", ["Flutter", "Firebase", "Firestore", "SQLite"]),
    ("AI / ML", "#e879f9", ["Machine Learning", "Data Processing", "OCR Workflows", "Ingredient Analysis", "Optimization"]),
    ("Embedded / Robotics", "#34d399", ["ESP32", "Arduino", "MQTT", "TFT Displays", "RGB LEDs", "Drone Systems", "Sensors"]),
    ("Game Dev", "#f472b6", ["Unity", "Roblox Studio", "Godot"]),
    ("Engineering", "#7dd3fc", ["SolidWorks", "AutoCAD", "CAD Modeling", "Mechanical Systems"]),
    ("Tools", "#c4b5fd", ["Git", "VS Code", "PlatformIO", "Firebase", "OR-Tools"]),
]

TIMELINE = [
    ("Mechanical Engineering", "Abdullah Gül University — Kayseri",
     "Mechanics, materials, thermodynamics, CAD. The systems-thinking foundation that sits under everything else I build.", "FOUNDATION"),
    ("Drone Team / Robotics", "Sidus Drone Systems",
     "Embedded logic, airframe integration and engineering trade-offs on machines where a bad assumption ends in a crash.", "ROBOTICS"),
    ("Programming & Math Instructor", "Teaching Python, Scratch, Roblox Studio, Lua",
     "Explaining loops, logic and geometry to beginners — the fastest way to find out whether you actually understand them yourself.", "EDUCATION"),
    ("Flutter App Development", "Skincare Analyzer · StudIQ",
     "Feature-based architectures, Firebase backends, OCR pipelines — mobile products designed to be used daily, not demoed once.", "MOBILE"),
    ("ESP32 / IoT Prototyping", "Café Table Ordering System",
     "MQTT state machines, TFT UI and RGB status signaling — a physical product loop from QR scan to 'order ready'.", "EMBEDDED"),
    ("E-commerce Theme Development", "Shopify / ikas storefronts",
     "Production storefront themes: responsive product and category pages, frontend fixes, real customers on the other side.", "WEB"),
    ("ML & Optimization", "OCR workflows · OR-Tools CP-SAT",
     "Data processing, ingredient analysis and constraint-based production scheduling — software that decides, not just displays.", "AI / OPT"),
]

PROCESS = [
    ("Idea", "Find the friction worth solving."),
    ("System Design", "Define inputs, constraints, architecture."),
    ("Prototype", "Build the ugliest working version, fast."),
    ("Test", "Break it before reality does."),
    ("Iterate", "Tighten tolerances, cut what's dead."),
    ("Ship", "Put it in real hands."),
]

PROJECTS = [
    ("Skincare Analyzer", "MOBILE / AI SYSTEM", "PROTOTYPE → PRODUCT",
     "Flutter app that scans skincare labels with OCR and matches every ingredient against a 247-item library with safety and category labeling. Firebase/Firestore backend with AI-assisted data cleanup for messy real-world label text.",
     "Flutter, Firebase, Firestore, OCR, AI Cleanup", "#22d3ee", True),
    ("StudIQ — Study Focus Planner", "MOBILE SYSTEM", "IN DEVELOPMENT",
     "Academic planner built in Flutter: tasks, calendar, projects, settings and onboarding on a feature-based architecture with local storage — built to survive a real semester, not a demo.",
     "Flutter, Dart, Local Storage, Feature Architecture", "#38bdf8", False),
    ("Café Table Ordering", "EMBEDDED / IOT SYSTEM", "WORKING PROTOTYPE",
     "ESP32-based table ordering prototype: QR/web order flow, MQTT state sync, TFT screen UI and RGB LED indicators driving order states — waiting, preparing, ready — with live Wi-Fi status.",
     "ESP32, MQTT, C++, TFT Display, Wi-Fi", "#34d399", False),
    ("Sidus Drone Systems", "ROBOTICS SYSTEM", "TEAM PROJECT",
     "Student drone team work spanning robotics, embedded logic and systems thinking — integrating airframe, electronics and control into one machine that actually has to fly.",
     "Drones, Embedded, Robotics, Systems Integration", "#a78bfa", False),
    ("E-commerce Theme Development", "WEB / COMMERCE SYSTEM", "PRODUCTION WORK",
     "Custom Shopify/ikas-style storefront and theme development: responsive product and category pages, frontend fixes and production-oriented UI shipped to live stores.",
     "Shopify, ikas, JavaScript, CSS, Responsive UI", "#e879f9", False),
    ("OR-Tools Production Scheduler", "OPTIMIZATION SYSTEM", "RESEARCH BUILD",
     "Python optimization project on Google OR-Tools CP-SAT: production scheduling across workers, machines and constraints, with tuned solver configuration for real factory-shaped problems.",
     "Python, OR-Tools, CP-SAT, Constraint Modeling", "#c084fc", False),
    ("Programming Education", "EDUCATION SYSTEM", "ONGOING",
     "Teaching programming and mathematics through Python, Scratch, Roblox Studio and Lua — turning game worlds into a first engineering lab for students.",
     "Python, Lua, Roblox Studio, Scratch, Mathematics", "#7dd3fc", False),
]


class Command(BaseCommand):
    help = "Seed the database with the site's current content."

    def handle(self, *args, **options):
        profile = SiteProfile.load()
        profile.name = "Ömür Ravlı"
        profile.role = "Multidisciplinary Engineer & Developer"
        profile.location = "Kayseri, Türkiye"
        profile.university = "Abdullah Gül University"
        profile.email = "omurravli04@gmail.com"
        profile.github = "https://github.com/omurravli"
        profile.linkedin = "https://linkedin.com/in/omurravli/"
        profile.hero_badge = "SYSTEMS ONLINE — KAYSERI, TÜRKİYE"
        profile.hero_heading_lead = "Ömür Ravlı builds where"
        profile.hero_heading_accent = "software meets machines"
        profile.hero_subtitle = (
            "Mechanical engineering student and multidisciplinary developer creating mobile apps, "
            "IoT systems, ML workflows, drone projects, optimization tools, and modern web experiences."
        )
        profile.save()

        Stat.objects.all().delete()
        for i, (value, suffix, label) in enumerate(STATS):
            Stat.objects.create(value=value, suffix=suffix, label=label, order=i)

        SkillCategory.objects.all().delete()
        for i, (label, color, skills) in enumerate(SKILLS):
            cat = SkillCategory.objects.create(label=label, color=color, order=i)
            for j, name in enumerate(skills):
                Skill.objects.create(category=cat, name=name, order=j)

        TimelineEntry.objects.all().delete()
        for i, (title, context, description, tag) in enumerate(TIMELINE):
            TimelineEntry.objects.create(title=title, context=context, description=description, tag=tag, order=i)

        ProcessStage.objects.all().delete()
        for i, (title, blurb) in enumerate(PROCESS):
            ProcessStage.objects.create(title=title, blurb=blurb, order=i)

        Project.objects.all().delete()
        for i, (title, system, status, description, stack, accent, featured) in enumerate(PROJECTS):
            Project.objects.create(
                title=title, system=system, status=status, description=description,
                stack=stack, accent=accent, featured=featured, order=i, is_active=True,
            )

        self.stdout.write(self.style.SUCCESS("Seeded site content."))
