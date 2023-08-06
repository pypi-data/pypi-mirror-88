from unittest import mock
import json

from citibox.gcloudlogger.src.gcloud_formatter import GCloudFormatter
from citibox.gcloudlogger.contrib.falcon import FalconMiddleware
from citibox.gcloudlogger.test_helpers.logger_test_case import LoggerTestCase


class EmptyResource:
    pass


@mock.patch('citibox.gcloudlogger.contrib.falcon.middleware.falcon_middleware.Response')
@mock.patch('citibox.gcloudlogger.contrib.falcon.middleware.falcon_middleware.Request')
class TestFalconMiddleware(LoggerTestCase):
    logger = None
    _formatter = GCloudFormatter
    logger_name = __name__

    def test_process_request_get_http(self, request_mock, response_mock):
        falcon_middleware = FalconMiddleware()
        request_mock.method = "GET"
        request_mock.host = "PYTEST"
        request_mock.path = "/test_path"
        request_mock.headers = {"header-a": "A"}
        request_mock.params = {"parameter_1": "1"}

        response_mock.body = {"status": "ok"}
        response_mock.status = "200 Ok"

        falcon_middleware.process_response(request_mock, response_mock, EmptyResource(), True)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("1", last_log.get('request').get("params").get("parameter_1"))
        self.assertEquals("A", last_log.get('request').get("headers").get("header-a"))
        self.assertEquals(response_mock.body, last_log.get("response").get("body"))

    def test_process_request_post_http(self, request_mock, response_mock):
        falcon_middleware = FalconMiddleware()
        request_mock.method = "POST"
        request_mock.host = "PYTEST_POST"
        request_mock.path = "/test_path"
        request_mock.headers = {"header-a": "A"}
        request_mock.media = {"parameter_1": "1"}

        response_mock.body = {"status": "ok"}
        response_mock.status = "200 Ok"
        falcon_middleware.process_response(request_mock, response_mock, EmptyResource(), True)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("body", last_log.get('request'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("1", last_log.get('request').get("body").get("parameter_1"))
        self.assertEquals("A", last_log.get('request').get("headers").get("header-a"))
        self.assertEquals(response_mock.body, last_log.get("response").get('body'))

    def test_process_request_post_pubsub(self, request_mock, response_mock):
        falcon_middleware = FalconMiddleware()
        request_mock.method = "POST"
        request_mock.host = "PYTEST"
        request_mock.path = "/test_path"
        request_mock.headers = {"header-a": "A"}
        request_mock.user_agent = FalconMiddleware.PUBSUB_USER_AGENT
        request_mock.media = {"message": {"attributes": {"attr_1": "AA"}}}

        response_mock.body = {"status": "ok"}
        response_mock.status = "200 Ok"

        falcon_middleware.process_response(request_mock, response_mock, EmptyResource(), True)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("A", last_log.get('request').get("headers").get("header-a"))
        self.assertEquals("AA", last_log.get('attr_1'))

