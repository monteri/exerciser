from app.models import SlackUserResponse


def get_user_streak(slack_user_id):
    responses = SlackUserResponse.objects.filter(slack_user_id=slack_user_id).order_by('-challenge__id')
    streak = 0
    expected_challenge_id = responses[0].challenge_id

    for response in responses:
        if response.challenge_id == expected_challenge_id:
            streak += 1
            expected_challenge_id -= 1
        else:
            break

    return streak