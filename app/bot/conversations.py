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
                    "text": "Ми раді тебе запросити взяти участь у *Weekly Challenge* :tada:! Тут ти зможеш взяти участь у цікавих завданнях :jigsaw:, практикуватися в нових технологіях :gear: або покращити свої поточні навички :hammer_and_wrench:. Завдання чекають на тебе!",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Обирай категорію :point_down:",
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
                    "text": f"Завдання: *{task.name}* :bookmark_tabs:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "1️⃣ Відкрий завдання та скопіюй його. \n2️⃣ Надай доступ до Google Doc для всіх, хто має лінк (\"Share\" > \"General Access\" > \"Anyone with the link\"). \n3️⃣ Після виконання, надішли боту посилання на Google Doc."
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Відкрити завдання :open_book:",
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
                            "text": "Здати завдання :inbox_tray:",
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
