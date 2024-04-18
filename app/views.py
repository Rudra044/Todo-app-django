from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todos
from .serializers import Todosserializers
# Create your views here.


class Addview(APIView):
    def post(self, request):
        serializer = Todosserializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        value = Todos.objects.all()
        serializer = Todosserializers(value, many=True)
        return Response(serializer.data, status=200)


class Crud(APIView):
    def get(self, request, id):
        value = Todos.objects.get(id=id)
        serializer = Todosserializers(value)
        return Response(serializer.data, status=200)
    
    def delete(self, request, id):
        value = Todos.objects.get(id=id)
        value.delete()
        return Response("Todo deleted successfully", status=204)

    def patch(self, request, id):
        value = Todos.objects.get(id=id)
        serializer = Todosserializers(value, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=404)


class Multipleoperation(APIView):
    def process_batch(self, batch_data):
        response_data = []
        for operation in batch_data:
            method = operation.get('method')
            data = operation.get('data')
            todo_id = operation.get('id')

            if method not in ['create', 'read', 'update', 'delete']:
                response_data.append({'error': 'Invalid method'})
                continue

            if method in ['create', 'update']:
                if not data:
                    response_data.append({'error': f'data missing for {method} operation'})
                    continue

                title = data.get('title')
                description = data.get('description')
                if not title or not description:
                    response_data.append({'error': 'Title and description are required'})
                    continue

            try:
                if method == 'create':
                    todos_serializer = Todosserializers(data=data)
                    if todos_serializer.is_valid():
                        todos_serializer.save()
                        response_data.append({'result': f'{method.capitalize()} operation successful'})
                    else:
                        response_data.append({'error': todos_serializer.errors})
                elif method == 'read':
                    todo = Todos.objects.get(pk=todo_id)
                    todos_data = Todosserializers(todo).data
                    response_data.append({'result': 'Read operation successful', **todos_data})
                elif method == 'update':
                    todo = Todos.objects.get(pk=todo_id)
                    todos_serializer = Todosserializers(instance=todo, data=data, partial=True)
                    if todos_serializer.is_valid():
                        todos_serializer.save()
                        response_data.append({'result': 'Update operation successful'})
                    else:
                        response_data.append({'error': todos_serializer.errors})
                elif method == 'delete':
                    todo = Todos.objects.get(pk=todo_id)
                    todo.delete()
                    response_data.append({'result': 'Delete operation successful'})
            except Todos.DoesNotExist:
                response_data.append({'error': 'Todo not found'})

        return response_data
    