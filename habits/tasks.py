from celery import shared_task
from datetime import datetime, timedelta
from config import settings
bot_token = settings.TELEGRAM_API_TOKEN
from habits.models import Habit
from habits.services import create_message, send_telegram_message


@shared_task
def check_and_send_reminders():
    """
        Отправляет напоминания о привычках пользователям через Telegram.
    """
    good_habit = Habit.objects.filter(sign_of_pleasant=False)
    now_time = datetime.now().time()
    now_date = datetime.now().today()

    for habit in good_habit:
        if not habit.next_date:
            if habit.time < now_time:

                chat_id, message = create_message(habit)
                send_telegram_message(chat_id, message, bot_token)
                habit.next_date = now_date + timedelta(days=habit.periodicity)
                habit.save()

            elif habit.next_date <= now_date:
                
                chat_id, message = create_message(habit)
                send_telegram_message(chat_id, message, bot_token)
                habit.next_date = now_date + timedelta(days=habit.periodicity)
                habit.save()
