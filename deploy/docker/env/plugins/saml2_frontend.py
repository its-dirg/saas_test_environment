from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.saml import NAME_FORMAT_URI
from saml2.saml import NAMEID_FORMAT_TRANSIENT
from saml2.saml import NAMEID_FORMAT_PERSISTENT

from satosa.plugin_base.endpoint import FrontendModulePlugin
from satosa.frontends.saml2 import SamlFrontend

__author__ = 'mathiashedstrom'

xmlsec_path = '/usr/bin/xmlsec1'

MODULE = SamlFrontend
RECEIVER = "Saml2IDP"
ENDPOINTS = {"single_sign_on_service": {BINDING_HTTP_REDIRECT: "sso/redirect",
                                        BINDING_HTTP_POST: "sso/post"}}


class Saml2FrontendModulePlugin(FrontendModulePlugin):
    def __init__(self, base_url):
        idpConfig = {
            "entityid": "%s/%s/proxy.xml" % (base_url, RECEIVER),
            "description": "A SAML2SAML proxy",
            "service": {
                "idp": {
                    "name": "Proxy IdP",
                    "endpoints": {
                        "single_sign_on_service": [
                            # The endpoints will be added later when registering endpoints in the
                            # module.
                        ],
                    },
                    "policy": {
                        "default": {
                            "lifetime": {"minutes": 15},
                            "attribute_restrictions": None,  # means all I have
                            "name_form": NAME_FORMAT_URI,
                            "entity_categories": ["edugain"],
                            "fail_on_missing_requested": False
                        },
                    },
                    "subject_data": "./idp.subject",
                    "name_id_format": [NAMEID_FORMAT_TRANSIENT,
                                       NAMEID_FORMAT_PERSISTENT],
                    "want_authn_requests_signed": False
                },
            },
            "key_file": "frontend.key",
            "cert_file": "frontend.crt",
            "metadata": {
                "local": ["sp.xml"],
            },
            "xmlsec_binary": xmlsec_path,
            "logger": {
                "rotating": {
                    "filename": "idp.log",
                    "maxBytes": 500000,
                    "backupCount": 5,
                },
                "loglevel": "debug",
            }
        }

        config = {"idp_config": idpConfig,
                  "endpoints": ENDPOINTS,
                  "base": base_url,
                  }

        super(Saml2FrontendModulePlugin, self).__init__(MODULE, RECEIVER, config)
