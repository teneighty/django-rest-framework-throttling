from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import widgets
from django.utils.translation import ugettext_lazy

from rest_framework_throttling.settings import api_settings

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and api_settings.DEFAULT_NEW_USER_THROTTLE:
        for (k,v) in api_settings.ENDPOINTS.iteritems():
            UserThrottleRules.objects.create(user=instance, view=k, rate=v)
        UserThrottleRules.objects.create(
            user=instance, view='*',
            rate=api_settings.DEFAULT_NEW_USER_THROTTLE_RATE)

class UserThrottleRules(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    view = models.CharField(max_length=60, null=True, blank=True)
    rate = models.CharField(max_length=60, null=True, blank=True)

    def __unicode__(self):
        if self.view:
            return "{0}, {1}, {2}".format(self.user.username, self.view, self.rate)
        else:
            return "{0}, {1}".format(self.user.username, self.rate)

class RateSelect(widgets.MultiWidget):
    def __init__(self, attrs=None):
        denom=[("sec", ugettext_lazy("Second")),
               ("min", ugettext_lazy("Minute")),
               ("hour", ugettext_lazy("Hour")),
               ("Day", ugettext_lazy("day"))]
        _widgets = (
            widgets.NumberInput(attrs=attrs),
            widgets.Select(attrs=attrs, choices=denom),
        )
        super(RateSelect, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split('/')
        return [None, None]

    def format_output(self, rendered_widgets):
        return ' request per '.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        values = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        return '/'.join(values)

class ViewSelect(widgets.Select):
    def __init__(self, attrs=None):
        views = [(k,k) for (k,v) in api_settings.ENDPOINTS.iteritems()]
        choices = tuple(views + [('*', ugettext_lazy('All'))])
        super(ViewSelect, self).__init__(attrs, choices)

class UserThrottleRulesAdminForm(forms.ModelForm):
    class Meta:
        model = UserThrottleRules
        widgets = {
            'view':ViewSelect,
            'rate':RateSelect
        }

class UserThrottleRulesAdmin(admin.ModelAdmin):
    fields = ('user', 'view', 'rate', )
    list_display = ('user', 'view', 'rate', )
    form = UserThrottleRulesAdminForm

admin.site.register(UserThrottleRules, UserThrottleRulesAdmin)
