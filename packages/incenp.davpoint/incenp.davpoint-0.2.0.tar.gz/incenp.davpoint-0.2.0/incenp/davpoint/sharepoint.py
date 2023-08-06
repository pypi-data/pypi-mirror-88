# -*- coding: utf-8 -*-
# davpoint - Davfs2 wrapper to mount SharePoint filesystems
# Copyright © 2019,2020 Damien Goutte-Gattat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""SharePoint helper module.

This module provides functions to interact with SharePoint services.
"""

from http.cookiejar import CookieJar
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, urlopen, HTTPCookieProcessor
from xml.etree.ElementTree import parse as xmlparse

from incenp.davpoint import Error

_request_template = '''<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
      xmlns:a="http://www.w3.org/2005/08/addressing"
      xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
  <s:Header>
    <a:Action s:mustUnderstand="1">http://schemas.xmlsoap.org/ws/2005/02/trust/RST/Issue</a:Action>
    <a:ReplyTo>
      <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
    </a:ReplyTo>
    <a:To s:mustUnderstand="1">https://login.microsoftonline.com/extSTS.srf</a:To>
    <o:Security s:mustUnderstand="1"
       xmlns:o="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
      <o:UsernameToken>
        <o:Username>{0}</o:Username>
        <o:Password>{1}</o:Password>
      </o:UsernameToken>
    </o:Security>
  </s:Header>
  <s:Body>
    <t:RequestSecurityToken xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust">
      <wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy">
        <a:EndpointReference>
          <a:Address>{2}</a:Address>
        </a:EndpointReference>
      </wsp:AppliesTo>
      <t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType>
      <t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType>
      <t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType>
    </t:RequestSecurityToken>
  </s:Body>
</s:Envelope>
'''

_site_url_template = '{}://{}/_forms/default.aspx?wa=wsignin1.0'

_namespaces = {
        'wssec': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'
        }


def authenticate(endpoint, username, password):
    """Authenticate to a SharePoint service.

    This function authenticates a user to a SharePoint service
    identified by the endpoint URL. It returns a dictionary containing
    the authentication tokens the service will expect for future
    connections.
    """
    scheme, host, _, _, _, _ = urlparse(endpoint)
    if scheme not in ['http', 'https'] or not host:
        raise Error(f"Invalid endpoint: {endpoint}")

    try:
        data = _request_template.format(username, password, endpoint)
        request = urlopen('https://login.microsoftonline.com/extSTS.srf',
                          data.encode('utf-8'))
    except URLError as e:
        raise Error(f"Authentication request failed: {e.reason}")

    reply = xmlparse(request)
    token = reply.find('.//wssec:BinarySecurityToken', _namespaces)
    if token is None:
        raise Error("Cannot retrieve authentication token")

    cookie_jar = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cookie_jar))
    try:
        request = Request(_site_url_template.format(scheme, host))
        reply = opener.open(request, data=token.text.encode('utf-8'))
    except URLError as e:
        raise Error(f"Login request failed: {e.reason}")

    cookies = {}
    for cookie in cookie_jar:
        if cookie.name in ('FedAuth', 'rtFa'):
            cookies[cookie.name] = cookie.value
    if 'FedAuth' not in cookies or 'rtFa' not in cookies:
        raise Error("Missing authentication cookies")

    return cookies
