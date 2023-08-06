from __future__ import absolute_import

import flask
import logging
import sys
from flask import request, signals

import stackifyapm
import stackifyapm.instrumentation.control
from stackifyapm.base import Client
from stackifyapm.conf import constants
from stackifyapm.contrib.flask.utils import get_data_from_request, get_data_from_response, get_data_from_exception
from stackifyapm.decorators import exception_handler
from stackifyapm.utils.helper import get_stackify_header
from stackifyapm.utils import build_name_with_http_method_prefix
from stackifyapm.utils.disttracing import TraceParent
from stackifyapm.utils.helper import can_insert_script
from stackifyapm.utils.helper import get_rum_script_or_none
from stackifyapm.handlers.exceptions import get_exception_context
from stackifyapm.traces import execution_context
from stackifyapm.utils.helper import get_main_file

logger = logging.getLogger("stackifyapm.traces")


def make_client(app, **defaults):
    config = app.config.get("STACKIFY_APM", {})
    defaults.update(app.config)

    instrument_all_exclude = defaults.get('INSTRUMENT_ALL_EXCLUDE', "")
    excludes = instrument_all_exclude and instrument_all_exclude.split(',') or []
    excludes.append(get_main_file())
    defaults["INSTRUMENT_ALL_EXCLUDE"] = ','.join(excludes)

    if not app.config.get("BASE_DIR"):
        defaults["BASE_DIR"] = app.config.root_path

    if "framework_name" not in defaults:
        defaults["framework_name"] = "flask"
        defaults["framework_version"] = getattr(flask, "__version__", "<0.7")

    return Client(config, **defaults)


class StackifyAPM(object):
    """
    Flask application for StackifyAPM.
    """
    @exception_handler(message="Error creating flask StackifyAPM")
    def __init__(self, app=None, **defaults):
        self.app = app
        self.logging = logging
        self.client = None

        if app:
            self.init_app(app, **defaults)

    def init_app(self, app, **defaults):
        self.app = app

        if not self.client:
            self.client = make_client(app, **defaults)

        signals.got_request_exception.connect(self.handle_exception, sender=app, weak=False)

        try:
            from stackifyapm.contrib.celery import register_exception_tracking

            register_exception_tracking(self.client)
        except ImportError:
            pass

        # Instrument to get spans
        if self.client.config.instrument:
            stackifyapm.instrumentation.control.instrument(client=self.client)

            signals.request_started.connect(self.request_started, sender=app)
            signals.request_finished.connect(self.request_finished, sender=app)

            try:
                from stackifyapm.contrib.celery import register_instrumentation

                register_instrumentation(self.client)
            except ImportError:
                pass
        else:
            logger.debug("Skipping instrumentation. INSTRUMENT is set to False.")

        @app.context_processor
        def rum_tracing():
            if self.client.config.rum_auto_injection:
                return {}

            transaction = execution_context.get_transaction()
            rum_script = get_rum_script_or_none(transaction)
            if rum_script:
                return {
                    "stackifyapm_inject_rum": rum_script
                }
            return {}

    def request_started(self, app, **kwargs):
        if constants.TRACEPARENT_HEADER_NAME in request.headers:
            trace_parent = TraceParent.from_string(request.headers[constants.TRACEPARENT_HEADER_NAME])
        else:
            trace_parent = None

        self.client.begin_transaction("request", trace_parent=trace_parent, client=self.client)

    def request_finished(self, app, response, **kwargs):
        transaction = execution_context.get_transaction()

        rule = request.url_rule.rule if request.url_rule is not None else ""
        rule = build_name_with_http_method_prefix(rule, request)
        stackifyapm.set_transaction_context(
            lambda: get_data_from_request(request, capture_body=self.client.config.prefix_enabled),
            "request",
        )
        stackifyapm.set_transaction_context(
            lambda: get_data_from_response(response, capture_body=self.client.config.prefix_enabled),
            "response"
        )
        stackifyapm.set_transaction_name(rule, override=False)

        response.headers["X-StackifyID"] = get_stackify_header(transaction)

        if self.client.config.rum_enabled:
            stackifyapm.set_transaction_context(lambda: True, "rum")
            # adding RUM Cookie
            response.set_cookie(
                constants.RUM_COOKIE_NAME,
                str(transaction.get_trace_parent().trace_id),
            )

        if self.client.config.rum_auto_injection:
            rum_script = get_rum_script_or_none(transaction)
            data = response.get_data()
            if rum_script and can_insert_script(data):
                data = data.replace(str.encode('</head>'), str.encode('{}</head>'.format(rum_script)))
                response.set_data(data)

        self.client.end_transaction()

    def handle_exception(self, app, **kwargs):
        if not self.client:
            return

        exc_info = sys.exc_info()
        if exc_info:
            exception = exc_info[1]
            traceback = exc_info[2]
        else:
            return

        rule = request.url_rule.rule if request.url_rule is not None else ""
        rule = build_name_with_http_method_prefix(rule, request)
        stackifyapm.set_transaction_context(
            lambda: get_data_from_request(request, capture_body=self.client.config.prefix_enabled),
            "request",
        )
        stackifyapm.set_transaction_context(lambda: get_data_from_exception(), "response")
        stackifyapm.set_transaction_name(rule, override=False)

        self.client.capture_exception(
            exception=get_exception_context(exception, traceback)
        )
        self.client.end_transaction()

    def capture_exception(self, *args, **kwargs):
        assert self.client, "capture_exception called before application configured"
        return self.client.capture_exception(*args, **kwargs)
