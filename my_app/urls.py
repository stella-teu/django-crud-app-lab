from django.urls import path
from .views import (Home, 
                    MonkeyList, 
                    MonkeyDetail, 
                    FeedingList, 
                    FeedingDetail,
                    ToyList,
                    ToyDetail,
                    AddToyToMonkey,
                    RemoveToyFromMonkey)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('monkeys/', MonkeyList.as_view(), name='monkey_list'),
    path('monkeys/<int:id>', MonkeyDetail.as_view(), name='monkey_detail'),
    path('monkeys/<int:monkey_id>/feedings', FeedingList.as_view(), name='feeding_list'),
    path('monkeys/<int:monkey_id>/feedings/<int:id>', FeedingDetail.as_view(), name='feeding_detail'),
    path('toys/', ToyList.as_view(), name='toy_list'),
    path('toys/<int:id>', ToyDetail.as_view(), name='toy_detail'),
    path('monkeys/<int:monkey_id>/add_toy/<int:toy_id>/', AddToyToMonkey.as_view(), name='add_toy_to_monkey'),
    path('monkeys/<int:monkey_id>/remove_toy/<int:toy_id>/', RemoveToyFromMonkey.as_view(), name='remove_toy_from_monkey'),
]