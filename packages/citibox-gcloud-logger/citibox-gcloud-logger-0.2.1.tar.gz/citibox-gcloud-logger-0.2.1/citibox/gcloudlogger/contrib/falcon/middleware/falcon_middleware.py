import logging
import time

from falcon import Request, Response


class FalconMiddleware:
    PUBSUB_USER_AGENT = "CloudPubSub-Google"

    def __init__(self):
        self._logger = logging.getLogger()

    def _get_request_details(self, req: Request):
        method = req.method
        query_details = {
            "host": req.host,
            "path": req.path,
            "request": {
                "method": method,
                "headers": req.headers
            }
        }

        if method in ("GET", "DELETE"):
            query_details["request"].update({"params": req.params})
        elif method in ("POST", "PUT", "PATCH"):
            query_details["request"].update({"body": req.media})
            if req.user_agent == self.PUBSUB_USER_AGENT:
                try:
                    [query_details.update({k: v}) for k, v in req.media['message']['attributes'].items()]
                except KeyError as e:  # pragma nocover
                    self._logger.warning(f'Cannot load pubsub message attributes')

        return query_details

    @staticmethod
    def _get_current_timestamp():
        return int(round(time.time() * 1000))

    def process_request(self, req: Request, resp: Response):
        """

        :param req: falcon.Request
        :param resp: falcon.Response
        :return:
        """
        req.context.started_at = self._get_current_timestamp()

    def process_response(self, req: Request, resp: Response, resource, req_succeeded: bool):
        """

        :param req: falcon.Request
        :param resp: falcon.Response
        :param resource: Resource object
        :param req_succeeded: bool
        :return:
        """
        response_detail = self._get_request_details(req)
        response_detail["response"] = {
            "body": resp.body,
            "http_status": resp.status,
            "headers": resp.headers
        }
        response_detail.update({"duration": (self._get_current_timestamp() - req.context.started_at) / 1000})
        try:
            self._logger.info(
                f'{req.method} {resp.status} {req.path}',
                extra=response_detail
            )
        except Exception as e:  # pragma nocover
            pass
