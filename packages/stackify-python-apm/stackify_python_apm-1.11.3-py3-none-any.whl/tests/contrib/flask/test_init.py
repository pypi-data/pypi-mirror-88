import json

from flask import Flask, render_template_string
from flask import jsonify
from flask import make_response
from unittest import TestCase
try:
    from unittest import mock
except Exception:
    import mock

from stackifyapm.base import Client
from stackifyapm.conf.constants import RUM_COOKIE_NAME
from stackifyapm.conf.constants import RUM_SCRIPT_SRC
from stackifyapm.contrib.flask import make_client
from stackifyapm.contrib.flask import StackifyAPM
from stackifyapm.instrumentation import control


CONFIG = {
    "SERVICE_NAME": "service_name",
    "ENVIRONMENT": "production",
    "HOSTNAME": "sample_host",
    "FRAMEWORK_NAME": "framework",
    "FRAMEWORK_VERSION": "1.0",
    "APPLICATION_NAME": "sample_application",
    "BASE_DIR": "path/to/application/",
}


class MakeClientTest(TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['ENVIRONMENT'] = 'test'
        self.app.config['CONFIG_FILE'] = 'stackify.json'

    def test_should_return_client(self):
        client = make_client(self.app)

        assert isinstance(client, Client)

    def test_client_config(self):
        client = make_client(self.app)

        assert client.config.application_name == 'Python Application'
        assert client.config.environment == 'test'
        assert client.config.config_file == 'stackify.json'
        assert client.config.framework_name == 'flask'
        assert client.config.framework_version


class StackifyAPMTest(TestCase):
    def setUp(self):
        # mock setup logging so it will not log any traces
        self.setup_logging = mock.patch('stackifyapm.conf.setup_logging')
        self.setup_logging.start()

        self.app = Flask('asfadsa')
        self.app.config['ENV'] = 'test'

        @self.app.route('/', methods=['GET'])
        def index():
            return jsonify(result='index')

        @self.app.route('/exception', methods=['GET'])
        def exception():
            1 / 0

    def tearDown(self):
        control.uninstrument()
        self.setup_logging.stop()

    @mock.patch('stackifyapm.base.setup_logging')
    def test_failing_creation_flask_apm(self, setup_logging_mock):
        setup_logging_mock.side_effect = Exception("Some Exception")

        # test should not raise Exception
        flask_apm = StackifyAPM(self.app)

        assert flask_apm.client is None

    def test_begin_transaction(self):
        begin_transaction = mock.patch('stackifyapm.base.Client.begin_transaction')
        mock_begin_transaction = begin_transaction.start()
        StackifyAPM(self.app)

        self.app.test_client().get('/')

        assert mock_begin_transaction.called
        assert mock_begin_transaction.call_args_list[0][0][0] == 'request'

        begin_transaction.stop()

    def test_end_transaction(self):
        end_transaction = mock.patch('stackifyapm.base.Client.end_transaction')
        mock_end_transaction = end_transaction.start()
        StackifyAPM(self.app)

        self.app.test_client().get('/')

        assert mock_end_transaction.called

        end_transaction.stop()

    def test_capture_exception(self):
        capture_exception = mock.patch('stackifyapm.base.Client.capture_exception')
        end_transaction = mock.patch('stackifyapm.base.Client.end_transaction')
        mock_capture_exception = capture_exception.start()
        end_transaction.start()
        StackifyAPM(self.app)

        self.app.test_client().get('/exception')

        assert mock_capture_exception.called
        assert mock_capture_exception.call_args_list[0][1]['exception']
        assert mock_capture_exception.call_args_list[0][1]['exception']['Frames']
        assert mock_capture_exception.call_args_list[0][1]['exception']['Timestamp']
        assert mock_capture_exception.call_args_list[0][1]['exception']['Exception']
        assert mock_capture_exception.call_args_list[0][1]['exception']['CaughtBy']
        assert mock_capture_exception.call_args_list[0][1]['exception']['Message']

        capture_exception.stop()
        end_transaction.stop()

    def test_response_should_contain_stackify_header(self):
        StackifyAPM(self.app)

        res = self.app.test_client().get('/')

        assert 'X-StackifyID' in res.headers.keys()

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_stackify_header_should_not_include_client_and_device_id(self, get_property_info_mock):
        get_property_info_mock.return_value = {}
        StackifyAPM(self.app)

        res = self.app.test_client().get('/')

        assert "C" not in res.headers.get('X-StackifyID')
        assert "CD" not in res.headers.get('X-StackifyID')

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_stackify_header_should_contain_client_id(self, get_property_info_mock):
        get_property_info_mock.return_value = {"clientId": "some_id"}
        StackifyAPM(self.app)

        res = self.app.test_client().get('/')

        assert "Csome_id" in res.headers.get('X-StackifyID')
        assert "CDsome_id" not in res.headers.get('X-StackifyID')

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_stackify_header_should_contain_device_id(self, get_property_info_mock):
        get_property_info_mock.return_value = {"deviceId": "some_id"}
        StackifyAPM(self.app)

        res = self.app.test_client().get('/')

        assert "Csome_id" not in res.headers.get('X-StackifyID')
        assert "CDsome_id" in res.headers.get('X-StackifyID')

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_stackify_header_should_contain_client_and_device_id(self, get_property_info_mock):
        get_property_info_mock.return_value = {"deviceId": "some_id", "clientId": "some_id"}
        StackifyAPM(self.app)

        res = self.app.test_client().get('/')

        assert "Csome_id" in res.headers.get('X-StackifyID')
        assert "CDsome_id" in res.headers.get('X-StackifyID')

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_get_client_property_call(self, get_property_info_mock):
        get_property_info_mock.return_value = {"deviceId": "some_id", "clientId": "some_id"}
        StackifyAPM(self.app)

        # do multiple requests
        self.app.test_client().get('/')
        self.app.test_client().get('/')
        res = self.app.test_client().get('/')

        assert get_property_info_mock.call_count == 1
        assert "Csome_id" in res.headers.get('X-StackifyID')
        assert "CDsome_id" in res.headers.get('X-StackifyID')

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_get_client_property_call_fallback(self, get_property_info_mock):
        get_property_info_mock.side_effect = [
            {},  # first get_properties call making sure property is empty
            {"deviceId": "some_id", "clientId": "some_id"},  # second get_properties call
        ]
        StackifyAPM(self.app)

        # do multiple requests
        self.app.test_client().get('/')
        self.app.test_client().get('/')
        res = self.app.test_client().get('/')

        assert get_property_info_mock.call_count == 2
        assert "Csome_id" in res.headers.get('X-StackifyID')
        assert "CDsome_id" in res.headers.get('X-StackifyID')


class RumInjectionTest(TestCase):
    def set_up_flask_app(self, rum_enabled=False, rum_auto=False):

        self.setup_logging = mock.patch('stackifyapm.conf.setup_logging')
        self.setup_logging.start()

        self.app = Flask('asfadsa')
        self.app.config['ENV'] = 'test'
        self.app.config['RUM_ENABLED'] = rum_enabled
        self.app.config['RUM_AUTO_INJECTION'] = rum_auto

        @self.app.route('/rum', methods=['GET'])
        def rum():
            return render_template_string("<html><head>{{stackifyapm_inject_rum | safe }}</head></html>")

        @self.app.route('/rum_auto', methods=['GET'])
        def rum_auto():
            return render_template_string("<html><head></head></html>")

    def tearDown(self):
        control.uninstrument()
        self.setup_logging.stop()

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_rum_injection(self, get_property_info_mock):
        self.set_up_flask_app()
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}
        StackifyAPM(self.app)

        res = self.app.test_client().get('/rum')

        assert '<script src="{}"'.format(RUM_SCRIPT_SRC) in str(res.data)
        assert '</script>' in str(res.data)
        assert 'data-host="Client Rum Domain"' in str(res.data)
        assert '|CClient ID|CDDevice ID"' in str(res.data)

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_rum_auto_injection(self, get_property_info_mock):
        self.set_up_flask_app(rum_auto=True)
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}
        StackifyAPM(self.app)

        res = self.app.test_client().get('/rum_auto')

        assert '<script src="{}"'.format(RUM_SCRIPT_SRC) in str(res.data)
        assert '</script>' in str(res.data)
        assert 'data-host="Client Rum Domain"' in str(res.data)
        assert '|CClient ID|CDDevice ID"' in str(res.data)

    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_rum_cookie(self, get_property_info_mock):
        self.set_up_flask_app(rum_enabled=True, rum_auto=True)
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}
        StackifyAPM(self.app)

        res = self.app.test_client().get('/rum_auto')
        cookies = [header for header in res.headers if header[0] == 'Set-Cookie' and RUM_COOKIE_NAME in header[1]]

        assert "Path=/" in cookies[0][1]
        assert any(cookies)

    @mock.patch('stackifyapm.base.Client.queue')
    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_rum_trace_property_should_true(self, get_property_info_mock, mock_queue):
        self.set_up_flask_app(rum_enabled=True, rum_auto=True)
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}
        StackifyAPM(self.app)

        res = self.app.test_client().get('/rum_auto')
        cookies = [header for header in res.headers if header[0] == 'Set-Cookie' and RUM_COOKIE_NAME in header[1]]

        assert any(cookies)
        assert mock_queue.called
        assert mock_queue.call_args_list[0][0][0].get_context().get('rum')

    @mock.patch('stackifyapm.base.Client.queue')
    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_rum_trace_property_should_false(self, get_property_info_mock, mock_queue):
        self.set_up_flask_app(rum_enabled=False, rum_auto=False)
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}
        StackifyAPM(self.app)

        res = self.app.test_client().get('/rum_auto')
        cookies = [header for header in res.headers if header[0] == 'Set-Cookie' and RUM_COOKIE_NAME in header[1]]

        assert not any(cookies)
        assert mock_queue.called
        assert not mock_queue.call_args_list[0][0][0].get_context().get('rum')


