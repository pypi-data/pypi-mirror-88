from .certificate_kinds import CertificateKinds
from .certificate_parameters import CertificateParameters


class CreateOrderRequest(object):

    def __init__(self):
        self.__ca_id = None
        self.__template_id = None
        self.__kind = None
        self.__copy_to_certificate = None
        self.__parameters = None
        self.__validity_end = None

    @property
    def ca_id(self):
        return self.__ca_id

    @ca_id.setter
    def ca_id(self, value):
        self.__ca_id = value

    @property
    def template_id(self):
        return self.__template_id

    @template_id.setter
    def template_id(self, value):
        self.__template_id = value

    @property
    def kind(self):
        return self.__kind

    @kind.setter
    def kind(self, value):
        self.__kind = value

    @property
    def copy_to_certificate(self):
        return self.__copy_to_certificate

    @copy_to_certificate.setter
    def copy_to_certificate(self, value):
        self.__copy_to_certificate = value

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__parameters = value

    @property
    def validity_end(self):
        return self.__validity_end

    @validity_end.setter
    def validity_end(self, value):
        self.__validity_end = value

    def to_model(self):
        if self.__parameters is None:
            raise Exception('The "parameters" field was not set')

        if not isinstance(self.__parameters, CertificateParameters):
            raise Exception('Unsupported type for "parameters" on model for CreateOrderRequest: {0}'
                            .format(type(self.__parameters)))

        if self.__kind != CertificateKinds.PUBLIC_KEY and self.__kind != CertificateKinds.ATTRIBUTE:
            raise Exception('Unsupported "kind" field on model for CreateOrderRequest: {0}'.format(self.__kind))

        return {
            'caId': self.__ca_id,
            'templateId': self.__template_id,
            'kind': self.__kind,
            'copyToCertificate': self.__copy_to_certificate,
            'parameters': self.__parameters.to_model() if (self.__parameters is not None) else None,
            'validityEnd': self.__validity_end
        }


__all__ = ['CreateOrderRequest']
