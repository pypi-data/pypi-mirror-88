from .base_certificate import BaseCertificate
from .certificate_parameters import CertificateParameters


class Certificate(BaseCertificate):

    def __init__(self, model):
        BaseCertificate.__init__(self, model)

        if model.get('parameters', None) is not None:
            self.__parameters = CertificateParameters.decode(model.get('parameters', None))

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__parameters = value

    def to_model(self):
        model = super(Certificate, self).to_model()
        model['parameters'] = self.__parameters.to_model() if (self.__parameters is not None) else None
        return model


__all__ = ['Certificate']
