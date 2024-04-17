
from rest_framework import serializers
from datetime import timedelta
from rest_framework.serializers import ValidationError


def choose_related_habit_or_reward(value):

    related_habit = value["related_habit"]
    reward = value["reward"]
    if related_habit and reward:
        raise serializers.ValidationError("Нельзя одновременно выбирать связанную привычку и указывать вознаграждение")


def long_execution_time(value):
    time = timedelta(minutes=2)

    time_to_complete = value['time_to_complete']
    if time_to_complete > time:
        raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд")


def related_is_pleasant(value):

    if value["related_habit"]:
        if not value["related_habit"].sign_of_pleasant:
            raise serializers.ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки")


def pleasant_format(value):

    sign_of_pleasant = value["sign_of_pleasant"]
    reward = value["reward"]
    related_habit = value["related_habit"]
    if sign_of_pleasant:
        if reward or related_habit:
            raise serializers.ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")


def completion_duration(value):

    periodicity = value["periodicity"]
    if periodicity > 7:
        raise serializers.ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")
