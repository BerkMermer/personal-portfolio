from types import SimpleNamespace

from django.templatetags.static import static

from .models import Project

SEED_PROJECTS = [
    {
        'title': 'Courier Tracking API',
        'description': (
            'Gerçek zamanlı kurye konum takibi, Redis GEO ile akıllı atama ve '
            'STOMP ile canlı izleme. JWT kimlik doğrulama, PostgreSQL, RabbitMQ '
            've Docker Compose ile çalışan full-stack bir backend demosu.'
        ),
        'technologies': 'Java, Spring Boot, Spring Security, JWT, PostgreSQL, Redis, RabbitMQ, Docker, React, Leaflet',
        'link': 'https://github.com/BerkMermer/Live-Courier-Tracking',
        'static_image': 'portfolyo/projects/live-tracking.png',
    },
    {
        'title': 'Personal Portfolio',
        'description': (
            'Django ile geliştirilmiş kişisel portfolyo sitesi. İletişim formu, '
            'responsive arayüz ve proje kartları; Render üzerinde yayında.'
        ),
        'technologies': 'Python, Django, SQLite, HTML, CSS, JavaScript',
        'link': 'https://github.com/BerkMermer/personal-portfolio',
        'static_image': 'portfolyo/projects/portfolio.png',
    },
]


def seed_projects_as_display():
    """DB olmadan da şablona gidebilecek proje kartları."""
    items = []
    for data in SEED_PROJECTS:
        techs = [t.strip() for t in data.get('technologies', '').split(',') if t.strip()]
        image = static(data['static_image']) if data.get('static_image') else ''
        items.append(
            SimpleNamespace(
                title=data['title'],
                description=data['description'],
                link=data['link'],
                tech_list=techs,
                display_image_url=image,
            )
        )
    return items


def ensure_seed_projects():
    for data in SEED_PROJECTS:
        obj, created = Project.objects.get_or_create(
            title=data['title'],
            defaults=data,
        )
        if created:
            continue
        changed = []
        if data.get('static_image') and obj.static_image != data['static_image']:
            obj.static_image = data['static_image']
            changed.append('static_image')
        if data.get('link') and obj.link != data['link']:
            obj.link = data['link']
            changed.append('link')
        if changed:
            obj.save(update_fields=changed)
