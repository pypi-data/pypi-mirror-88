import re

from .arisp_roles import ArispRoles
from .certificate_formats import CertificateFormats


class CertificateParameters(object):

    def __init__(self, model=None):
        if model is not None:
            self._format = model.get('format', None)

    @staticmethod
    def decode(model):
        certificate_format = model.get('format', None)
        if certificate_format is None:
            raise Exception('Missing "format" field')

        if certificate_format == CertificateFormats.PKI_BRAZIL:
            return PkiBrazilCertificateParameters(model)
        elif certificate_format == CertificateFormats.SSL:
            return SslCertificateParameters(model)
        elif certificate_format == CertificateFormats.CNB:
            return CnbCertificateParameters(model)
        elif certificate_format == CertificateFormats.CNB_CA:
            return CnbCACertificateParameters(model)
        elif certificate_format == CertificateFormats.CIE:
            return CieCertificateParameters(model)
        elif certificate_format == CertificateFormats.ARISP:
            return ArispCertificateParameters(model)
        else:
            raise Exception('Certificate "format" field not supported on model for CertificateParameters: {0}'
                            .format(certificate_format))

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    def to_model(self):
        return {
            'format': self._format,
        }


class PkiBrazilCertificateParameters(CertificateParameters):

    def __init__(self, model=None):
        CertificateParameters.__init__(self, model)
        self._format = CertificateFormats.PKI_BRAZIL

        self.__name = None
        self.__email_address = None
        self.__cnpj = None
        self.__company_name = None
        self.__cpf = None
        self.__birth_date = None
        self.__oab_uf = None
        self.__oab_numero = None
        self.__rg_emissor = None
        self.__rg_emissor_uf = None
        self.__rg_numero = None
        self.__organization_units = None
        self.__organization = None
        self.__country = None
        self.__phone_number = None

        if model is not None:
            self.__name = model.get('nome', None)
            self.__email_address = model.get('emailAddress', None)
            self.__cnpj = model.get('cnpj', None)
            self.__company_name = model.get('companyName', None)
            self.__cpf = model.get('cpf', None)
            self.__birth_date = model.get('birthDate', None)
            self.__oab_uf = model.get('oabUF', None)
            self.__oab_numero = model.get('oabNumbero', None)
            self.__rg_emissor = model.get('rgEmissor', None)
            self.__rg_emissor_uf = model.get('rgEmissorUF', None)
            self.__rg_numero = model.get('rgNumero', None)
            self.__organization_units = model.get('organizationUnits', None)
            self.__organization = model.get('organization', None)
            self.__country = model.get('country', None)
            self.__phone_number = model.get('phoneNumber', None)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def email_address(self):
        return self.__email_address

    @email_address.setter
    def email_address(self, value):
        self.__email_address = value

    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, value):
        self.__cnpj = value

    @property
    def company_name(self):
        return self.__company_name

    @company_name.setter
    def company_name(self, value):
        self.__company_name = value

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, value):
        self.__cpf = value

    @property
    def birth_date(self):
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, value):
        self.__birth_date = value

    @property
    def oab_uf(self):
        return self.__oab_uf

    @oab_uf.setter
    def oab_uf(self, value):
        self.__oab_uf = value

    @property
    def oab_numero(self):
        return self.__oab_numero

    @oab_numero.setter
    def oab_numero(self, value):
        self.__oab_numero = value

    @property
    def rg_emissor(self):
        return self.__rg_emissor

    @rg_emissor.setter
    def rg_emissor(self, value):
        self.__rg_emissor = value

    @property
    def rg_emissor_uf(self):
        return self.__rg_emissor_uf

    @rg_emissor_uf.setter
    def rg_emissor_uf(self, value):
        self.__rg_emissor_uf = value

    @property
    def rg_numero(self):
        return self.__rg_numero

    @rg_numero.setter
    def rg_numero(self, value):
        self.__rg_numero = value

    @property
    def organization_units(self):
        return self.__organization_units

    @organization_units.setter
    def organization_units(self, value):
        self.__organization_units = value

    @property
    def organization(self):
        return self.__organization

    @organization.setter
    def organization(self, value):
        self.__organization = value

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, value):
        self.__country = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    def to_model(self):
        if self.__name is None:
            raise Exception('The "name" field was not set')

        if self.__cpf is None:
            raise Exception('The "cpf" field was not set')

        model = super(PkiBrazilCertificateParameters, self).to_model()
        model['name'] = self.__name
        model['emailAddress'] = self.__email_address
        model['cnpj'] = self.__cnpj
        model['companyName'] = self.__company_name
        model['cpf'] = self.__cpf
        model['birthDate'] = self.__birth_date
        model['oabUF'] = self.__oab_uf
        model['oabNumero'] = self.__oab_numero
        model['rgEmissor'] = self.__rg_emissor
        model['rgEmissorUF'] = self.__rg_emissor_uf
        model['rgNumero'] = self.__rg_numero
        model['organizationUnits'] = self.__organization_units
        model['organization'] = self.__organization
        model['country'] = self.__country
        model['phoneNumber'] = self.__phone_number
        return model


