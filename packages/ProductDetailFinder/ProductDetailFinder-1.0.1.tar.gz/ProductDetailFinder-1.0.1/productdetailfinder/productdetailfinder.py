from productdetailfinder.constants import *
from productdetailfinder.exception import ProductIsOutOfStock, UnableToSupportDomain, UnableToGetProductId
from productdetailfinder.util import get_product_id, is_amazon_product_in_stock, get_amazon_product_information, \
    get_flipkart_product_information


def get_product_details(full_url, domain_name):
    product_id = get_product_id(full_url=full_url, domain_name=domain_name)
    if product_id is not None:
        if domain_name.lower() == DOMAIN_AMAZON.lower():
            if is_amazon_product_in_stock(asin=product_id):
                return get_amazon_product_information(
                    product_id)
            else:
                raise ProductIsOutOfStock("Product is out of stock. ASIN number {}".format(product_id))
        elif domain_name.lower() == DOMAIN_FLIPKART.lower():
            try:
                return get_flipkart_product_information(
                    product_id)
            except Exception as ex:
                raise ProductIsOutOfStock("Product is out of stock. Product id {}".format(product_id))
        else:
            raise UnableToSupportDomain("Currently we support only Amazon and Flipkart for WordPress posting.")
    else:
        raise UnableToGetProductId("Unable to get product id from - {}".format(full_url))