class TestPrefixInstrumentation(TestCase):
    def setUp(self):
        self.setup_logging = mock.patch('stackifyapm.conf.setup_logging')
        self.setup_logging.start()

        self.app = Flask('test')
        self.app.config['APPLICATION_NAME'] = 'test'
        self.app.config['ENVIRONMENT'] = 'test'
        self.app.config['PREFIX_ENABLED'] = True

        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            return jsonify(result='index')

        @self.app.route('/exception', methods=['GET', 'POST'])
        def exception():
            1 / 0
            return make_response(jsonify({'data': 'test'}), 400)

        @self.app.route('/template', methods=['GET', 'POST'])
        def template():
            return render_template_string("<html><head>Test</head></html>")

    def tearDown(self):
        control.uninstrument()
        self.setup_logging.stop()

    @mock.patch('stackifyapm.base.Client.queue')
    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_prefix_data(self, get_property_info_mock, queue_mock):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}
        StackifyAPM(self.app)

        self.app.test_client().post('/', data=json.dumps({"foo": "bar"}), headers={"Content-Type": "x-test"})

        assert queue_mock.called
        transaction_dict = queue_mock.call_args_list[0][0][0].to_dict()

        assert '{"result":"index"}' in transaction_dict.get('props', {}).get('PREFIX_RESPONSE_BODY')
        assert '19' == transaction_dict.get('props', {}).get('PREFIX_RESPONSE_SIZE_BYTES')
        assert 'application/json' in transaction_dict.get('props', {}).get('PREFIX_RESPONSE_HEADERS')
        assert '{"foo": "bar"}' == transaction_dict.get('props', {}).get('PREFIX_REQUEST_BODY')
        assert '14' == transaction_dict.get('props', {}).get('PREFIX_REQUEST_SIZE_BYTES')
        assert 'x-test' in transaction_dict.get('props', {}).get('PREFIX_REQUEST_HEADERS')

    @mock.patch('stackifyapm.base.Client.queue')
    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_prefix_data_with_exception(self, get_property_info_mock, queue_mock):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}
        StackifyAPM(self.app)

        self.app.test_client().post('/exception', data=json.dumps({"foo": "bar"}), headers={"Content-Type": "x-test"})

        assert queue_mock.called
        transaction_dict = queue_mock.call_args_list[0][0][0].to_dict()

        assert not transaction_dict.get('props', {}).get('PREFIX_RESPONSE_BODY')
        assert not transaction_dict.get('props', {}).get('PREFIX_RESPONSE_SIZE_BYTES')
        assert not transaction_dict.get('props', {}).get('PREFIX_RESPONSE_HEADERS')
        assert '{"foo": "bar"}' == transaction_dict.get('props', {}).get('PREFIX_REQUEST_BODY')
        assert '14' == transaction_dict.get('props', {}).get('PREFIX_REQUEST_SIZE_BYTES')
        assert 'x-test' in transaction_dict.get('props', {}).get('PREFIX_REQUEST_HEADERS')

    @mock.patch('stackifyapm.base.Client.queue')
    @mock.patch('stackifyapm.base.Client.get_property_info')
    def test_prefix_data_with_template(self, get_property_info_mock, queue_mock):
        get_property_info_mock.return_value = {"deviceId": "Device ID", "clientId": "Client ID", "clientRumDomain": "Client Rum Domain"}
        StackifyAPM(self.app)

        self.app.test_client().post('/template', data=json.dumps({"foo": "bar"}), headers={"Content-Type": "x-test"})

        assert queue_mock.called
        transaction_dict = queue_mock.call_args_list[0][0][0].to_dict()

        assert '<html><head>Test</head></html>' in transaction_dict.get('props', {}).get('PREFIX_RESPONSE_BODY')
        assert '30' == transaction_dict.get('props', {}).get('PREFIX_RESPONSE_SIZE_BYTES')
        assert 'text/html' in transaction_dict.get('props', {}).get('PREFIX_RESPONSE_HEADERS')
        assert '{"foo": "bar"}' == transaction_dict.get('props', {}).get('PREFIX_REQUEST_BODY')
        assert '14' == transaction_dict.get('props', {}).get('PREFIX_REQUEST_SIZE_BYTES')
        assert 'x-test' in transaction_dict.get('props', {}).get('PREFIX_REQUEST_HEADERS')
