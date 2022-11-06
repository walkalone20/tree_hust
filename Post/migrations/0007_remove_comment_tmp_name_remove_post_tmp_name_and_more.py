# Generated by Django 4.1.2 on 2022-11-06 06:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Post", "0006_browser_history_alter_post_browser_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="tmp_name",
        ),
        migrations.RemoveField(
            model_name="post",
            name="tmp_name",
        ),
        migrations.AlterField(
            model_name="post",
            name="browser",
            field=models.ManyToManyField(
                blank=True,
                related_name="user_browser",
                to=settings.AUTH_USER_MODEL,
                verbose_name="browsered by some user",
            ),
        ),
        migrations.DeleteModel(
            name="browser_history",
        ),
    ]
