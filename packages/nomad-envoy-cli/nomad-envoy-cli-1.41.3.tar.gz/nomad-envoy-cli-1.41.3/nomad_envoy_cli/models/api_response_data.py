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


class ApiResponseData(object):
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
        'products': 'list[Product]',
        'product': 'Product',
        'product_id': 'str',
        'orders': 'list[Order]',
        'order': 'Order',
        'order_id': 'str',
        'return_value': 'str'
    }

    attribute_map = {
        'products': 'products',
        'product': 'product',
        'product_id': 'productId',
        'orders': 'orders',
        'order': 'order',
        'order_id': 'orderId',
        'return_value': 'returnValue'
    }

    def __init__(self, products=None, product=None, product_id=None, orders=None, order=None, order_id=None, return_value=None, local_vars_configuration=None):  # noqa: E501
        """ApiResponseData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._products = None
        self._product = None
        self._product_id = None
        self._orders = None
        self._order = None
        self._order_id = None
        self._return_value = None
        self.discriminator = None

        if products is not None:
            self.products = products
        if product is not None:
            self.product = product
        if product_id is not None:
            self.product_id = product_id
        if orders is not None:
            self.orders = orders
        if order is not None:
            self.order = order
        if order_id is not None:
            self.order_id = order_id
        if return_value is not None:
            self.return_value = return_value

    @property
    def products(self):
        """Gets the products of this ApiResponseData.  # noqa: E501


        :return: The products of this ApiResponseData.  # noqa: E501
        :rtype: list[Product]
        """
        return self._products

    @products.setter
    def products(self, products):
        """Sets the products of this ApiResponseData.


        :param products: The products of this ApiResponseData.  # noqa: E501
        :type: list[Product]
        """

        self._products = products

    @property
    def product(self):
        """Gets the product of this ApiResponseData.  # noqa: E501


        :return: The product of this ApiResponseData.  # noqa: E501
        :rtype: Product
        """
        return self._product

    @product.setter
    def product(self, product):
        """Sets the product of this ApiResponseData.


        :param product: The product of this ApiResponseData.  # noqa: E501
        :type: Product
        """

        self._product = product

    @property
    def product_id(self):
        """Gets the product_id of this ApiResponseData.  # noqa: E501


        :return: The product_id of this ApiResponseData.  # noqa: E501
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        """Sets the product_id of this ApiResponseData.


        :param product_id: The product_id of this ApiResponseData.  # noqa: E501
        :type: str
        """

        self._product_id = product_id

    @property
    def orders(self):
        """Gets the orders of this ApiResponseData.  # noqa: E501


        :return: The orders of this ApiResponseData.  # noqa: E501
        :rtype: list[Order]
        """
        return self._orders

    @orders.setter
    def orders(self, orders):
        """Sets the orders of this ApiResponseData.


        :param orders: The orders of this ApiResponseData.  # noqa: E501
        :type: list[Order]
        """

        self._orders = orders

    @property
    def order(self):
        """Gets the order of this ApiResponseData.  # noqa: E501


        :return: The order of this ApiResponseData.  # noqa: E501
        :rtype: Order
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this ApiResponseData.


        :param order: The order of this ApiResponseData.  # noqa: E501
        :type: Order
        """

        self._order = order

    @property
    def order_id(self):
        """Gets the order_id of this ApiResponseData.  # noqa: E501


        :return: The order_id of this ApiResponseData.  # noqa: E501
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this ApiResponseData.


        :param order_id: The order_id of this ApiResponseData.  # noqa: E501
        :type: str
        """

        self._order_id = order_id

    @property
    def return_value(self):
        """Gets the return_value of this ApiResponseData.  # noqa: E501

        any other return value.  # noqa: E501

        :return: The return_value of this ApiResponseData.  # noqa: E501
        :rtype: str
        """
        return self._return_value

    @return_value.setter
    def return_value(self, return_value):
        """Sets the return_value of this ApiResponseData.

        any other return value.  # noqa: E501

        :param return_value: The return_value of this ApiResponseData.  # noqa: E501
        :type: str
        """

        self._return_value = return_value

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
        if not isinstance(other, ApiResponseData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ApiResponseData):
            return True

        return self.to_dict() != other.to_dict()
