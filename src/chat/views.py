
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.parsers import JSONParser
from rest_framework import status
from chat.helper import apiResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate, logout
from chat.serializers import UserSerializer, UserImageSerializer, UserInfosSerializer,PasswordSerializer
from chat.serializers import MessageSerializer
from chat.models import User,Message
from django.contrib.auth.decorators import login_required

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        data = []
        print(request.data)
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = "user created with success"
        data.append(serializer.data)
        return apiResponse(data,message,status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        userA = {}
        code = status.HTTP_201_CREATED
        message = "user login with success"
        data = []
        email = request.data['email']
        password = request.data['password']
        userExist = User.objects.filter(email=email).first()
        user = authenticate(request, email=email, password=password)

        if userExist is None or user is None:
            code = status.HTTP_401_UNAUTHORIZED
            message = "authentication failed"
            return apiResponse(data,message,code)
        
        if not user.check_password(password):
             message ='incorrect password'
             code = status.HTTP_401_UNAUTHORIZED
        
        try:
            token = Token.objects.get(user_id=user.id)

        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        #login(request, user)
        userA['token'] = token.key
        userA['user_id'] = user.pk
        userA['email'] = user.email
        userA['name'] = user.name
        queryset = User.objects.filter(pk=user.pk)
        serializer = UserImageSerializer(queryset, context={"request": 
                      request}, many=True)
        userA['image_url'] = serializer.data[0]['image_url']
        data.append(userA)
        return apiResponse(data,message,code)

class ImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, )
    def post(self, request, format=None):
        serializer = UserImageSerializer(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        queryset = User.objects.filter(pk=request.user.id)
        serializer = UserImageSerializer(queryset, context={"request": 
                      request}, many=True)
        message = ""
        statusCode = status.HTTP_200_OK
        data = serializer.data
        return apiResponse(data, message, statusCode)

class userInfoView(APIView):
    permission_classes = [IsAuthenticated]
    data = []
    def get(self,request,user_id):
        data = []
        try:
            queryset = User.objects.filter(pk = user_id)
            serializer = UserInfosSerializer(queryset, context={"request": 
                      request}, many=True)
            message = "User displaying with success"
            statusCode = status.HTTP_201_CREATED
        except User.DoesNotExist:
            message = "User Do'es not exist"
            statusCode = status.HTTP_404_NOT_FOUND
        except:
           message = "User Do'es not exist"
           statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        data.append(serializer.data)
        return apiResponse(serializer.data,message,statusCode)
    
class authUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    data = []
    def get(self,request):
        data = []
        try:
            queryset = User.objects.filter(pk = request.user.id)
            serializer = UserInfosSerializer(queryset, context={"request": 
                      request}, many=True)
            message = "User displaying with success"
            statusCode = status.HTTP_201_CREATED
        except User.DoesNotExist:
            message = "User Do'es not exist"
            statusCode = status.HTTP_404_NOT_FOUND
        except:
           message = "User Do'es not exist"
           statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        data.append(serializer.data)
        return apiResponse(serializer.data,message,statusCode)
    
    def put(self,request):
        data = []
        try:           
            user = User.objects.get(pk = request.user.id)
        except User.DoesNotExist:
            message = "User Do'es not exist"
            statusCode = status.HTTP_404_NOT_FOUND
            return apiResponse(data,message,statusCode)
        
        serializer = UserInfosSerializer(data=request.data, instance=user)
        if serializer.is_valid():
            serializer.save()
            message = "user Updated with success"
            return apiResponse(serializer.data,message,status.HTTP_200_OK)
        else:
            message = "failure of user modification"
            return apiResponse(serializer.errors,message,status.HTTP_500_INTERNAL_SERVER_ERROR)
               

class usersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        data = []
        try:
            queryset = User.objects.all()
            serializer = UserImageSerializer(queryset, context={"request": 
                      request}, many=True)
            statusCode = status.HTTP_202_ACCEPTED
            message = "Image display with success"
        except User.DoesNotExist:
            message = "User Do'es not exist"
            statusCode = status.HTTP_404_NOT_FOUND
        except:
           message = "User Do'es not exist"
           statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        data.append(serializer.data)
        return apiResponse(data,message,statusCode)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request):
        data = []
        try:           
            user = User.objects.get(pk = request.user.id)
        except User.DoesNotExist:
            message = "User Do'es not exist"
            statusCode = status.HTTP_404_NOT_FOUND
            return apiResponse(data,message,statusCode)
        
        oldPassword = request.data['old_password']
        password = request.data['password']
        passwordConfirmation = request.data['password_confirmation']
        if not user.check_password(oldPassword):
             message ="incorrect password / the passwords don't match"
             statusCode = status.HTTP_401_UNAUTHORIZED
             return apiResponse(data,message,statusCode)
        if password != passwordConfirmation:
            message ="incorrect password / the passwords don't match"
            statusCode = status.HTTP_401_UNAUTHORIZED
            return apiResponse(data,message,statusCode)
        
        serializer = PasswordSerializer(data=request.data, instance=user)
        if serializer.is_valid():
            serializer.save()
            message = "Password Updated With Success"
            return apiResponse(serializer.data,message,status.HTTP_200_OK)
        else:
            message = "Failure to update password"
            return apiResponse(serializer.errors,message,status.HTTP_500_INTERNAL_SERVER_ERROR)

class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        message ='Sucessfully logged out'
        return apiResponse([],message,status.HTTP_200_OK)

class allUsers(APIView):
    permission_classes = [IsAuthenticated]
    data = []
    def get(self,request):
        data = []
        try:
            queryset = User.objects.exclude(pk = request.user.id).order_by('name')
            serializer = UserInfosSerializer(queryset, context={"request": 
                      request}, many=True)
            message = "Users displaying with success"
            statusCode = status.HTTP_201_CREATED
        except User.DoesNotExist:
            message = "Users Do'es not exist"
            statusCode = status.HTTP_404_NOT_FOUND
        except:
           message = "Users Do'es not exist"
           statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        data.append(serializer.data)
        return apiResponse(serializer.data,message,statusCode)

class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request,id):
        message = "Message created with success"
        statusCode =status.HTTP_201_CREATED
        try:
            User.objects.filter(pk = id) 
        except User.DoesNotExist:
            message = "Users Do'es not exist"
            statusCode = status.HTTP_404_NOT_FOUND
        except:
           message = "Users Do'es not exist"
           statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = []
        
        content = request.data['content']
        Message.objects.create(
            sender_id = request.user.id,
            content = content,
            receiver_id = id
        )
       
        return apiResponse(data,message,statusCode)
        
    def get(self,request,id):
        data = []
        try:
            queryset = Message.objects.filter(Q(receiver_id = id, sender_id = request.user.id ) | Q(receiver_id = request.user.id, sender_id = id)).order_by('created_at')
            serializer = MessageSerializer(queryset, context={"request": 
                      request}, many=True)
            message = "Messages displaying with success"
            statusCode = status.HTTP_201_CREATED
        except User.DoesNotExist:
            message = "Messages Do'es not exist"
            statusCode = status.HTTP_404_NOT_FOUND
        except:
           message = "Messages Do'es not exist"
           statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        data.append(serializer.data)
        return apiResponse(serializer.data,message,statusCode)