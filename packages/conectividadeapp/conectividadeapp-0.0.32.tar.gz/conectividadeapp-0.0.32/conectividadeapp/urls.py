from django.urls import path
from . import views

urlpatterns = [

    path('listagem/', views.ListConectividadeView.as_view(), name='list'),

    # Activity URLs
    path('activity/', views.ActivityListView.as_view(), name='activity_list'),

    path('addactivity/', views.CreateactivityView.as_view(), name='addactivity'),

    path('addactor/', views.CreateActor.as_view(), name='addactor'),

    path('<int:pk>/', views.ActorView.as_view(), name='actor'),

    path('<int:pk>/edit/', views.EditActor.as_view(), name='actor_edit'),

    path('<int:pk>/delete/', views.DeleteActor.as_view(), name='actor_delete'),

    path('delete/', views.BulkDeleteActor.as_view(), name='actor_bulk_delete'),

    path('actor_list/', views.ActorListView.as_view(), name='actor_list'),

    path('searchdevice/', views.ListDeviceView.as_view(), name='searchdevice'),

    path('searchdeviceresult/', views.SearchDeviceView.as_view(), name='searchdeviceresult'),
]
