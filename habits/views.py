from django.shortcuts import render
from rest_framework import generics
from habits.models import Habit
from rest_framework.permissions import IsAuthenticated, AllowAny
from habits.paginators import HabitsPagination
from habits.serializers import HabitSerializer
from habits.permissions import IsOwner


class HabitCreateAPIView(generics.CreateAPIView):
    """ Создание привычки """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class GoodHabitListAPIView(generics.ListAPIView):
    """Просмотр всех публичных полезных привычек, но не более 5 на странице."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(sign_of_pleasant=False, is_published=True)
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPagination


class NiceHabitListAPIView(generics.ListAPIView):
    """Просмотр всех публичных приятных привычек, но не более 5 на странице."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(sign_of_pleasant=True, is_published=True)
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPagination


class OwnerHabitListAPIView(generics.ListAPIView):
    """Просмотр всех привычек пользователя, но не более 5 на странице."""
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitRetrieveView(generics.RetrieveAPIView):
    """Просмотр привычки по ID"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateView(generics.UpdateAPIView):
    """Редактирование привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyView(generics.DestroyAPIView):
    """Удаление привычки"""
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
