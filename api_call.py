import requests
import xml.etree.ElementTree as ET

token = """AgAAAA**AQAAAA**aAAAAA**PlLuWA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GlDpaDpAudj6x9nY+seQ**LyoEAA**AAMAAA**wSd/jBCbxJHbYuIfP4ESyC0mHG2Tn4O3v6rO2zmnoVSF614aVDFfLSCkJ5b9wg9nD7rkDzQayiqvwdWeoJkqEpNQx6wjbVQ1pjiIaWdrYRq+dXxxGHlyVd+LqL1oPp/T9PxgaVAuxFXlVMh6wSyoAMRySI6QUzalepa82jSQ/qDaurz40/EIhu6+sizj0mCgjcdamKhp1Jk3Hqmv8FXFnXouQ9Vr0Qt+D1POIFbfEg9ykH1/I2CYkZBMIG+k6Pf00/UujbQdne6HUAu6CSj9wGsqQSAEPIXXvEnVmtU+6U991ZUhPuA/DMFEfVlibvNLBA7Shslp2oTy2T0wlpJN+f/Jle3gurHLIPc6EkEmckEpmSpFEyuBKz+ix4Cf4wYbcUk/Gr3kGdSi20XQGu/ZnJ7Clz4vVak9iJjN99j8lwA2zKW+CBRuHBjZdaUiDctSaADHwfz/x+09bIU9icgpzuOuKooMM5STbt+yJlJZdE3SRZHwilC4dToTQeVhAXA4tFZcDrZFzBmJsoRsJYrCdkJBPeGBub+fqomQYyKt1J0LAQ5Y0FQxLHBIp0cRZTPAuL/MNxQ/UXcxQTXjoCSdZd7B55f0UapU3EsqetEFvIMPxCPJ63YahVprODDva9Kz/Htm3piKyWzuCXfeu3siJvHuOVyx7Q4wyHrIyiJDNz5b9ABAKKauxDP32uqD7jqDzsVLH11/imKLLdl0U5PN+FP30XAQGBAFkHf+pAvOFLrdDTSjT3oQhFRzRPzLWkFg"""

urn = "urn:ebay:apis:eBLBaseComponents"

xml_gateway_uri = "https://api.sandbox.ebay.com/ws/api.dll"


def get_categories():
    """
    Headers and xml specs for Ebay's GetCategories request
    :return: headers, xml as tuple
    """
    headers = {
        "X-EBAY-API-CALL-NAME": "GetCategories",  # Must match request item
        "X-EBAY-API-APP-NAME": "EchoBay62-5538-466c-b43b-662768d6841",  # AppID
        "X-EBAY-API-CERT-NAME": "00dd08ab-2082-4e3c-9518-5f4298f296db",
        "X-EBAY-API-DEV-NAME": "16a26b1b-26cf-442d-906d-597b60c41c19",  # DevId
        "X-EBAY-API-SITEID": "0",  # Ebay site to send the request: USA /
              #  USD
        "X-EBAY-API-COMPATIBILITY-LEVEL": "861",  # Ebay's supported schema
    }

    xml_data = """<?xml version="{}" encoding="{}"?>""".format("1.0", "utf-8")
    xml_data += """<GetCategoriesRequest xmlns="{}">""".format(urn)
    xml_data += """<CategorySiteID>{}</CategorySiteID>""".format(0)
    xml_data += """<DetailLevel>{}</DetailLevel>""".format("ReturnAll")
    xml_data += """<ViewAllNodes>{}</ViewAllNodes>""".format("True")
    xml_data += """<RequesterCredentials>"""
    xml_data += """<eBayAuthToken>{}</eBayAuthToken>""".format(token)
    xml_data += """</RequesterCredentials>"""
    xml_data += """</GetCategoriesRequest>"""

    return headers, xml_data


def get_category_version():
    """
    Headers and xml specs to check Ebay's Categories version.

    :return: headers, xml as tuple
    """
    headers = {
        "X-EBAY-API-CALL-NAME": "GetCategories",  # Must match request item
        "X-EBAY-API-APP-NAME": "EchoBay62-5538-466c-b43b-662768d6841",  # AppID
        "X-EBAY-API-CERT-NAME": "00dd08ab-2082-4e3c-9518-5f4298f296db",
        "X-EBAY-API-DEV-NAME": "16a26b1b-26cf-442d-906d-597b60c41c19",  # DevId
        "X-EBAY-API-SITEID": "0",  # Ebay site to send the request: USA / USD
        "X-EBAY-API-COMPATIBILITY-LEVEL": "861",  # Ebay's supported schema
    }

    xml_data = """<?xml version="{}" encoding="{}"?>""".format("1.0", "utf-8")
    xml_data += """<GetCategoriesRequest xmlns="{}">""".format(urn)
    xml_data += """<RequesterCredentials>"""
    xml_data += """<eBayAuthToken>{}</eBayAuthToken>""".format(token)
    xml_data += """</RequesterCredentials>"""
    xml_data += """</GetCategoriesRequest>"""

    return headers, xml_data


def get_data(call):
    """
    Makes the post request and returns status and response.

    :param call: tuple of headers and xml specs for request
    :return: post request status and response
    """
    h, d = call

    request = requests.post(xml_gateway_uri, headers=h,data=d)
    response = request.text.encode("utf-8")

    return request, response



def load_data(call):
    """
    Loads CategoryArray response data from server into categories variable

    :param call: tuple of headers and xml specs for request
    :return:
    """
    status, response = get_data(call)
    root = ET.fromstring(response)
    categories = root.find("{{{}}}CategoryArray".format(urn))

    return categories


if __name__ == '__main__':
    req, res = get_data(get_category_version())
    r = ET.fromstring(res)
    version = r.find("{{{}}}CategoryVersion".format(urn)).text
    ack = r.find("{{{}}}Ack".format(urn)).text

    print("Status: {}, Ack: {}, Categories Version No. {}".format(
        req, ack, version))