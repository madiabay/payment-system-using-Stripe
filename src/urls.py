from django.contrib import admin
from django.urls import path

from items import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('item/', views.ItemsView.as_view(), name='items'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('item/<int:pk>/', views.DetailItem.as_view(), name='view_item'),
    path('buy/<int:item_id>/', views.create_checkout_session, name='buy'),
]
