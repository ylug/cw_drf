from django.urls import path
from habits.apps import HabitsConfig
from habits.views import GoodHabitListAPIView, HabitCreateAPIView, HabitDestroyView, HabitRetrieveView, HabitUpdateView, NiceHabitListAPIView, OwnerHabitListAPIView


app_name = HabitsConfig.name


urlpatterns = [
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habit/list/good/', GoodHabitListAPIView.as_view(), name='good_habits-list'),
    path('habit/list/nice/', NiceHabitListAPIView.as_view(), name='nice_habits-list'),
    path('habit/list/owner/', OwnerHabitListAPIView.as_view(), name='owner_habits-list'),
    path('habit/<int:pk>/', HabitRetrieveView.as_view(), name='habit-get'),
    path('habit/<int:pk>/update/', HabitUpdateView.as_view(), name='habit-update'),
    path('habit/<int:pk>/delete/', HabitDestroyView.as_view(), name='habit-delete'),
]
