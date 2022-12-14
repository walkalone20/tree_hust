# Generated by Django 4.1 on 2022-11-06 06:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Post", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="browser",
            field=models.ManyToManyField(
                blank=True,
                related_name="user_browser",
                to=settings.AUTH_USER_MODEL,
                verbose_name="browsered by some user",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="collection",
            field=models.ManyToManyField(
                blank=True,
                related_name="user_collection",
                to=settings.AUTH_USER_MODEL,
                verbose_name="collected by some user",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="downvote",
            field=models.ManyToManyField(
                blank=True,
                related_name="downvote_post",
                to=settings.AUTH_USER_MODEL,
                verbose_name="downvote by some user",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="posted_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_post",
                to=settings.AUTH_USER_MODEL,
                verbose_name="posted by some user",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="upvote",
            field=models.ManyToManyField(
                blank=True,
                related_name="upvote_post",
                to=settings.AUTH_USER_MODEL,
                verbose_name="upvote by some user",
            ),
        ),
        migrations.AddField(
            model_name="draft",
            name="drafted_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_draft",
                to=settings.AUTH_USER_MODEL,
                verbose_name="draft drafted by some user",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="comment_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_comment",
                to=settings.AUTH_USER_MODEL,
                verbose_name="comment by some user",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="comment_under",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="post_comment",
                to="Post.post",
                verbose_name="comment under some post",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="downvote",
            field=models.ManyToManyField(
                blank=True,
                related_name="downvote_comment",
                to=settings.AUTH_USER_MODEL,
                verbose_name="downvote by some user",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="reply_to",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comment_comment",
                to="Post.comment",
                verbose_name="commeng on other comment",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="upvote",
            field=models.ManyToManyField(
                blank=True,
                related_name="upvote_comment",
                to=settings.AUTH_USER_MODEL,
                verbose_name="upvote by some user",
            ),
        ),
    ]