class ArispCertificateParameters(CertificateParameters):

    def __init__(self, model=None):
        CertificateParameters.__init__(self, model)
        self._format = CertificateFormats.ARISP

        self.__nome = None
        self.__cpf = None
        self.__funcao = None
        self.__cartorio = None

        if model is not None:
            self.__nome = model.get('nome', None)
            self.__cpf = model.get('cpf', None)
            self.__funcao = model.get('funcao', None)

            if model.get('cartorio', None) is not None:
                self.__cartorio = ArispCartorioInfo(model.get('cartorio', None))

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = value

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, value):
        self.__cpf = value

    @property
    def funcao(self):
        return self.__funcao

    @funcao.setter
    def funcao(self, value):
        self.__funcao = value

    @property
    def cartorio(self):
        return self.__cartorio

    @cartorio.setter
    def cartorio(self, value):
        self.__cartorio = value

    def to_model(self):
        if self.__nome is None:
            raise Exception('The "nome" field was not set')

        if self.__cpf is None:
            raise Exception('The "cpf" field was not set')

        if self.__cartorio is None:
            raise Exception('The "cartorio" was not set')

        if self.__funcao != ArispRoles.TABELIAO\
                and self.__funcao != ArispRoles.SUBSTITUTO\
                and self.__funcao != ArispRoles.ESCREVENTE:
            raise Exception('Unsupported "funcao" field on model for ArispCertificateParameters: {0}'
                            .format(self.__funcao))

        if self.__cartorio is not None and not (isinstance(self.__cartorio, ArispCartorioInfo)):
            raise Exception('Unsupported type for "cartorio" field on model for ArispCertificateParameters: {0}'
                            .format(type(self.__cartorio)))

        model = super(ArispCertificateParameters, self).to_model()
        model['nome'] = self.__nome
        model['cpf'] = self.__cpf
        model['funcao'] = self.__funcao
        model['cartorio'] = self.__cartorio.to_model() if (self.__cartorio is not None) else None
        return model


class ArispCartorioInfo(object):

    def __init__(self, model=None):
        self.__cns = None
        self.__numero = None
        self.__nome = None
        self.__oficial = None
        self.__telefone = None
        self.__site = None
        self.__email = None
        self.__endereco = None

        if model is not None:
            self.__cns = model.get('cns', None)
            self.__numero = model.get('numero', None)
            self.__nome = model.get('nome', None)
            self.__oficial = model.get('oficial', None)
            self.__telefone = model.get('telefone', None)
            self.__site = model.get('site', None)
            self.__email = model.get('email', None)

            if model.get('endereco', None) is not None:
                self.__endereco = ArispEndereco(model.get('endereco', None))

    @property
    def cns(self):
        return self.__cns

    @cns.setter
    def cns(self, value):
        self.__cns = value

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, value):
        self.__numero = value

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = value

    @property
    def oficial(self):
        return self.__oficial

    @oficial.setter
    def oficial(self, value):
        self.__oficial = value

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, value):
        self.__endereco = value

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, value):
        self.__telefone = value

    @property
    def site(self):
        return self.__site

    @site.setter
    def site(self, value):
        self.__site = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    def to_model(self):
        if self.__cns is None:
            raise Exception('The "cns" field was not set')

        if self.__nome is None:
            raise Exception('The "nome" field was not set')

        if self.__oficial is None:
            raise Exception('The "oficial" field was not set')

        if self.__endereco is not None and not (isinstance(self.__endereco, ArispEndereco)):
            raise Exception('Unsupported type for "endereco" field on model for ArispCartorioInfo: {0}'
                            .format(type(self.__endereco)))

        return {
            'cns': self.__cns,
            'numero': self.__numero,
            'nome': self.__nome,
            'oficial': self.__oficial,
            'endereco': self.__endereco.to_model() if (self.__endereco is not None) else None,
            'telefone': self.__telefone,
            'site': self.__site,
            'email': self.__email,
        }


