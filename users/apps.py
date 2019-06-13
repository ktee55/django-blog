from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name ='ユーザー'

    def ready(self):
        import users.signals

