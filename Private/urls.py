from django.urls import path

from . import views

urlpatterns = [
    path('view/', views.admin_private_view),
    path('view/<int:hid>', views.private_views),
    path('view/<str:id>', views.private_view),

    path('share/', views.share),
    path('share/<int:hid>', views.share_views),
    path('share/<str:id>', views.share_view),

    path('updatepra/', views.updatepra),

    path('remove_pri/<str:hid>', views.remove_pri),
    path('remove_photo/<str:hid>', views.remove_photo),

    path('download_data/', views.download_data),
]
