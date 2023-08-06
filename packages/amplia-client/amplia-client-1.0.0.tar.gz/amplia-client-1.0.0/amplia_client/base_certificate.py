from .name import Name


class BaseCertificate(object):

    def __init__(self, model):
        self.__id = model.get('id', None)
        self.__ca_id = model.get('caId', None)
        self.__alias = model.get('alias', None)
        self.__serial_number = model.get('serialNumber', None)
        self.__content_base64 = model.get('content', None)
        self.__kind = model.get('kind', None)
        self.__format = model.get('format', None)

        self.__subject_name = None
        self.__email_address = None
        self.__issuer_name = None
        self.__validity_start = None
        self.__validity_end = None
        self.__crl_distribution_points = None
        self.__ocsp_uris = None
        if model.get('info', None) is not None:
            self.__email_address = model.get('info').get('emailAddress', None)
            self.__validity_start = model.get('info').get('validityStart', None)
            self.__validity_end = model.get('info').get('validityEnd', None)
            self.__crl_distribution_points = model.get('info').get('crlDistributionPoints', None)
            self.__ocsp_uris = model.get('info').get('ocspUris', None)

            if model.get('info').get('subjectName', None) is not None:
                self.__subject_name = Name(model.get('info').get('subjectName'))

            if model.get('info').get('issuerName', None) is not None:
                self.__issuer_name = Name(model.get('info').get('issuerName'))

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
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, value):
        self.__alias = value

    @property
    def subject_name(self):
        return self.__subject_name

    @subject_name.setter
    def subject_name(self, value):
        self.__subject_name = value

    @property
    def email_address(self):
        return self.__email_address

    @email_address.setter
    def email_address(self, value):
        self.__email_address = value

    @property
    def issuer_name(self):
        return self.__issuer_name

    @issuer_name.setter
    def issuer_name(self, value):
        self.__issuer_name = value

    @property
    def validity_start(self):
        return self.__validity_start

    @validity_start.setter
    def validity_start(self, value):
        self.__validity_start = value

    @property
    def validity_end(self):
        return self.__validity_end

    @validity_end.setter
    def validity_end(self, value):
        self.__validity_end = value

    @property
    def crl_distribution_points(self):
        return self.__crl_distribution_points

    @crl_distribution_points.setter
    def crl_distribution_points(self, value):
        self.__crl_distribution_points = value

    @property
    def ocsp_uris(self):
        return self.__ocsp_uris

    @ocsp_uris.setter
    def ocsp_uris(self, value):
        self.__ocsp_uris = value

    @property
    def serial_number(self):
        return self.__serial_number

    @serial_number.setter
    def serial_number(self, value):
        self.__serial_number = value

    @property
    def content_base64(self):
        return self.__content_base64

    @content_base64.setter
    def content_base64(self, value):
        self.__content_base64 = value

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

    def to_model(self):
        return {
            'id': self.__id,
            'caId': self.__ca_id,
            'alias': self.__alias,
            'subjectName': self.__subject_name.to_model() if (self.__subject_name is not None) else None,
            'emailAddress': self.__email_address,
            'issuerName': self.__issuer_name.to_model() if (self.__issuer_name is not None) else None,
            'serialNumber': self.__serial_number,
            'validityStart': self.__validity_start,
            'validityEnd': self.__validity_end,
            'crlDistributionPoints': self.__crl_distribution_points,
            'ocspUris': self.__ocsp_uris,
            'content': self.__content_base64,
            'kind': self.__kind,
            'format': self.__format
        }


__all__ = ['BaseCertificate']
