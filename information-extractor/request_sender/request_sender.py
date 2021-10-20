import requests


class RequestSender:
    @staticmethod
    def send_get_request(url):
        return requests.get(url)

    @staticmethod
    def send_multiple_get_requests(requests):
        ret_list = []

        for request in requests:
            ret_list.append(RequestSender.send_get_request(request))

        return ret_list
