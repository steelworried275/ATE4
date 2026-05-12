from django.contrib.auth.views import LoginView


class SimpleLoginView(LoginView):
    template_name = 'users/login.html'
