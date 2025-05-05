from django.urls import path
from .views import Home, MonkeyList, MonkeyDetail

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('monkeys/', MonkeyList.as_view(), name='monkey_list'),
    path('monkeys/<int:id>', MonkeyDetail.as_view(), name='monkey_detail')
]