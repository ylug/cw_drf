import requests


""" def create_interval(habit):
    # Создаем интервал для повтора

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.periodicity,
        period=IntervalSchedule.DAYS,
    )
    return schedule

def create_habit_schedule(habit):
    # Создаем задачу для повторения

    PeriodicTask.objects.create(
        interval=create_interval(habit),
        name='Check_and_send_reminders',
        task='habits.tasks.check_and_send_reminders',
        args=json.dumps(['arg1', 'arg2']),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
 )
 """


def send_telegram_message(chat_id, message, bot_token):
    """
    Отправка сообщения в телеграм
    """
    URL = "https://api.telegram.org/bot"
    response = requests.post(
        url=f"{URL}{bot_token}/sendMessage",
        data={
            'chat_id': chat_id,
            'text': message,
        }
    )

def create_message(habit):
    """Функция создания сообщения"""
    if habit.owner.chat_id:
        chat_id = habit.owner.chat_id
        message = f"Напоминание: {habit.action} в {habit.place} в {habit.time.strftime('%H:%M')}"

    if habit.reward:
        message += f" Награда за выполнение: {habit.reward}."

    if habit.related_habit:
        related_habit_action = habit.related_habit.action
        message += f" Связанная привычка: {related_habit_action}."

    return chat_id, message
