from django.db import models
from django import forms

class Wiki_Active_User_Manager(models.Manager):
    """
    Shorcuts Manager for handle active user.
    """
    def get_active(self):
        return self.get_query_set().get(active=True)

    def nick(self):
        self.get_active().nick

    def family(self):
        self.get_active().family

    def language(self):
        self.get_active().language

    def url(self):
        self.get_active().url


class Wiki_User(models.Model):
    """
    Class/Table for users registered on wikis.
    """
    # TODO
    # Add validator for '/' in end of url
    activated = Wiki_Active_User_Manager()
    objects = models.Manager()
    class Meta:
        app_label = 'core'
        ordering = ('active','nick')

    nick = models.CharField(max_length=100, help_text='Your id on wiki')
    family = models.CharField(max_length=50, help_text='Your wikimedia family')
    language = models.CharField(max_length=3)
    url = models.CharField(max_length=200, help_text='index.php URL')
    comment = models.CharField(max_length=1000,null=True, blank=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nick

    def set_active(self):
        """
        Set current user as active.
        There is only one active user.
        """
        Wiki_User.objects.update(active=False)
        self.active = True
        self.save()

    def save(self,*args,**kwargs):
       """
       This method is overided for set all users unactived
       if the one saved is active.
       """
       if self.active:
           Wiki_User.objects.exclude(id=self.id).update(active=False)
       super(Wiki_User, self).save(*args,**kwargs)


class Wiki_User_Form(forms.ModelForm):
    class Meta:
        model = Wiki_User
