from .order_status import OrderStatus


class BaseOrder(object):

    def __init__(self, model=None):
        self.__id = None
        self.__ca_id = None
        self.__template_id = None
        self.__alias = None
        self.__email_address = None
        self.__certificate_id = None
        self.__status = None

        if model is not None:
            self.__id = model.get('id', None)
            self.__ca_id = model.get('caId', None)
            self.__template_id = model.get('templateId', None)
            self.__alias = model.get('alias', None)
            self.__email_address = model.get('emailAddress', None)
            self.__certificate_id = model.get('certificateId', None)
            self.__status = model.get('status', None)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

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
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, value):
        self.__alias = value

    @property
    def email_address(self):
        return self.__email_address

    @email_address.setter
    def email_address(self, value):
        self.__email_address = value

    @property
    def certificate_id(self):
        return self.__certificate_id

    @certificate_id.setter
    def certificate_id(self, value):
        self.__certificate_id = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    def to_model(self):
        if self.__status != OrderStatus.PENDING \
                and self.__status != OrderStatus.LOCKED \
                and self.__status != OrderStatus.ISSUED:
            raise Exception('Unsupported "status" field on model for BaseOrder: {0}'.format(self.__status))

        return {
            'id': self.__id,
            'caId': self.__ca_id,
            'templateId': self.__template_id,
            'alias': self.__alias,
            'emailAddress': self.__email_address,
            'certificateId': self.__certificate_id,
            'status': self.__status,
        }


__all__ = ['BaseOrder']
