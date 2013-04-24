from django.db import models
from django import forms
from core.validators import validate_family, validate_url


class Wiki_Active_User_Manager(models.Manager):
    """
    Shorcuts Manager for handle active user.
    """
    def get_active(self):
	try:
            return self.get_query_set().get(active=True)
        except Wiki_User.DoesNotExist as e:
            raise Wiki_User.NoActiveUser

    def nick(self):
        return self.get_active().nick

    def family(self):
        return self.get_active().family

    def language(self):
        return self.get_active().language

    def url(self):
        return self.get_active().url


class Wiki_User(models.Model):
    """
    Class/Table for users registered on wikis.
    """
    # TODO
    # Add validator for '/' in end of url

    nick = models.CharField(max_length=100, help_text='Your id on wiki')
    family = models.CharField(max_length=50, help_text='Your wikimedia family', validators=[validate_family])
    language = models.CharField(max_length=3)
    url = models.CharField(max_length=200, help_text='index.php URL', validators=[validate_url])
    comment = models.CharField(max_length=1000,null=True, blank=True)
    active = models.BooleanField(default=False)

    activated = Wiki_Active_User_Manager()
    objects = models.Manager()
    class Meta:
        app_label = 'core'
        ordering = ('active','nick')

    class NoActiveUser(Exception):
        """No active user found in database."""
        pass

    def __unicode__(self):
        return self.nick

    def set_active(self):
        """
        Set current user as active.
        There is only one active user.
        """
        Wiki_User.objects.exclude(id=self.id).update(active=False)
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
        widgets = {
           'nick': forms.TextInput(attrs={'class':'span3','placeholder':'Nick'}),
           'family': forms.TextInput(attrs={'class':'span2','placeholder':'Family'}),
           'language': forms.TextInput(attrs={'class':'span1','placeholder':'Language'}),
           'url': forms.TextInput(attrs={'class':'span6','placeholder':'Wiki index'}),
           'comment': forms.Textarea(attrs={'class':'span6','placeholder':'Comment'}),
           'active': forms.CheckboxInput(attrs={}),
        }
