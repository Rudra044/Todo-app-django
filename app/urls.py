
from django.urls import path
from .views import (Addview, Crud, Multipleoperation)


urlpatterns = [
    path('create', Addview.as_view()),
    path('<int:id>', Crud.as_view()),
    path('batch',Multipleoperation.as_view())
]
