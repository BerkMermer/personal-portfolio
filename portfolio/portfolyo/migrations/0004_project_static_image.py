from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolyo', '0003_project_technologies_alter_project_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='static_image',
            field=models.CharField(
                blank=True,
                help_text="Örn: portfolyo/projects/live-tracking.png — GitHub’a gider.",
                max_length=200,
                verbose_name='Statik görsel',
            ),
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['id']},
        ),
    ]
