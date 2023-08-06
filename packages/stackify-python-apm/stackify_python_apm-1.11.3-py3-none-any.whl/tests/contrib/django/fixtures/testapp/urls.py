from __future__ import absolute_import

from django.conf.urls import url

from tests.contrib.django.fixtures.testapp.views import exception, index, rum, rum_auto, test_logging


urlpatterns = (
    url(r"^index$", index, name="index"),
    url(r"^exception$", exception, name="exception"),
    url(r"^rum$", rum, name="rum"),
    url(r"^rum_auto$", rum_auto, name="rum_auto"),
    url(r"^test_logging$", test_logging, name="test_logging")
    # url(r"^rum_without_curly_braces$", rum, name="rum_without_curly_braces"),
)
