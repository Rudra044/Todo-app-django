from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todos
from .serializers import Todosserializers
# Create your views here.


class Addview(APIView):
    def post(self, request):
        serializer = Todosserializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400) 
    

    def get(self, request):
        value = Todos.objects.all()
        serializer = Todosserializers(value, many = True)
        return Response(serializer.data, status = 200)

class Crud(APIView):
    def get(self, request, id):
        value = Todos.objects.get(id = id)
        serializer = Todosserializers(value)
        return Response(serializer.data, status = 200)
    

    def delete(self, request, id):
        value = Todos.objects.get(id = id)
        value.delete()
        return Response("Todo deleted successfully", status = 204)


    def patch(self, request, id):
        value = Todos.objects.get(id = id)
        serializer = Todosserializers(value, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 200)
        return Response(serializer.errors, status = 404)

