import django
from django.conf import settings
from django.test import Client as DjangoClient
from django.urls import reverse
from unittest import TestCase
try:
    from unittest import mock
except Exception:
    import mock

from stackifyapm.conf.constants import RUM_COOKIE_NAME
from stackifyapm.conf.constants import RUM_SCRIPT_SRC
from stackifyapm.base import Client
from stackifyapm.instrumentation import control
from stackifyapm.instrumentation import register
from tests.contrib.django.fixtures.testapp.settings import TEST_SETTINGS
from stackifyapm.contrib.django.apps import register_handlers

CONFIG = {
    "SERVICE_NAME": "service_name",
    "ENVIRONMENT": "production",
    "HOSTNAME": "sample_host",
    "FRAMEWORK_NAME": "framework",
    "FRAMEWORK_VERSION": "1.0",
    "APPLICATION_NAME": "sample_application",
    "BASE_DIR": "path/to/application/",
    "PREFIX_ENABLED": True,
}


class StackifyAPMConfigTest(TestCase):
    def setUp(self):
        # mock setup logging so it will not log any traces
        self.setup_logging = mock.patch('stackifyapm.conf.setup_logging')
        self.setup_logging.start()
        register._cls_registers = {
            "stackifyapm.instrumentation.packages.logger.LoggerInstrumentation",
        }

    def set_up_client(self):
        self.client = Client(CONFIG)
        if not settings.configured:
            settings.configure(**TEST_SETTINGS)
            django.setup()

        self.django_client = DjangoClient()
        control.instrument(self.client)

    def tearDown(self):
        control.uninstrument()
        self.setup_logging.stop()

    def test_begin_transaction(self):
        begin_transaction = mock.patch('stackifyapm.base.Client.begin_transaction')
        mock_begin_transaction = begin_transaction.start()
        end_transaction = mock.patch('stackifyapm.base.Client.end_transaction')
        end_transaction.start()
        self.set_up_client()
        register_handlers(self.client)

        self.django_client.get(reverse('index'))

        assert mock_begin_transaction.called
        assert mock_begin_transaction.call_args_list[0][0][0] == 'request'

        begin_transaction.stop()
        end_transaction.stop()

    def test_end_transaction(self):
        end_transaction = mock.patch('stackifyapm.base.Client.end_transaction')
        mock_end_transaction = end_transaction.start()
        self.set_up_client()
        register_handlers(self.client)

        self.django_client.get(reverse('index'))

        assert mock_end_transaction.called

        end_transaction.stop()

    def test_exception(self):
        capture_exception = mock.patch('stackifyapm.base.Client.capture_exception')
        mock_capture_exception = capture_exception.start()
        self.set_up_client()
        register_handlers(self.client)

        with self.assertRaises(Exception):
            self.django_client.get(reverse('exception'))

        assert mock_capture_exception.called

        capture_exception.stop()

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_response_should_contain_stackify_header(self, get_property_info_mock):
        get_property_info_mock.return_value = {}
        self.set_up_client()
        register_handlers(self.client)

        res = self.django_client.get(reverse('index'))

        assert res.has_header('X-StackifyID')

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_stackify_header_should_not_include_client_and_device_id(self, get_property_info_mock):
        get_property_info_mock.return_value = {}
        self.set_up_client()
        register_handlers(self.client)

        res = self.django_client.get(reverse('index'))

        assert "C" not in res._headers.get('x-stackifyid')[1]
        assert "CD" not in res._headers.get('x-stackifyid')[1]

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_stackify_header_should_contain_client_id(self, get_property_info_mock):
        get_property_info_mock.return_value = {"clientId": "some_id"}
        self.set_up_client()
        register_handlers(self.client)

        res = self.django_client.get(reverse('index'))

        assert "Csome_id" in res._headers.get('x-stackifyid')[1]
        assert "CDsome_id" not in res._headers.get('x-stackifyid')[1]

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_stackify_header_should_contain_device_id(self, get_property_info_mock):
        get_property_info_mock.return_value = {"deviceId": "some_id"}
        self.set_up_client()
        register_handlers(self.client)

        res = self.django_client.get(reverse('index'))

        assert "Csome_id" not in res._headers.get('x-stackifyid')[1]
        assert "CDsome_id" in res._headers.get('x-stackifyid')[1]

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_stackify_header_should_contain_client_and_device_id(self, get_property_info_mock):
        get_property_info_mock.return_value = {"deviceId": "some_id", "clientId": "some_id"}
        self.set_up_client()
        register_handlers(self.client)

        res = self.django_client.get(reverse('index'))

        assert "Csome_id" in res._headers.get('x-stackifyid')[1]
        assert "CDsome_id" in res._headers.get('x-stackifyid')[1]

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_get_client_property_call(self, get_property_info_mock):
        get_property_info_mock.return_value = {"deviceId": "some_id", "clientId": "some_id"}
        self.set_up_client()
        register_handlers(self.client)

        # do multiple requests
        self.django_client.get(reverse('index'))
        self.django_client.get(reverse('index'))
        res = self.django_client.get(reverse('index'))

        assert get_property_info_mock.call_count == 1
        assert "Csome_id" in res._headers.get('x-stackifyid')[1]
        assert "CDsome_id" in res._headers.get('x-stackifyid')[1]

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_get_client_property_call_fallback(self, get_property_info_mock):
        get_property_info_mock.side_effect = [
            {},  # first get_properties call making sure property is empty
            {"deviceId": "some_id", "clientId": "some_id"},  # second get_properties call
        ]
        self.set_up_client()
        register_handlers(self.client)

        # do multiple requests
        self.django_client.get(reverse('index'))
        self.django_client.get(reverse('index'))
        res = self.django_client.get(reverse('index'))

        assert get_property_info_mock.call_count == 2
        assert "Csome_id" in res._headers.get('x-stackifyid')[1]
        assert "CDsome_id" in res._headers.get('x-stackifyid')[1]

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_rum_injection(self, get_property_info_mock):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}

        self.set_up_client()
        register_handlers(self.client)

        res = self.django_client.get(reverse('rum'))

        assert '<script src="{}"'.format(RUM_SCRIPT_SRC) in str(res.content)
        assert '</script>' in str(res.content)
        assert 'data-host="Client Rum Domain"' in str(res.content)
        assert '|CClient ID|CDDevice ID"' in str(res.content)

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_rum_cookie(self, get_property_info_mock):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}

        self.set_up_client()
        register_handlers(self.client)

        res = self.django_client.get(reverse('rum'))
        cookie = res.cookies.get(RUM_COOKIE_NAME)

        assert "Path=/" in cookie.output()
        assert cookie

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_rum_auto_injection(self, get_property_info_mock):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}

        self.set_up_client()
        register_handlers(self.client)

        res = self.django_client.get(reverse('rum_auto'))

        assert '<script src="{}"'.format(RUM_SCRIPT_SRC) in str(res.content)
        assert '</script>' in str(res.content)
        assert 'data-host="Client Rum Domain"' in str(res.content)
        assert '|CClient ID|CDDevice ID"' in str(res.content)

        # making sure manual rum injection still working
        assert str(res.content).count('<script src="{}"'.format(RUM_SCRIPT_SRC)) == 1

    @mock.patch('stackifyapm.base.Client.queue')
    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_rum_trace_property(self, get_property_info_mock, mock_queue):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}

        self.set_up_client()
        register_handlers(self.client)

        res = self.django_client.get(reverse('rum'))
        cookie = res.cookies.get(RUM_COOKIE_NAME)

        assert cookie
        assert mock_queue.called
        assert mock_queue.call_args_list[0][0][0].get_context()['rum']


