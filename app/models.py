from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (
    Model, CharField, ForeignKey, SET_NULL, CASCADE, DateTimeField, BooleanField, TextField, IntegerField
)

from app.bot.slack_bot import SlackBot

slack_bot = SlackBot()


class Category(Model):
    name = CharField(max_length=255, unique=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.name


class Task(Model):
    category = ForeignKey(Category, on_delete=CASCADE)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    name = CharField(max_length=255)
    content = CharField(max_length=500)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    active = BooleanField(default=False)

    def category_name(self):
        return self.category.name

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Challenge(Model):
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Challenge#{self.id}"


class SlackAnswer(Model):
    grade = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    text = TextField(blank=True)

    def __str__(self):
        return f"Grade: {self.grade}, text: {self.text}"


class SlackUserResponse(Model):
    slack_user_id = CharField(max_length=32)
    slack_user_username = CharField(max_length=32)
    slack_user_name = CharField(max_length=64)
    challenge = ForeignKey(Challenge, on_delete=CASCADE, null=True)
    task = ForeignKey(Task, on_delete=CASCADE)
    response = TextField()
    answer = ForeignKey(SlackAnswer, on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return f"User: {self.slack_user_name} ({self.slack_user_name}), Task: {self.task}"

    def save(self, *args, **kwargs):
        original_answer = None
        if self.pk:
            try:
                original_answer = SlackUserResponse.objects.get(pk=self.pk).answer
            except SlackUserResponse.DoesNotExist:
                pass
        super(SlackUserResponse, self).save(*args, **kwargs)

        if original_answer is None and self.answer is not None:
            slack_bot.send_message(self.slack_user_id, {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{''.join([':star:' for _ in range(self.answer.grade)])}",
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": self.answer.text
                        }
                    }
                ]
            })
