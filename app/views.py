from django.shortcuts import render
from rest_framework import viewsets
from .models import LogAcesso
from .serializers import LogAcessoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from .serializers import UserSerializer
from .serializers import ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class LogAcessoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LogAcessoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LogAcesso.objects.filter(usuario=self.request.user)




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]




class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'mensagem': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)


 



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response(
                    {'erro': 'Senha atual incorreta.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()
            return Response({'mensagem': 'Senha alterada com sucesso.'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

