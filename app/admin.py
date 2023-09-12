from django.conf import settings
from django.contrib import admin, messages
from django.db.models import OuterRef, Exists, Count

from .bot.conversations import render_challenge_categories
from .bot.slack_bot import SlackBot
from .models import Category, Task, SlackUserResponse, Challenge, SlackAnswer

slack_bot = SlackBot()


class CurrentChallengeFilter(admin.SimpleListFilter):
    title = 'Current Challenge'
    parameter_name = 'current_challenge'

    def lookups(self, request, model_admin):
        return [('yes', 'Yes'), ('no', 'No')]

    def queryset(self, request, queryset):
        last_challenge_id = Challenge.objects.order_by('-id').values_list('id', flat=True).first()
        if self.value() == 'yes':
            queryset = queryset.filter(challenge_id=last_challenge_id)
        elif self.value() == 'no':
            queryset = queryset.exclude(challenge_id=last_challenge_id)
        return queryset


class SlackUserResponseAdmin(admin.ModelAdmin):
    list_filter = (CurrentChallengeFilter,)


def launch_challenge(modeladmin, request, queryset):
    channel = slack_bot.get_bot_channel(settings.SHARING_CHANNEL_NAME)
    if not channel:
        messages.error(request, "Failed to launch challenge.")
        return

    Challenge.objects.create()
    users = slack_bot.get_users_in_channel(channel['id'])
    categories_with_tasks = Category.objects.annotate(
        task_count=Count('task'),
        has_active_task=Exists(Task.objects.filter(category=OuterRef('pk'), active=True))
    ).filter(has_active_task=True)
    message = render_challenge_categories(categories_with_tasks)
    for user_id in users:
        if user_id != slack_bot.id:
            slack_bot.send_message(user_id, message)

    messages.success(request, "Challenge launched successfully.")


admin.site.register(Category)
admin.site.register(SlackAnswer)
admin.site.register(Challenge)
admin.site.register(SlackUserResponse, SlackUserResponseAdmin)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    actions = [launch_challenge]
    list_display = ('name', 'category_name', 'active', 'created_at')
    search_fields = ['category__name', 'name']
    ordering = ['-created_at']

