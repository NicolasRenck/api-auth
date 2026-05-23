from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import LogAcesso


# ─────────────────────────────────────────
# TESTES DO MODEL
# ─────────────────────────────────────────

class LogAcessoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="nicolasssd",
            password="django111"
        )
        self.log = LogAcesso.objects.create(
            usuario=self.user,
            ip="127.0.0.1"
        )

    def test_criacao_log(self):
        """Verifica se o log foi criado corretamente"""
        self.assertEqual(self.log.usuario, self.user)
        self.assertEqual(self.log.ip, "127.0.0.1")

    def test_criado_em_preenchido_automaticamente(self):
        """Verifica se criada_em é preenchido automaticamente"""
        self.assertIsNotNone(self.log.criada_em)

    def test_log_deletado_ao_deletar_usuario(self):
        """Verifica CASCADE — log some quando usuário é deletado"""
        self.user.delete()
        self.assertFalse(LogAcesso.objects.filter(ip="127.0.0.1").exists())


# ─────────────────────────────────────────
# TESTES DE REGISTRO
# ─────────────────────────────────────────

class RegisterTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_registro_sucesso(self):
        """POST /api/register/ deve criar usuário e retornar 201"""
        data = {
            "username": "novouser",
            "password": "senha123",
            "email": "novo@email.com"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="novouser").exists())

    def test_registro_username_duplicado(self):
        """POST /api/register/ com username existente deve retornar 400"""
        User.objects.create_user(username="existente", password="senha123")
        data = {
            "username": "existente",
            "password": "senha123"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# TESTES DE TOKEN (LOGIN)
# ─────────────────────────────────────────

class TokenTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="nicolasssd",
            password="django111"
        )

    def test_login_sucesso(self):
        """POST /api/token/ com credenciais corretas deve retornar tokens"""
        response = self.client.post("/api/token/", {
            "username": "nicolasssd",
            "password": "django111"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_senha_errada(self):
        """POST /api/token/ com senha errada deve retornar 401"""
        response = self.client.post("/api/token/", {
            "username": "nicolas",
            "password": "senhaerrada"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─────────────────────────────────────────
# TESTES DO ENDPOINT /me/
# ─────────────────────────────────────────

class MeViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="nicolasssd",
            password="django111",
            email="nicolas@gmail.com"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_me(self):
        """GET /api/me/ deve retornar dados do usuário autenticado"""
        response = self.client.get("/api/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "nicolasssd")
        self.assertEqual(response.data["email"], "nicolas@gmail.com")

    def test_patch_me_email(self):
        """PATCH /api/me/ deve atualizar email do usuário"""
        response = self.client.patch("/api/me/", {"email": "novo@email.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "novo@email.com")

    def test_patch_me_username(self):
        """PATCH /api/me/ deve atualizar username do usuário"""
        response = self.client.patch("/api/me/", {"username": "nicolasatualizado"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "nicolasatualizado")

    def test_me_sem_autenticacao(self):
        """GET /api/me/ sem token deve retornar 401"""
        client = APIClient()
        response = client.get("/api/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─────────────────────────────────────────
# TESTES DE TROCA DE SENHA
# ─────────────────────────────────────────

class ChangePasswordTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="nicolasssd",
            password="django111"
        )
        self.client.force_authenticate(user=self.user)

    def test_troca_senha_sucesso(self):
        """POST /api/change-password/ com senha correta deve retornar 200"""
        response = self.client.post("/api/change-password/", {
            "old_password": "django111",
            "new_password": "novasenha456"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_troca_senha_atual_errada(self):
        """POST /api/change-password/ com senha atual errada deve retornar 400"""
        response = self.client.post("/api/change-password/", {
            "old_password": "senhaerrada",
            "new_password": "novasenha456"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_troca_senha_sem_autenticacao(self):
        """POST /api/change-password/ sem token deve retornar 401"""
        client = APIClient()
        response = client.post("/api/change-password/", {
            "old_password": "senha123",
            "new_password": "novasenha456"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─────────────────────────────────────────
# TESTES DE LOGOUT
# ─────────────────────────────────────────

def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(
        username="userlogout",
        password="senha123"
    )
    self.client.force_authenticate(user=self.user)

def test_logout_sucesso(self):
    """POST /api/logout/ com refresh token válido deve retornar 200"""
    refresh = str(RefreshToken.for_user(self.user))
    response = self.client.post("/api/logout/", {"refresh": refresh})
    self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_logout_sem_token(self):
    """POST /api/logout/ sem refresh token deve retornar 400"""
    response = self.client.post("/api/logout/", {})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# TESTES DE LOG DE ACESSO
# ─────────────────────────────────────────

class LogAcessoAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="nicolasssd",
            password="django111"
        )
        self.client.force_authenticate(user=self.user)
        LogAcesso.objects.create(usuario=self.user, ip="127.0.0.1")

    def test_listar_logs(self):
        """GET /api/log-acesso/ deve retornar 200"""
        response = self.client.get("/api/log-acesso/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logs_isolados_por_usuario(self):
        """Usuário não deve ver logs de outro usuário"""
        outro_user = User.objects.create_user(
            username="outro",
            password="senha123"
        )
        LogAcesso.objects.create(usuario=outro_user, ip="192.168.0.1")

        response = self.client.get("/api/log-acesso/")
        logs = response.data.get("results", response.data)
        ips = [log["ip"] for log in logs]
        self.assertNotIn("192.168.0.1", ips)

    def test_logs_sem_autenticacao(self):
        """GET /api/log-acesso/ sem token deve retornar 401"""
        client = APIClient()
        response = client.get("/api/log-acesso/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)