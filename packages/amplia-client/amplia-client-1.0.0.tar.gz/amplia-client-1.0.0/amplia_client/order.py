from .certificate_parameters import CertificateParameters
from .base_order import BaseOrder


class Order(BaseOrder):

    def __init__(self, model=None):
        BaseOrder.__init__(self, model)

        self.__parameters = None

        if model is not None:
            if model.get('parameters', None) is not None:
                self.__parameters = CertificateParameters.decode(model.get('parameters', None))

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__parameters = value

    def to_model(self):
        if not isinstance(self.__parameters, CertificateParameters):
            raise Exception('Unsupported type for "parameters" on model for Order: {0}'
                            .format(type(self.__parameters)))

        model = super(Order, self).to_model()
        model['parameters'] = self.__parameters.to_model() if (self.__parameters is not None) else None
        return model


__all__ = ['Order']
