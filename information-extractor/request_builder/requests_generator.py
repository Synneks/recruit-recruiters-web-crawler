from request_builder.request_builder import RequestBuilder


class RequestsGenerator:
    @staticmethod
    def generate_requests(technology, location):
        requests = []

        for page in range(1, 8):
            requests.append(RequestBuilder().title(technology.strip('\n').lower()).location(location).page(page).build())

        return requests