class ArispEndereco(object):

    def __init__(self, model=None):
        self.__logradouro = None
        self.__numero = None
        self.__complemento = None
        self.__distrito = None
        self.__comarca = None
        self.__municipio = None
        self.__estado = None
        self.__cep = None

        if model is not None:
            self.__logradouro = model.get('logradouro', None)
            self.__numero = model.get('numero', None)
            self.__complemento = model.get('complemento', None)
            self.__distrito = model.get('distrito', None)
            self.__comarca = model.get('comarca', None)
            self.__municipio = model.get('municipio', None)
            self.__estado = model.get('estado', None)
            self.__cep = model.get('cep', None)

    @property
    def logradouro(self):
        return self.__logradouro

    @logradouro.setter
    def logradouro(self, value):
        self.__logradouro = value

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, value):
        self.__numero = value

    @property
    def complemento(self):
        return self.__complemento

    @complemento.setter
    def complemento(self, value):
        self.__complemento = value

    @property
    def distrito(self):
        return self.__distrito

    @distrito.setter
    def distrito(self, value):
        self.__distrito = value

    @property
    def comarca(self):
        return self.__comarca

    @comarca.setter
    def comarca(self, value):
        self.__comarca = value

    @property
    def municipio(self):
        return self.__municipio

    @municipio.setter
    def municipio(self, value):
        self.__municipio = value

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value):
        self.__estado = value

    @property
    def cep(self):
        return self.__cep

    @cep.setter
    def cep(self, value):
        self.__cep = value

    def to_model(self):
        if self.__logradouro is None:
            raise Exception('The "logradouro" field was not set')

        if self.__municipio is None:
            raise Exception('The "municipio" field was not set')

        if self.__estado is None:
            raise Exception('The "estado" field was not set')

        supported_estado = "^AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO$"
        if not re.search(supported_estado, self.__estado):
            raise Exception('Unsupported "estado" field: {0}'.format(self.__estado))

        return {
            'logradouro': self.__logradouro,
            'numero': self.__numero,
            'complemento': self.__complemento,
            'distrito': self.__distrito,
            'comarca': self.__comarca,
            'municipio': self.__municipio,
            'estado': self.__estado,
            'cep': self.__cep,
        }


class CieCertificateParameters(CertificateParameters):

    def __init__(self, model=None):
        CertificateParameters.__init__(self, model)
        self._format = CertificateFormats.CIE

        self.__name = None
        self.__eea = None
        self.__birth_date = None
        self.__cpf = None
        self.__registration_number = None
        self.__id_number = None
        self.__id_issuer = None
        self.__id_issuer_state = None
        self.__degree = None
        self.__course = None
        self.__institution = None

        if model is not None:
            self.__name = model.get('name', None)
            self.__eea = model.get('eea', None)
            self.__birth_date = model.get('birthDate', None)
            self.__cpf = model.get('cpf', None)
            self.__registration_number = model.get('registrationNumber', None)
            self.__id_number = model.get('idNumber', None)
            self.__id_issuer = model.get('idIssuer', None)
            self.__id_issuer_state = model.get('idIssuerState', None)
            self.__degree = model.get('degree', None)
            self.__course = model.get('course', None)

            if model.get('institution', None) is not None:
                self.__institution = CieInstitution(model.get('institution', None))

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def eea(self):
        return self.__eea

    @eea.setter
    def eea(self, value):
        self.__eea = value

    @property
    def birth_date(self):
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, value):
        self.__birth_date = value

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, value):
        self.__cpf = value

    @property
    def registration_number(self):
        return self.__registration_number

    @registration_number.setter
    def registration_number(self, value):
        self.__registration_number = value

    @property
    def id_number(self):
        return self.__id_number

    @id_number.setter
    def id_number(self, value):
        self.__id_number = value

    @property
    def id_issuer(self):
        return self.__id_issuer

    @id_issuer.setter
    def id_issuer(self, value):
        self.__id_issuer = value

    @property
    def id_issuer_state(self):
        return self.__id_issuer_state

    @id_issuer_state.setter
    def id_issuer_state(self, value):
        self.__id_issuer_state = value

    @property
    def institution(self):
        return self.__institution

    @institution.setter
    def institution(self, value):
        self.__institution = value

    @property
    def degree(self):
        return self.__degree

    @degree.setter
    def degree(self, value):
        self.__degree = value

    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self, value):
        self.__course = value

    def to_model(self):
        if self.__name is None:
            raise Exception('The "name" field was not set')

        if self.__registration_number is None:
            raise Exception('The "registrationNumber" field was not set')

        if self.__degree is None:
            raise Exception('The "degree" field was not set')

        if self.__course is None:
            raise Exception('The "course" field was not set')

        if self.__institution is not None and not (isinstance(self.__institution, CieInstitution)):
            raise Exception('Unsupported type for "institution" field on model for CieCertificateParameters: {0}'
                            .format(type(self.__institution)))

        model = super(CieCertificateParameters, self).to_model()
        model['name'] = self.__name
        model['eea'] = self.__eea
        model['birthDate'] = self.__birth_date
        model['cpf'] = self.__cpf
        model['registrationNumber'] = self.__registration_number
        model['idNumber'] = self.__id_number
        model['idIssuer'] = self.__id_issuer
        model['idIssuerState'] = self.__id_issuer_state
        model['institution'] = self.__institution
        model['degree'] = self.__degree
        model['course'] = self.__course
        return model


