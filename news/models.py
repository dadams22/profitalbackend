from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    plaid_access_token = models.CharField(max_length=100, blank=True, null=True)

    def set_plaid_access_token(self, access_token):
        self.plaid_access_token = access_token
        self.save()

    def is_plaid_connected(self):
        return bool(self.plaid_access_token)