class TestPrefixInstrumentation(TestCase):
    def setUp(self):
        # mock setup logging so it will not log any traces
        self.setup_logging = mock.patch('stackifyapm.conf.setup_logging')
        self.setup_logging.start()
        register._cls_registers = {
            "stackifyapm.instrumentation.packages.logger.LoggerInstrumentation",
        }

    def set_up_client(self):
        self.client = Client(CONFIG)
        if not settings.configured:
            settings.configure(**TEST_SETTINGS)
            django.setup()

        self.django_client = DjangoClient()
        control.instrument(self.client)

    @mock.patch('stackifyapm.base.Client.queue')
    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_transaction_prefix_data(self, get_property_info_mock, mock_queue):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}

        self.set_up_client()
        register_handlers(self.client)

        self.django_client.post(reverse('rum'), {"foo": "bar"})

        assert mock_queue.called

        transaction_dict = mock_queue.call_args_list[0][0][0].to_dict()

        assert transaction_dict.get('props', {}).get('PREFIX_REQUEST_BODY')
        assert transaction_dict.get('props', {}).get('PREFIX_REQUEST_SIZE_BYTES')
        assert transaction_dict.get('props', {}).get('PREFIX_REQUEST_HEADERS')
        assert transaction_dict.get('props', {}).get('PREFIX_RESPONSE_BODY')
        assert transaction_dict.get('props', {}).get('PREFIX_RESPONSE_SIZE_BYTES')
        assert transaction_dict.get('props', {}).get('PREFIX_RESPONSE_HEADERS')

    @mock.patch('stackifyapm.base.Client.queue')
    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_transaction_exception(self, get_property_info_mock, mock_queue):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}

        self.set_up_client()
        register_handlers(self.client)

        with self.assertRaises(Exception):
            self.django_client.post(reverse('exception'), {"foo": "bar"})

        assert mock_queue.called

        transaction_dict = mock_queue.call_args_list[0][0][0].to_dict()

        assert transaction_dict.get('props', {}).get('PREFIX_REQUEST_BODY')
        assert transaction_dict.get('props', {}).get('PREFIX_REQUEST_SIZE_BYTES')
        assert transaction_dict.get('props', {}).get('PREFIX_REQUEST_HEADERS')
        assert transaction_dict.get('props', {}).get('PREFIX_RESPONSE_BODY')
        assert transaction_dict.get('props', {}).get('PREFIX_RESPONSE_SIZE_BYTES')
        assert transaction_dict.get('props', {}).get('PREFIX_RESPONSE_HEADERS')

    @mock.patch('stackifyapm.base.Client.queue')
    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_span_logging(self, get_property_info_mock, mock_queue):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}

        self.set_up_client()
        register_handlers(self.client)

        self.django_client.post(reverse('test_logging'))

        assert mock_queue.called

        transaction = mock_queue.call_args_list[0][0][0]
        assert transaction
        assert transaction.get_spans()

        span = transaction.get_spans()[0]
        span_data = span.to_dict()

        assert span_data['reqBegin']
        assert span_data['reqEnd']
        assert span_data['transaction_id']
        assert span_data['call'] == 'cpython.logging'
        assert span_data['props']
        assert span_data['props']['CATEGORY'] == 'Log'
        assert span_data['props']['SUBCATEGORY'] == 'Logger'
        assert span_data['props']['LEVEL'] == 'INFO'
        assert span_data['props']['MESSAGE'] == 'test info log'
