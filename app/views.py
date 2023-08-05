import json

from django.db.models import Count, Exists, OuterRef
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .bot.actions import SlackActions
from .bot.conversations import render_challenge_categories
from .bot.slack_bot import SlackBot
from .bot.transformer import SlackApiTransformer
from .models import Category, Task

from conf import settings

slack_bot = SlackBot()


@csrf_exempt
def message(request):
    json_dict = json.loads(request.body.decode('utf-8'))
    if json_dict.get('token', None) != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=403)

    if json_dict.get('type', None) == 'url_verification':
        response_dict = {"challenge": json_dict['challenge']}
        return JsonResponse(response_dict, safe=False)

    event = json_dict.get('event', {})
    user_id = event.get('user')
    channel_id = event.get('channel')
    text = event.get('text')

    if user_id is not None and slack_bot.id != user_id:
        if text.lower() == 'start':
            slack_bot.send_message('#test', "Let's go!")

    return JsonResponse({}, status=200)


@csrf_exempt
def get_task(request):
    json_dict = json.loads(request.body.decode('utf-8'))
    event = json_dict.get('event', {})
    user_id = event.get('user')
    slack_bot.send_message(user_id, message)
    return HttpResponse(status=200)


@csrf_exempt
def button_callback(request):
    payload = json.loads(request.POST.get('payload'))
    data = SlackApiTransformer(payload)
    if not data.type:
        return HttpResponse(status=400)

    actions_handler = SlackActions(data, slack_bot)
    actions_handler.dispatch_action()

    return HttpResponse(status=200)
