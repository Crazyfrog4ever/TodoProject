from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer , UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics , mixins
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination
from rest_framework.authentication import BasicAuthentication 
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


User = get_user_model()



# Create your views here.

#Region function base view
@api_view(['GET' , 'POST'])
def all_todos(request : Request) :
    if request.method == 'GET' :
       todos = Todo.objects.order_by('priority').all()
       todo_serializer = TodoSerializer(todos , many = True)
       return Response(todo_serializer.data , status.HTTP_200_OK)
    elif request.method == 'POST' :
        serializer = TodoSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data , status.HTTP_201_CREATED)
       
    return Response(None , status.HTTP_400_BAD_REQUEST)


@api_view(['GET' , 'PUT' , 'DELETE'])
def todo_detail_view(request : Request , todo_id : int) :
    try :
        todo = Todo.objects.get(pk = todo_id)
    except Todo.DoesNotExist :
        return Response(None , status.HTTP_404_NOT_FOUND)

    if request.method == 'GET' :
        serializer = TodoSerializer(todo)
        return Response(serializer.data , status.HTTP_200_OK)

    elif request.method == 'PUT' :
        serializer = TodoSerializer(todo , data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data , status.HTTP_202_ACCEPTED)
        return Response(None , status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' :
        todo.delete()
        return Response(None , status.HTTP_204_NO_CONTENT)  
#End Region 

#Region class base view 

class TodosListApiView(APIView) :


    @extend_schema(
        request=TodoSerializer,
        responses={201: TodoSerializer},
        description='This Api Is Used For Get All Todos List'
    )
    def get(self , request : Request) :
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializer(todos , many = True)
        return Response(todo_serializer.data , status.HTTP_200_OK) 

    def post(self , request : Request) : 
        serializer = TodoSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data , status.HTTP_201_CREATED)
        else :
            return Response(None , status.HTTP_400_BAD_REQUEST)
        

class TodosDetailApiView(APIView) :

    def get_object(self, todo_id : int) :
        try :
            todo = Todo.objects.get(pk = todo_id)
        except Todo.DoesNotExist :
            return Response(None , status.HTTP_404_NOT_FOUND) 


    def get(self , request : Request , todo_id : int) :
        todo = self.get_object(todo_id)  
        serializer = TodoSerializer(todo)
        return Response(serializer.data , status.HTTP_200_OK) 

    def put(self , request : Request , todo_id : int) : 
        todo = self.get_object(todo_id) 
        serializer = TodoSerializer(todo , data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data , status.HTTP_202_ACCEPTED)
        return Response(None , status.HTTP_400_BAD_REQUEST) 

    def delete(self , request : Request , todo_id : int) :  
        todo = self.get_object(todo_id) 
        todo.delete()
        return Response(None , status.HTTP_204_NO_CONTENT)      

#End Region    


#Region Mixins 

class TodosListMixinApiView(mixins.ListModelMixin , mixins.CreateModelMixin , generics.GenericAPIView) :
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self , request : Request) :
        return self.list(request)
    

    def post(self , request : Request) :
        return self.create(request)
    

class TodosDetailMixinApiView(mixins.RetrieveModelMixin , mixins.UpdateModelMixin , mixins.DestroyModelMixin , generics.GenericAPIView) :
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer  

    def get(self , request : Request , pk) :
        return self.retrieve(request, pk) 
    

    def put(self , request : Request , pk) :
        return self.update(request, pk)
    
    def delete(self , request : Request , pk) :
        return self.destroy(request, pk)


#End Region   


#Region Generic 
    
class TodosGenericApiViewPagination(PageNumberPagination) :
    page_size = 2    

class TodosGenericApiView(generics.ListCreateAPIView) :
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = TodosGenericApiViewPagination
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class TodosGenericDetailView(generics.RetrieveUpdateDestroyAPIView) :
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer    


#End Region 


#Region ViewSets


class TodosViewsSetApiView(viewsets.ModelViewSet) :
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = LimitOffsetPagination

#End Region 


#Region Users

class UserGenericApiView(generics.ListAPIView) :
    queryset = User.objects.all()
    serializer_class = UserSerializer

#End Region              




