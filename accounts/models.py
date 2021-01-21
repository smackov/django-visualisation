from django.db import models


class GuestModeCounter(models.Model):
    """The counter fo 'Guest user mode'
    
    This counter is needed for correct creating new 'Guest users in
    'Guest user mode'"""
    counter = models.IntegerField(default=1)
