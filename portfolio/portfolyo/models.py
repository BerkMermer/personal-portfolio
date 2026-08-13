from django.db import models
from django.templatetags.static import static


class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name='Başlık')
    description = models.TextField(verbose_name='Açıklama')
    image = models.ImageField(
        upload_to='portfolio/images/',
        blank=True,
        null=True,
        verbose_name='Ekran görüntüsü',
        help_text='Admin yüklemesi. Dosya yoksa aşağıdaki statik görsel kullanılır.'
    )
    static_image = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Statik görsel',
        help_text='Örn: portfolyo/projects/live-tracking.png — GitHub’a gider.'
    )
    technologies = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Teknolojiler',
        help_text='Virgülle ayırın. Örn: Django, PostgreSQL, REST, JWT'
    )
    link = models.URLField(blank=True, verbose_name='Proje linki')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    @property
    def display_image_url(self):
        if self.image:
            try:
                if self.image.storage.exists(self.image.name):
                    return self.image.url
            except (ValueError, OSError):
                pass
        if self.static_image:
            return static(self.static_image)
        return ''

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
