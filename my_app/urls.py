from django.urls import path
from .views import Home, MonkeyList, MonkeyDetail, FeedingList, FeedingDetail

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('monkeys/', MonkeyList.as_view(), name='monkey_list'),
    path('monkeys/<int:id>', MonkeyDetail.as_view(), name='monkey_detail'),
    path('monkeys/<int:monkey_id>/feedings', FeedingList.as_view(), name='feeding_list'),
    path('monkey/<int:monkey_id>/feedings/<int:id>', FeedingDetail.as_view(), name='feeding_detail')
]