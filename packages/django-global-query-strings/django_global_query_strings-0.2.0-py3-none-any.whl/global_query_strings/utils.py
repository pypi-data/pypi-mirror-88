from bs4 import BeautifulSoup
from urllib.parse import urlencode, parse_qs, urlsplit, urlunsplit

from django.conf import settings

GLOBAL_QUERY_STRINGS_IGNORE_URLS = getattr(
    settings, "GLOBAL_QUERY_STRINGS_IGNORE_URLS", []
)
GLOBAL_QUERY_STRINGS_IGNORE_RELATIVE_PATHS = getattr(
    settings, "GLOBAL_QUERY_STRINGS_IGNORE_RELATIVE_PATHS", False
)
GLOBAL_QUERY_STRINGS_PARAMS = getattr(settings, "GLOBAL_QUERY_STRINGS_PARAMS", {})


def add_query_strings_to_links(html_content):
    """
    Given a html content, add some query string to all the a tags.
    Urls and domain names found in GLOBAL_QUERY_STRING_EXCLUSIONS will be ignored.
    If GLOBAL_QUERY_STRING_IGNORE_RELATIVE_PATHS is set to True all relatives path will be ignored
    """
    soup = BeautifulSoup(html_content, "html.parser")

    for link in soup.find_all("a"):
        # Some 'a' tag might not have an href (e.g.: data-href)
        if not link.has_attr("href"):
            continue

        to_exclude = any(
            excluded in link["href"] for excluded in GLOBAL_QUERY_STRINGS_IGNORE_URLS
        )
        exclude_relative_path = (
            "http" not in link["href"]
            if GLOBAL_QUERY_STRINGS_IGNORE_RELATIVE_PATHS
            else False
        )

        if not to_exclude and not exclude_relative_path:
            link["href"] = _set_query_parameters(
                link["href"], GLOBAL_QUERY_STRINGS_PARAMS
            )

    return str(soup)


def _set_query_parameters(url, params_dict):
    """
    Given a URL, set or replace a query parameter and return the
    modified URL.

    set_query_parameter('http://example.com?foo=bar&biz=baz', {'foo': 'stuff'})
    'http://example.com?foo=stuff&biz=baz'

    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    for param_key, param_value in params_dict.items():
        query_params[param_key] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
