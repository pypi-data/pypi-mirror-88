# coding: utf-8

"""
    Nomad Envoy

    This is the API descriptor for the Nomad Envoy API, responsible for order operation and product lists. Developed by [Samarkand Global](https://samarkand.global) in partnership with [Youzan](https://www.youzan.com/), [LittleRED](https://www.xiaohongshu.com/), [PDD](http://www.pinduoduo.com/), etc. Read the documentation online at [Nomad API Suite](https://api.samarkand.io/). - Install for node with `npm install nomad_envoy_cli` - Install for python with `pip install nomad-envoy-cli`  # noqa: E501

    The version of the OpenAPI document: 1.41.3
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from nomad_envoy_cli.configuration import Configuration


class CustomsDeclarationResult(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'region': 'str',
        'declaration_type': 'str',
        'declaration_number': 'str',
        'client_order_ref': 'str',
        'order_id': 'str',
        'product_sku_number': 'str',
        'product_barcode': 'str',
        'orig_message': 'str',
        'is_regsitered': 'bool'
    }

    attribute_map = {
        'region': 'region',
        'declaration_type': 'declarationType',
        'declaration_number': 'declarationNumber',
        'client_order_ref': 'clientOrderRef',
        'order_id': 'orderId',
        'product_sku_number': 'product_sku_number',
        'product_barcode': 'product_barcode',
        'orig_message': 'origMessage',
        'is_regsitered': 'isRegsitered'
    }

    def __init__(self, region=None, declaration_type=None, declaration_number=None, client_order_ref=None, order_id=None, product_sku_number=None, product_barcode=None, orig_message=None, is_regsitered=None, local_vars_configuration=None):  # noqa: E501
        """CustomsDeclarationResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._region = None
        self._declaration_type = None
        self._declaration_number = None
        self._client_order_ref = None
        self._order_id = None
        self._product_sku_number = None
        self._product_barcode = None
        self._orig_message = None
        self._is_regsitered = None
        self.discriminator = None

        if region is not None:
            self.region = region
        if declaration_type is not None:
            self.declaration_type = declaration_type
        if declaration_number is not None:
            self.declaration_number = declaration_number
        if client_order_ref is not None:
            self.client_order_ref = client_order_ref
        if order_id is not None:
            self.order_id = order_id
        if product_sku_number is not None:
            self.product_sku_number = product_sku_number
        if product_barcode is not None:
            self.product_barcode = product_barcode
        if orig_message is not None:
            self.orig_message = orig_message
        if is_regsitered is not None:
            self.is_regsitered = is_regsitered

    @property
    def region(self):
        """Gets the region of this CustomsDeclarationResult.  # noqa: E501

        The sender customs port of current callback.  # noqa: E501

        :return: The region of this CustomsDeclarationResult.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this CustomsDeclarationResult.

        The sender customs port of current callback.  # noqa: E501

        :param region: The region of this CustomsDeclarationResult.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def declaration_type(self):
        """Gets the declaration_type of this CustomsDeclarationResult.  # noqa: E501

        could be one of order/product/company/brand  # noqa: E501

        :return: The declaration_type of this CustomsDeclarationResult.  # noqa: E501
        :rtype: str
        """
        return self._declaration_type

    @declaration_type.setter
    def declaration_type(self, declaration_type):
        """Sets the declaration_type of this CustomsDeclarationResult.

        could be one of order/product/company/brand  # noqa: E501

        :param declaration_type: The declaration_type of this CustomsDeclarationResult.  # noqa: E501
        :type: str
        """

        self._declaration_type = declaration_type

    @property
    def declaration_number(self):
        """Gets the declaration_number of this CustomsDeclarationResult.  # noqa: E501

        1. an unique number given by customs when the order/product filing is successful, otherwise will be empty   # noqa: E501

        :return: The declaration_number of this CustomsDeclarationResult.  # noqa: E501
        :rtype: str
        """
        return self._declaration_number

    @declaration_number.setter
    def declaration_number(self, declaration_number):
        """Sets the declaration_number of this CustomsDeclarationResult.

        1. an unique number given by customs when the order/product filing is successful, otherwise will be empty   # noqa: E501

        :param declaration_number: The declaration_number of this CustomsDeclarationResult.  # noqa: E501
        :type: str
        """

        self._declaration_number = declaration_number

    @property
    def client_order_ref(self):
        """Gets the client_order_ref of this CustomsDeclarationResult.  # noqa: E501

        Client order ref (third party platform)  # noqa: E501

        :return: The client_order_ref of this CustomsDeclarationResult.  # noqa: E501
        :rtype: str
        """
        return self._client_order_ref

    @client_order_ref.setter
    def client_order_ref(self, client_order_ref):
        """Sets the client_order_ref of this CustomsDeclarationResult.

        Client order ref (third party platform)  # noqa: E501

        :param client_order_ref: The client_order_ref of this CustomsDeclarationResult.  # noqa: E501
        :type: str
        """

        self._client_order_ref = client_order_ref

    @property
    def order_id(self):
        """Gets the order_id of this CustomsDeclarationResult.  # noqa: E501

        Order ID ref (Odoo platform).  # noqa: E501

        :return: The order_id of this CustomsDeclarationResult.  # noqa: E501
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this CustomsDeclarationResult.

        Order ID ref (Odoo platform).  # noqa: E501

        :param order_id: The order_id of this CustomsDeclarationResult.  # noqa: E501
        :type: str
        """

        self._order_id = order_id

    @property
    def product_sku_number(self):
        """Gets the product_sku_number of this CustomsDeclarationResult.  # noqa: E501

        the sku number of current product/sku  # noqa: E501

        :return: The product_sku_number of this CustomsDeclarationResult.  # noqa: E501
        :rtype: str
        """
        return self._product_sku_number

    @product_sku_number.setter
    def product_sku_number(self, product_sku_number):
        """Sets the product_sku_number of this CustomsDeclarationResult.

        the sku number of current product/sku  # noqa: E501

        :param product_sku_number: The product_sku_number of this CustomsDeclarationResult.  # noqa: E501
        :type: str
        """

        self._product_sku_number = product_sku_number

    @property
    def product_barcode(self):
        """Gets the product_barcode of this CustomsDeclarationResult.  # noqa: E501

        the barcode of current product/sku  # noqa: E501

        :return: The product_barcode of this CustomsDeclarationResult.  # noqa: E501
        :rtype: str
        """
        return self._product_barcode

    @product_barcode.setter
    def product_barcode(self, product_barcode):
        """Sets the product_barcode of this CustomsDeclarationResult.

        the barcode of current product/sku  # noqa: E501

        :param product_barcode: The product_barcode of this CustomsDeclarationResult.  # noqa: E501
        :type: str
        """

        self._product_barcode = product_barcode

    @property
    def orig_message(self):
        """Gets the orig_message of this CustomsDeclarationResult.  # noqa: E501

        Original message from the customs  # noqa: E501

        :return: The orig_message of this CustomsDeclarationResult.  # noqa: E501
        :rtype: str
        """
        return self._orig_message

    @orig_message.setter
    def orig_message(self, orig_message):
        """Sets the orig_message of this CustomsDeclarationResult.

        Original message from the customs  # noqa: E501

        :param orig_message: The orig_message of this CustomsDeclarationResult.  # noqa: E501
        :type: str
        """

        self._orig_message = orig_message

    @property
    def is_regsitered(self):
        """Gets the is_regsitered of this CustomsDeclarationResult.  # noqa: E501

        Return True if current order/product/.. already registered  # noqa: E501

        :return: The is_regsitered of this CustomsDeclarationResult.  # noqa: E501
        :rtype: bool
        """
        return self._is_regsitered

    @is_regsitered.setter
    def is_regsitered(self, is_regsitered):
        """Sets the is_regsitered of this CustomsDeclarationResult.

        Return True if current order/product/.. already registered  # noqa: E501

        :param is_regsitered: The is_regsitered of this CustomsDeclarationResult.  # noqa: E501
        :type: bool
        """

        self._is_regsitered = is_regsitered

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CustomsDeclarationResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CustomsDeclarationResult):
            return True

        return self.to_dict() != other.to_dict()