class CieInstitution(object):

    def __init__(self, model=None):
        self.__name = None
        self.__city = None
        self.__state = None

        if model is not None:
            self.__name = model.get('name', None)
            self.__city = model.get('city', None)
            self.__state = model.get('state', None)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        self.__city = value

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    def to_model(self):
        if self.__name is None:
            raise Exception('The "name" field was not set')

        if self.__city is None:
            raise Exception('The "city" field was not set')

        if self.__state is None:
            raise Exception('The "state" field was not set')

        return {
            'name': self.__name,
            'city': self.__city,
            'state': self.__state,
        }


class CnbCertificateParameters(PkiBrazilCertificateParameters):

    def __init__(self, model=None):
        PkiBrazilCertificateParameters.__init__(self, model)
        self._format = CertificateFormats.CNB

        self.__certificate_type = None

        if model is not None:
            self.__certificate_type = model.get('certificateType', None)

    @property
    def certificate_type(self):
        return self.__certificate_type

    @certificate_type.setter
    def certificate_type(self, value):
        self.__certificate_type = value

    def to_model(self):
        model = super(CnbCertificateParameters, self).to_model()
        model['certificateType'] = self.__certificate_type
        return model


class CnbCACertificateParameters(CertificateParameters):

    def __init__(self, model=None):
        CertificateParameters.__init__(self, model)
        self._format = CertificateFormats.CNB_CA

        self.__name = None
        self.__cns = None
        self.__street_address = None
        self.__locality = None
        self.__state_name = None
        self.__postal_code = None

        if model is not None:
            self.__name = model.get('name', None)
            self.__cns = model.get('cns', None)
            self.__street_address = model.get('streetAddress', None)
            self.__locality = model.get('locality', None)
            self.__state_name = model.get('stateName', None)
            self.__postal_code = model.get('postalCode', None)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def cns(self):
        return self.__cns

    @cns.setter
    def cns(self, value):
        self.__cns = value

    @property
    def street_address(self):
        return self.__street_address

    @street_address.setter
    def street_address(self, value):
        self.__street_address = value

    @property
    def locality(self):
        return self.__locality

    @locality.setter
    def locality(self, value):
        self.__locality = value

    @property
    def state_name(self):
        return self.__state_name

    @state_name.setter
    def state_name(self, value):
        self.__state_name = value

    @property
    def postal_code(self):
        return self.__postal_code

    @postal_code.setter
    def postal_code(self, value):
        self.__postal_code = value

    def to_model(self):
        if self.__name is None:
            raise Exception('The "name" field was not set')

        if self.__cns is None:
            raise Exception('The "cns" field was not set')

        model = super(CnbCACertificateParameters, self).to_model()
        model['name'] = self.__name
        model['cns'] = self.__cns
        model['streetAddress'] = self.__street_address
        model['locality'] = self.__locality
        model['stateName'] = self.__state_name
        model['postalCode'] = self.__postal_code
        return model


class SslCertificateParameters(CertificateParameters):

    def __init__(self, model=None):
        CertificateParameters.__init__(self, model)
        self._format = CertificateFormats.SSL

        self.__dns_names = None

        if model is not None:
            self.__dns_names = model.get('dnsNames', None)

    @property
    def dns_names(self):
        return self.__dns_names

    @dns_names.setter
    def dns_names(self, value):
        self.__dns_names = value

    def to_model(self):
        model = super(SslCertificateParameters, self).to_model()
        model['dnsNames'] = self.__dns_names
        return model


__all__ = [
    'CertificateParameters',
    'PkiBrazilCertificateParameters',
    'ArispCertificateParameters',
    'ArispCartorioInfo',
    'ArispEndereco',
    'CieCertificateParameters',
    'CieInstitution',
    'CnbCertificateParameters',
    'CnbCACertificateParameters',
    'SslCertificateParameters',
]
