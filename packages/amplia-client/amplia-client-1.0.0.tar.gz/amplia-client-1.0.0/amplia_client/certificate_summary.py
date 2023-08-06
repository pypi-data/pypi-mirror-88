class CertificateSummary(object):

    def __init__(self, model):
        self.__id = model.get('id', None)
        self.__subscription_id = model.get('subscriptionId', None)
        self.__ca_id = model.get('caId', None)
        self.__key_id = model.get('keyId', None)
        self.__date_issued = model.get('dateIssued', None)
        self.__date_expires = model.get('dateExpires', None)
        self.__date_revoked = model.get('dateRevoked', None)
        self.__alias = model.get('alias', None)
        self.__subject_display_name = model.get('subjectDisplayName', None)
        self.__serial_number = model.get('serialNumber', None)
        self.__is_ca = model.get('isCA', None)
        self.__kind = model.get('kind', None)
        self.__format = model.get('format', None)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def subscription_id(self):
        return self.__subscription_id

    @subscription_id.setter
    def subscription_id(self, value):
        self.__subscription_id = value

    @property
    def ca_id(self):
        return self.__ca_id

    @ca_id.setter
    def ca_id(self, value):
        self.__ca_id = value

    @property
    def key_id(self):
        return self.__key_id

    @key_id.setter
    def key_id(self, value):
        self.__key_id = value

    @property
    def date_issued(self):
        return self.__date_issued

    @date_issued.setter
    def date_issued(self, value):
        self.__date_issued = value

    @property
    def date_expires(self):
        return self.__date_expires

    @date_expires.setter
    def date_expires(self, value):
        self.__date_expires = value

    @property
    def date_revoked(self):
        return self.__date_revoked

    @date_revoked.setter
    def date_revoked(self, value):
        self.__date_revoked = value

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, value):
        self.__alias = value

    @property
    def subject_display_name(self):
        return self.__subject_display_name

    @subject_display_name.setter
    def subject_display_name(self, value):
        self.__subject_display_name = value

    @property
    def serial_number(self):
        return self.__serial_number

    @serial_number.setter
    def serial_number(self, value):
        self.__serial_number = value

    @property
    def is_ca(self):
        return self.__is_ca

    @is_ca.setter
    def is_ca(self, value):
        self.__is_ca = value

    @property
    def is_ca(self):
        return self.__is_ca

    @is_ca.setter
    def is_ca(self, value):
        self.__is_ca = value

    @property
    def kind(self):
        return self.__kind

    @kind.setter
    def kind(self, value):
        self.__kind = value

    @property
    def format(self):
        return self.__format

    @format.setter
    def format(self, value):
        self.__format = value


__all__ = ['CertificateSummary']
