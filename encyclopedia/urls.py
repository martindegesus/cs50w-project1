from django.urls import path

from . import views

app_name='encyclopedia'

urlpatterns = [
    path('', views.index, name="index"),
    path('search/edit/<str:title>', views.edit, name="edit"),
    path('search/', views.search, name="search"),
    path('search/<str:title>', views.title, name="title"),
    path('create',views.create, name="create"),
    path('edit/<str:title>', views.edit, name="edit"),
    path('wiki/<str:title>', views.title, name="title"),
    path('<str:title>', views.title, name="title")
]
