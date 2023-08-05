# coding: utf-8

"""
    Nomad Envoy

    This is the API descriptor for the Nomad Envoy API, responsible for order operation and product lists. Developed by [Samarkand Global](https://samarkand.global) in partnership with [Youzan](https://www.youzan.com/), [LittleRED](https://www.xiaohongshu.com/), [PDD](http://www.pinduoduo.com/), etc. Read the documentation online at [Nomad API Suite](https://api.samarkand.io/). - Install for node with `npm install nomad_envoy_cli` - Install for python with `pip install nomad-envoy-cli`  # noqa: E501

    The version of the OpenAPI document: 1.41.4
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from nomad_envoy_cli.configuration import Configuration


class Images(object):
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
        'ids': 'list[str]',
        'urls': 'list[str]',
        'uploads': 'list[str]'
    }

    attribute_map = {
        'ids': 'ids',
        'urls': 'urls',
        'uploads': 'uploads'
    }

    def __init__(self, ids=None, urls=None, uploads=None, local_vars_configuration=None):  # noqa: E501
        """Images - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._ids = None
        self._urls = None
        self._uploads = None
        self.discriminator = None

        if ids is not None:
            self.ids = ids
        if urls is not None:
            self.urls = urls
        if uploads is not None:
            self.uploads = uploads

    @property
    def ids(self):
        """Gets the ids of this Images.  # noqa: E501

        [response] The image ids of that platform.  # noqa: E501

        :return: The ids of this Images.  # noqa: E501
        :rtype: list[str]
        """
        return self._ids

    @ids.setter
    def ids(self, ids):
        """Sets the ids of this Images.

        [response] The image ids of that platform.  # noqa: E501

        :param ids: The ids of this Images.  # noqa: E501
        :type: list[str]
        """

        self._ids = ids

    @property
    def urls(self):
        """Gets the urls of this Images.  # noqa: E501

        [response] The image urls of that platform.  # noqa: E501

        :return: The urls of this Images.  # noqa: E501
        :rtype: list[str]
        """
        return self._urls

    @urls.setter
    def urls(self, urls):
        """Sets the urls of this Images.

        [response] The image urls of that platform.  # noqa: E501

        :param urls: The urls of this Images.  # noqa: E501
        :type: list[str]
        """

        self._urls = urls

    @property
    def uploads(self):
        """Gets the uploads of this Images.  # noqa: E501

        [request] Upload one or more images to a specific platform via URL  # noqa: E501

        :return: The uploads of this Images.  # noqa: E501
        :rtype: list[str]
        """
        return self._uploads

    @uploads.setter
    def uploads(self, uploads):
        """Sets the uploads of this Images.

        [request] Upload one or more images to a specific platform via URL  # noqa: E501

        :param uploads: The uploads of this Images.  # noqa: E501
        :type: list[str]
        """

        self._uploads = uploads

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
        if not isinstance(other, Images):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Images):
            return True

        return self.to_dict() != other.to_dict()
