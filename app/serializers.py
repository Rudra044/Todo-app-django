from rest_framework import serializers
from .models import Todos

class Todosserializers(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ["title", "description"]