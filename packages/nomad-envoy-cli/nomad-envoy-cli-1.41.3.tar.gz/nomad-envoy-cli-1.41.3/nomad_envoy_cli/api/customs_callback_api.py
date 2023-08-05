# coding: utf-8

"""
    Nomad Envoy

    This is the API descriptor for the Nomad Envoy API, responsible for order operation and product lists. Developed by [Samarkand Global](https://samarkand.global) in partnership with [Youzan](https://www.youzan.com/), [LittleRED](https://www.xiaohongshu.com/), [PDD](http://www.pinduoduo.com/), etc. Read the documentation online at [Nomad API Suite](https://api.samarkand.io/). - Install for node with `npm install nomad_envoy_cli` - Install for python with `pip install nomad-envoy-cli`  # noqa: E501

    The version of the OpenAPI document: 1.41.3
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from nomad_envoy_cli.api_client import ApiClient
from nomad_envoy_cli.exceptions import (
    ApiTypeError,
    ApiValueError
)


class CustomsCallbackApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def post_customs_callback(self, store, body, **kwargs):  # noqa: E501
        """postCustomsCallback  # noqa: E501

        Customs server calls Nomad to receive the filing result of one order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_customs_callback(store, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str store: ID of the store. (required)
        :param file body: Order details (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.post_customs_callback_with_http_info(store, body, **kwargs)  # noqa: E501

    def post_customs_callback_with_http_info(self, store, body, **kwargs):  # noqa: E501
        """postCustomsCallback  # noqa: E501

        Customs server calls Nomad to receive the filing result of one order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_customs_callback_with_http_info(store, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str store: ID of the store. (required)
        :param file body: Order details (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(str, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['store', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_customs_callback" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'store' is set
        if self.api_client.client_side_validation and ('store' not in local_var_params or  # noqa: E501
                                                        local_var_params['store'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `store` when calling `post_customs_callback`")  # noqa: E501
        # verify the required parameter 'body' is set
        if self.api_client.client_side_validation and ('body' not in local_var_params or  # noqa: E501
                                                        local_var_params['body'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `body` when calling `post_customs_callback`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'store' in local_var_params:
            path_params['store'] = local_var_params['store']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ca_key', 'ca_stage']  # noqa: E501

        return self.api_client.call_api(
            '/customs/{store}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='str',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
