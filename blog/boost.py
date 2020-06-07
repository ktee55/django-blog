
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.utils.http import is_safe_url

# Loginページ以外でもリンクURLにnextを付けて前のページに戻れるようにする。
class DynamicRedirectMixin(SuccessURLAllowedHostsMixin):

    redirect_field_name = 'next'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or super().get_success_url()

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''
