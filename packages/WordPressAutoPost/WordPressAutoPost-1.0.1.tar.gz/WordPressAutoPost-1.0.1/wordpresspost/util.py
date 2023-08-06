from wordpress_xmlrpc import WordPressPost, Client
from wordpress_xmlrpc.methods.posts import GetPost, xmlrpc_client
from wordpress_xmlrpc.methods import media, posts


def upload_article(wordpress_url, wordpress_username, wordpress_password, **kwargs):
    try:
        article_title = kwargs['article_title']
        article_content = kwargs['article_content']
        article_photo_path = kwargs['article_photo_path']
        article_tag = kwargs['article_tag']
        product_original_price = kwargs['product_original_price']
        product_deal_price = kwargs['product_deal_price']
        product_page_url = kwargs['product_page_url']

        client = Client(wordpress_url + '/xmlrpc.php', wordpress_username, wordpress_password)
        # prepare metadata
        data = {'name': 'picture.jpg', 'type': 'image/jpg', }

        # read the binary file and let the XMLRPC library encode it into base64
        with open(article_photo_path, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
        response = client.call(media.UploadFile(data))
        attachment_id = response['id']
        # Post
        post = WordPressPost()
        post.title = article_title
        post.content = article_content
        post.terms_names = {'post_tag': [article_tag], 'category': [article_tag]}
        post.post_status = 'publish'
        post.thumbnail = attachment_id
        post.custom_fields = []
        post.custom_fields.append({
            'key': 'rehub_main_product_price',
            'value': 'Rs. ' + str(product_deal_price)
        })

        post.custom_fields.append({
            'key': 'rehub_offer_product_url',
            'value': product_page_url
        })
        post.custom_fields.append({
            'key': 'rehub_offer_product_price_old',
            'value': 'Rs. ' + str(product_original_price)
        })
        post.custom_fields.append({
            'key': 'rehub_offer_product_price',
            'value': 'Rs. ' + str(product_deal_price)
        })
        post.id = client.call(posts.NewPost(post))
        post_detail = client.call(GetPost(post.id))
        return post_detail.link
    except Exception as ex:
        return str(ex)


def get_article_content(product_features, short_url, domain_name):
    ul_open_tag = "<ul>"
    ul_close_tag = "</ul>"
    li_tag = ''
    for product_feature in product_features:
        li_tag = li_tag + "<li>" + product_feature + "</li>"
    feature_text_to_post = ul_open_tag + li_tag + ul_close_tag
    # HTML content
    content = f""" <h2>Product Description:-</h2>
                            {feature_text_to_post}

                            <h2><strong><span style="color:#ffa500">How to get this Deal Online?</span></strong></h2>
                            <ol>
                                <li><a href="{short_url}" target='_blank'><strong>Buy Now on {domain_name.capitalize()}.
                                </strong></a></li> 
                                <li>Add product to cart.</li>
                                <li>Login or register.</li>
                                <li>Update or select shipping details.</li>
                                <li>Pay the amount.</li>
                            </ol>
                        <span style="font-size: 12px;color: red;">*Product price and availability are accurate at the time of posting the deal and are subject to change.</span>
                            """
    if domain_name == "amazon":
        content = content + "<br/><br/> <small>Disclosure: As an Amazon Associate I earn from qualifying purchases.</small>"
    return content
