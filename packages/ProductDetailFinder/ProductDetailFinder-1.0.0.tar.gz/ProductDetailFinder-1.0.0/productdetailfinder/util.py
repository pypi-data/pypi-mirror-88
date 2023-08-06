import json
import requests
import tldextract
from urllib import parse
from amazon.paapi import AmazonAPI

from productdetailfinder.constants import *
from productdetailfinder.exception import ProductIsOutOfStock, UnableToSupportDomain, UnableToGetProductId, \
    UnableToGetProductInformation


def get_product_id(full_url, domain_name):
    if domain_name.lower() == DOMAIN_AMAZON.lower():
        return get_amazon_asin_number(full_url=full_url)
    if domain_name.lower() == DOMAIN_FLIPKART.lower():
        return get_flipkart_product_id(full_url=full_url)
    return None





def get_domain_name_from_url(full_url):
    return tldextract.extract(full_url).domain.lower()


def get_amazon_asin_number(full_url):
    asin = None
    try:
        if '/dp' in full_url:
            asin = full_url.split("/dp/")[1]
            if '/' in asin:
                asin = asin.split("/")[0]
            elif '?' in asin:
                asin = asin.split("?")[0]
            elif '&' in asin:
                asin = asin.split("&")[0]
        elif '/d' in full_url:
            asin = full_url.split("/d/")[1]
            if '/' in asin:
                asin = asin.split("/")[0]
            elif '?' in asin:
                asin = asin.split("?")[0]
            elif '&' in asin:
                asin = asin.split("&")[0]
        elif '/product' in full_url:
            asin = full_url.split("/product/")[1]
            if '/' in asin:
                asin = asin.split("/")[0]
            elif '?' in asin:
                asin = asin.split("?")[0]
            elif '&' in asin:
                asin = asin.split("&")[0]
        elif '/offer-listing' in full_url:
            asin = full_url.split("/offer-listing/")[1]
            if '/' in asin:
                asin = asin.split("/")[0]
            elif '?' in asin:
                asin = asin.split("?")[0]
            elif '&' in asin:
                asin = asin.split("&")[0]
        return asin
    except Exception:
        raise UnableToGetProductId("Unable to get ASIN number from Amazon url {}".format(full_url))


def get_flipkart_product_id(full_url):
    try:
        parse.urlsplit(full_url)
        parse.parse_qs(parse.urlsplit(full_url).query)
        if "pid" not in dict(parse.parse_qsl(parse.urlsplit(full_url).query)):
            raise UnableToGetProductId("Unable to get Product Id from Flipkart url {}".format(full_url))
        product_id = dict(parse.parse_qsl(parse.urlsplit(full_url).query))['pid']
        return product_id
    except Exception:
        raise UnableToGetProductId("Unable to get Product Id from Flipkart url {}".format(full_url))


def is_amazon_product_in_stock(asin):
    try:
        amazon = AmazonAPI(key=AMAZON_KEY, secret=AMAZON_SECRET, tag=AMAZON_AFFILIATE_ID, country=AMAZON_COUNTRY)
        product = amazon.get_product(asin)
        mrp_price = product.prices.pvp.value
        if mrp_price is None:
            raise ProductIsOutOfStock("Product is out of stock. ASIN number {}".format(asin))
        else:
            return True
    except Exception as ex:
        raise ProductIsOutOfStock("Product is out of stock. ASIN number {}".format(asin))


def get_amazon_product_information(asin):
    amazon = AmazonAPI(key=AMAZON_KEY, secret=AMAZON_SECRET, tag=AMAZON_AFFILIATE_ID, country=AMAZON_COUNTRY)
    try:
        product = amazon.get_product(asin)
        mrp_price = product.prices.pvp.value
        deal_price = product.prices.price.value
        product_image_url = product.images.large
        discount = product.prices.price.savings.percentage
        if mrp_price is None:
            mrp_price = deal_price
            discount = '0.00'
        title = product.title
        product_feature = product.product.features
        return {
            'product_image_url': product_image_url,
            'mrp_price': mrp_price,
            'deal_price': deal_price,
            'discount': str(round(discount, 2)),
            'title': title,
            'product_feature': product_feature
        }
    except Exception as ex:
        raise UnableToGetProductInformation("Unable to get product information of ASIN - {}".format(asin))


def get_flipkart_product_information(product_id):
    flipkart_url = 'https://affiliate-api.flipkart.net/affiliate/1.0/product.json?id=' + product_id
    headers = {
        'Fk-Affiliate-Id': FLIPKART_AFFILIATE_ID,
        'Fk-Affiliate-Token': FLIPKART_AFFILIATE_API_KEY
    }
    try:
        client_info_response = requests.get(flipkart_url, headers=headers)
        json_format = json.loads(client_info_response.text)
        product_image_url = json_format['productBaseInfoV1']['imageUrls']['800x800']
        mrp_price = json_format['productBaseInfoV1']['maximumRetailPrice']['amount']
        deal_price = json_format['productBaseInfoV1']['flipkartSpecialPrice']['amount']
        try:
            discount = (float(mrp_price) - float(deal_price)) / float(mrp_price) * 100
        except ZeroDivisionError:
            discount = 0.00
            pass
        title = json_format['productBaseInfoV1']['title']
        product_feature = json_format['categorySpecificInfoV1']['keySpecs']

        return {
            'product_image_url': product_image_url,
            'mrp_price': mrp_price,
            'deal_price': deal_price,
            'discount': str(round(discount, 2)),
            'title': title,
            'product_feature': product_feature
        }
    except Exception:
        raise UnableToGetProductInformation("Unable to get product information of Product Id - {}".format(product_id))

