from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todos
from .serializers import Todosserializers
# Create your views here.


class Addview(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Todosserializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors) 
    

    def get(self, request, *args, **kwargs):
        value = Todos.objects.all()
        serializer = Todosserializers(value, many = True)
        return Response(serializer.data)

class Crud(APIView):
    def get(self, request, id):
        value = Todos.objects.get(id = id)
        serializer = Todosserializers(value)
        return Response(serializer.data)
    

    def delete(self, request, id):
        value = Todos.objects.filter(id = id)
        value.delete()
        return Response("Todo deleted successfully")


    def patch(self, request, id):
        value = Todos.objects.get(id = id)
        serializer = Todosserializers(value, data = request.dat, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

