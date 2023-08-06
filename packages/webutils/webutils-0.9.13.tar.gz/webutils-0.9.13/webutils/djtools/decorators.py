import urlparse

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
from django.conf import settings
from django.http import HttpResponseRedirect


def ssl_required(view_func):
    def _checkssl(request, *args, **kwargs):
        if not settings.DEBUG and not request.is_secure():
            if 'HTTP_X_FORWARDED_PROTO' not in request.META:
                # This checks for X_FORWARDED_PROTO header. Usually
                # passed when SSL is being proxied upstream.
                # This should avoid a redirect loop.
                if hasattr(settings, 'SSL_DOMAIN'):
                    url_str = urljoin(
                        settings.SSL_DOMAIN,
                        request.get_full_path()
                    )
                else:
                    url_str = request.build_absolute_uri()
                url_str = url_str.replace('http://', 'https://')
                return HttpResponseRedirect(url_str)

        return view_func(request, *args, **kwargs)
    return _checkssl
