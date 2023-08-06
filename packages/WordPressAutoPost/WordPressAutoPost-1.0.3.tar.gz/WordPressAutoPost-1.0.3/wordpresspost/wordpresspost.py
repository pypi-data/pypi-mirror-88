from affiliate_link_converter import expand_short_url
from productdetailfinder import get_product_details
from productdetailfinder.util import get_domain_name_from_url
from wordpresspost.exception import UnableToPostDealOnWordPress
from wordpresspost.util import get_article_content, upload_article


def post_blog(wordpress_url, wordpress_username, wordpress_password, short_url):
    try:
        full_url = expand_short_url(short_url)
        domain_name = get_domain_name_from_url(full_url=full_url)
        product_details = get_product_details(full_url=full_url, domain_name=domain_name)

        article_content = get_article_content(
            product_features=product_details['product_feature'],
            short_url=short_url,
            domain_name=domain_name
        )
        upload_article(wordpress_url=wordpress_url,
                       wordpress_password=wordpress_password,
                       wordpress_username=wordpress_username,
                       article_title=product_details['title'],
                       article_content=article_content,
                       article_photo_path=product_details['product_image_url'],
                       article_tag=domain_name,
                       product_original_price=product_details['mrp_price'],
                       product_deal_price=product_details['deal_price'],
                       product_page_url=short_url
                       )
        return True
    except Exception as ex:
        raise UnableToPostDealOnWordPress("Unable to post deal on WordPress. Error - {}".format(str(ex)))

