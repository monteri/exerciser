from .conversations import render_challenge_task, create_submission_modal
from ..models import Task, SlackUserResponse, Challenge
from ..utils import get_user_streak


class SlackActions:
    def __init__(self, data, slack_bot):
        self.data = data
        self.slack_bot = slack_bot

    def start_action(self):
        tasks = Task.objects.filter(category__id=self.data.value, active=True)
        current_task = tasks[0]
        message = render_challenge_task(current_task)
        self.slack_bot.send_message(self.data.user_id, message)

    def open_submission_modal(self):
        task = Task.objects.get(id=self.data.value)
        modal = create_submission_modal(task)
        self.slack_bot.client.views_open(trigger_id=self.data.trigger_id, view=modal)

    def handle_view_submission(self):
        response = self.data.values.get('task_submission_block', {}).get('task_submission_input', {}).get('value')
        task = Task.objects.get(id=self.data.metadata)
        challenge = Challenge.objects.latest('id')
        if SlackUserResponse.objects.filter(challenge=challenge, slack_user_id=self.data.user_id).exists():
            self.slack_bot.send_message(self.data.user_id, 'Ти вже успішно виконав завдання на цьому тижні! 👍')
            return
        SlackUserResponse.objects.create(
            slack_user_id=self.data.user_id,
            slack_user_username=self.data.user_username,
            slack_user_name=self.data.user_name,
            task=task,
            response=response,
            challenge=challenge,
        )
        user_streak = get_user_streak(self.data.user_id)

        self.slack_bot.send_message(self.data.user_id, f'🎉 Завдання успішно відправлено! \nТи пройшов(ла) челенжів поспіль: *{user_streak}*! 👏')

    def dispatch_action(self):
        if self.data.type == 'view_submission':
            self.handle_view_submission()
        elif self.data.action_id.startswith('start'):
            self.start_action()
        elif self.data.action_id == 'open_submission_modal':
            self.open_submission_modal()
        else:
            print(f'No action was found for action_id: {self.data.action_id}')