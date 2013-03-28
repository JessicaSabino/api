from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth import login
from atados.nonprofit.forms import RegistrationForm
from atados.nonprofit.models import Nonprofit
from atados.volunteer.models import Volunteer
from registration.backends.default import DefaultBackend
from registration.models import RegistrationProfile
from registration import signals


class RegistrationBackend(DefaultBackend):

    site = Site.objects.get_current()

    def register(self, request, **kwargs):
        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        new_user = RegistrationProfile.objects.create_inactive_user(username,
                                                                    email,
                                                                    password,
                                                                    self.site,
                                                                    False)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)

        new_user.first_name = kwargs['first_name']
        new_user.save();

        volunteer = Volunteer.objects.create(user=new_user)
        volunteer.save()

        nonprofit = Nonprofit.objects.create(user=new_user)
        nonprofit.name = kwargs['nonprofit_name']
        nonprofit.slug = kwargs['slug']
        nonprofit.save()

        self.send_activation_email(new_user)

        return new_user

    def post_registration_redirect(self, request, user):
        return ('nonprofit:sign-up-complete', (), {})

    def post_activation_redirect(self, request, user):
        user.backend = 'atados.core.backends.AuthenticationBackend'
        login(request, user)
        return ('nonprofit:first-step', (Nonprofit.objects.get(user=user).slug,), {})

    def get_form_class(self, request):
        return RegistrationForm

    def send_activation_email(self, user):
        site = self.site

        try:
            registration_profile = RegistrationProfile.objects.get(user=user)

            ctx_dict = { 'activation_key': registration_profile.activation_key,
                         'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                         'site': site }


            subject = _("Welcome to %s" % site.name)

            message = render_to_string('atados/nonprofit/activation_email.txt',
                                       ctx_dict)
            
            user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        
        except RegistrationProfile.DoesNotExist:
            return False
