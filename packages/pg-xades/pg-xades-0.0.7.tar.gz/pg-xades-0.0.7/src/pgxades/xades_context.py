# -*- coding: utf-8 -*-
# © 2017 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from os import path

from lxml import etree

from pgxmlsig import SignatureContext, utils, constants
from pgxmlsig.utils import b64_print
from cryptography.hazmat.primitives import serialization
from .constants import NS_MAP, EtsiNS
from datetime import datetime
import pytz
import base64
from cryptography.x509.oid import ExtensionOID
from . import policy
from dateutil import tz


from cryptography.x509 import oid


class XAdESContext(SignatureContext):
    def __init__(self, policy):
        """
        Declaration
        :param policy: Policy class
        :type policy: xades.Policy
        """
        self.policy = policy
        super(XAdESContext, self).__init__()

    def sign(self, node):
        """
        Signs a node
        :param node: Signature node
        :type node: lxml.etree.Element
        :return: None 
        """

        signed_properties = node.find(
            "ds:Object/xades:QualifyingProperties["
            "@Target='#{}']/xades:SignedProperties".format(
                node.get('Id')),
            namespaces=NS_MAP)
        assert signed_properties is not None
        self.calculate_signed_properties(signed_properties, node, True)
        unsigned_properties = node.find(
            "ds:Object/xades:QualifyingProperties["
            "@Target='#{}']/xades:UnSignedProperties".format(
                node.get('Id')),
            namespaces=NS_MAP)
        if unsigned_properties is not None:
            self.calculate_unsigned_properties(signed_properties, node, True)

        res = super(XAdESContext, self).sign(node)
        return res

    def verify(self, node):
        """
        verifies a signature
        :param node: Signature node
        :type node: lxml.etree.Element
        :return: 
        """
        schema = etree.XMLSchema(etree.parse(path.join(
            path.dirname(__file__), "data/XAdES.xsd"
        )))
        schema.assertValid(node)
        signed_properties = node.find(
            "ds:Object/xades:QualifyingProperties["
            "@Target='#{}']/xades:SignedProperties".format(
                node.get('Id')),
            namespaces=NS_MAP)
        assert signed_properties is not None
        self.calculate_signed_properties(signed_properties, node, False)
        unsigned_properties = node.find(
            "ds:Object/xades:QualifyingProperties["
            "@Target='#{}']/xades:UnSignedProperties".format(
                node.get('Id')),
            namespaces=NS_MAP)
        if unsigned_properties is not None:
            self.calculate_unsigned_properties(signed_properties, node, False)
        res = super(XAdESContext, self).verify(node)
        return res

    def calculate_signed_properties(self, signed_properties, node, sign=False):
        signature_properties = signed_properties.find(
            'xades:SignedSignatureProperties', namespaces=NS_MAP
        )
        assert signature_properties is not None
        self.calculate_signature_properties(signature_properties, node, sign)
        data_object_properties = signed_properties.find(
            'xades:SignedDataObjectProperties', namespaces=NS_MAP
        )
        if signature_properties is None:
            self.calculate_data_object_properties(
                data_object_properties, node, sign
            )
        return

    def calculate_signature_properties(
            self, signature_properties, node, sign=False):
        signing_time = signature_properties.find(
            'xades:SigningTime', namespaces=NS_MAP
        )
        assert signing_time is not None


        # Fix to xades4j.verification.SigningTimeVerificationException
        if sign and signing_time.text is None:
            from_zone = tz.gettz('UTC')
            to_zone = tz.gettz('America/Bogota')
            now=datetime.now()
            utc = now.replace(tzinfo=from_zone)
            col = utc.astimezone(to_zone)
            signing_time.text = col.isoformat()

        certificate_list = signature_properties.find(
            'xades:SigningCertificate', namespaces=NS_MAP
        )
        assert certificate_list is not None
        if sign:
            self.policy.calculate_certificate(certificate_list, self.x509)
        else:
            self.policy.validate_certificate(certificate_list, node)
        policy = signature_properties.find(
            'xades:SignaturePolicyIdentifier', namespaces=NS_MAP
        )
        assert policy is not None
        self.policy.calculate_policy_node(policy, sign)

    def calculate_data_object_properties(self, data_object_properties, node, sign=False):
        return

    def calculate_unsigned_properties(self, unsigned_properties, node, sign=False):
        return
