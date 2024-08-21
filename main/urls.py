
from django.urls import path

from main.views import TurnOnWaterWell,TurnOffWaterWell,WaterWellStatus,SortedMembersList,GroupListAPIView,GroupSortUpdateView,MembersSortUpdateView,MemberTimeUpdateAPIView,WaterWellCurrentMemberUpdateAPIView

urlpatterns = [
    # path("admin/", ),
    path('turn-on-water-well/', TurnOnWaterWell.as_view(), name='turn-on-water-well'),
    path('turn-on-water-well/<int:id>/', TurnOnWaterWell.as_view(), name='turn-on-water-well'),
    path('turn-off-water-well/', TurnOffWaterWell.as_view(), name='turn-off-water-well'),
    path('turn-off-water-well/<int:id>/', TurnOffWaterWell.as_view(), name='turn-off-water-well'),
    path('water-well-status/', WaterWellStatus.as_view(), name='water-well-status'),
    path('sorted-members-list/', SortedMembersList.as_view(), name='sorted-members-list'),
    path('group-list-api-view/', GroupListAPIView.as_view(), name='group-list-api-view-main'),
    path('group-sort-update-view/', GroupSortUpdateView.as_view(), name='group-sort-update-view-main'),
    path('members-sort-update-view/', MembersSortUpdateView.as_view(), name='members-sort-update-view-main'),
    path('member-time-update-view/<int:pk>/', MemberTimeUpdateAPIView.as_view(), name='member-time-update-view-main'),
    path('water-well-current-member-update/', WaterWellCurrentMemberUpdateAPIView.as_view(), name='water-well-current-member-update-main'),
]
