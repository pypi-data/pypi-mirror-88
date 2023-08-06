import requests

from .certificate import Certificate
from .certificate_formats import CertificateFormats
from .certificate_summary import CertificateSummary
from .issue_certificate_request import IssueCertificateRequest
from .paginated_search_params import PaginatedSearchParams
from .paginated_search_response import PaginatedSearchResponse
from .rest_client import RestClient
from .order import Order

TYPED_API_ROUTES = {
    CertificateFormats.PKI_BRAZIL: 'pki-brazil',
    CertificateFormats.SSL: 'ssl',
    CertificateFormats.CNB: 'cnb',
    CertificateFormats.CIE: 'cie',
    CertificateFormats.ARISP: 'arisp',
}


class AmpliaClient(object):

    def __init__(self, endpoint, api_key):
        self.__endpoint = endpoint
        self.__api_key = api_key
        self.__rest_client = None

    def __get_rest_client(self):
        if self.__rest_client is None:
            self.__rest_client = RestClient(self.__endpoint, self.__api_key)
        return self.__rest_client

    def create_order(self, request):
        if request is None:
            raise Exception('The request was not set')
        if request.parameters is None:
            raise Exception('The "parameters" field cannot be null')
        client = self.__get_rest_client()

        type_route_segment = AmpliaClient.__get_typed_route_segment(request.parameters.format)
        model = client.post('/api/orders/{0}'.format(type_route_segment), request)
        return Order(model)

    def get_order(self, order_id):
        if order_id is None:
            raise Exception('The order_id was not set')
        client = self.__get_rest_client()

        model = client.get('/api/v2/orders/{0}'.format(order_id))
        return Order(model)

    def get_order_issue_link(self, order_id, result_url=None):
        if order_id is None:
            raise Exception('The order_id was not set')
        client = self.__get_rest_client()

        url = "/api/orders/{0}/issue-link".format(order_id)
        if result_url is not None:
            encoded_url = requests.compat.quote_plus(result_url)
            url += "?returnUrl={0}".format(encoded_url)

        return client.get(url)

    def delete_order(self, order_id):
        if order_id is None:
            raise Exception('The order_id was not set')
        client = self.__get_rest_client()
        client.delete("/api/orders/{0}".format(order_id))

    def issue_certificate(self, order_id, csr):
        client = self.__get_rest_client()
        request = IssueCertificateRequest()
        request.order_id = order_id
        request.csr = csr

        model = client.post("/api/v2/certificates", request)
        return Certificate(model)

    def list_certificates(self, search_params=None, valid_only=False):
        if search_params is not None and not isinstance(search_params, PaginatedSearchParams):
            raise Exception('The "search_params" parameter is not a instance of the PaginatedSearchParams class')
        client = self.__get_rest_client()

        url = AmpliaClient.__set_paginated_search_params(
            '/api/v2/certificates',
            search_params if (search_params is not None) else PaginatedSearchParams()
        ) + "&validOnly=" + "true" if valid_only else "false"

        model = client.get(url)
        return PaginatedSearchResponse(model, CertificateSummary)

    def get_certificate(self, certificate_id, fill_content=False):
        if certificate_id is None:
            raise Exception('The certificate_id was not set')
        client = self.__get_rest_client()

        model = client.get('/api/v2/certificates/{0}?fillContent='.format(certificate_id)
                           + 'true' if fill_content else 'false')
        return Certificate(model)

    def revoke_certificate(self, certificate_id):
        if certificate_id is None:
            raise Exception('The certificate_id was not set')
        client = self.__get_rest_client()

        client.delete("/api/certificates/{0}".format(certificate_id))

    @staticmethod
    def __set_paginated_search_params(original_uri, search_params):
        return "{0}?q={1}&limit={2}&offset={3}&order={4}".format(
            original_uri,
            requests.compat.quote_plus(search_params.q),
            search_params.limit,
            search_params.offset,
            search_params.order,
        )

    @staticmethod
    def __get_typed_route_segment(cert_format):
        if cert_format in TYPED_API_ROUTES:
            return TYPED_API_ROUTES[cert_format]
        raise Exception('Certificate format not supported'.format(cert_format))

    @property
    def endpoint(self):
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, value):
        self.__endpoint = value

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, value):
        self.__api_key = value


__all__ = [
    'AmpliaClient'
]
