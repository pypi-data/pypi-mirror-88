class IssueCertificateRequest(object):

    def __init__(self):
        self.__order_id = None
        self.__csr = None

    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        self.__order_id = value

    @property
    def csr(self):
        return self.__csr

    @csr.setter
    def csr(self, value):
        self.__csr = value

    def to_model(self):
        return {
            'orderId': self.__order_id if self.__order_id is not None else '00000000-0000-0000-0000-000000000000',
            'csr': self.__csr
        }


__all__ = ['IssueCertificateRequest']
