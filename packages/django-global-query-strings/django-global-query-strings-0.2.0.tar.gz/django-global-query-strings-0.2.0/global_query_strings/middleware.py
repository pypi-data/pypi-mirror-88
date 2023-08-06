from .utils import add_query_strings_to_links


class GlobalQueryStringsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            "Content-Type" in response and "text/html" in response["Content-Type"]
        ):
            response.content = add_query_strings_to_links(response.content)

        return response
