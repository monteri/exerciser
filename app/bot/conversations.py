def render_challenge_categories(categories):
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Привіт, Єноте! :rocket::female-technologist:",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Ми раді тебе запросити взяти участь у захоплюючому *Weekly Challenge*, що допоможе тобі розвивати свої навички програмування та покращувати свої знання у різних галузях. Тут ти зможеш проявити свою креативність і змагатися з іншими однодумцями.",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Обрай категорію, яка тебе найбільш зацікавлює.",
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": category.name,
                            "emoji": True
                        },
                        "value": str(category.id),
                        "action_id": f"start_{category.id}"
                    } for category in categories
                ]
            }
        ]
    }


def render_challenge_task(task):
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Завдання: {task.name}",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Відкрий завдання, де буде запропоновано його скопіювати. Далі розшар доступ для всіх у кого є лінка. Виконавши завдання, скопіюй посилання на Google Doc боту.",
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Відкрити завдання",
                            "emoji": True
                        },
                        "value": "0",
                        "url": task.content,
                        "action_id": "task_receive"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Здати завдання",
                            "emoji": True
                        },
                        "value": str(task.id),
                        "action_id": "open_submission_modal"
                    }
                ]
            }
        ]
    }


def create_submission_modal(task):
    return {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Здати завдання"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Завдання: {task.name}",
                }
            },
            {
                "type": "input",
                "block_id": "task_submission_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_submission_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Вставте посилання на Google Doc тут..."
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Посилання"
                }
            }
        ],
        "submit": {
            "type": "plain_text",
            "text": "Відправити",
        },
        "close": {
            "type": "plain_text",
            "text": "Закрити"
        },
        "private_metadata": str(task.id),
        "callback_id": "task_submission_modal"
    }
