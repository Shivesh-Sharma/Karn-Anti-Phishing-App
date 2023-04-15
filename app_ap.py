import pickle
import requests
from flask import Flask, request,jsonify

# with open('model.pkl', 'rb') as file:
#   model = pickle.load(file)

app = Flask(__name__)
model = pickle.load(open('randomfo.pkl','rb'))



def website(site):
    from urllib.parse import urlparse
    from tld import get_tld
    import re
    import tldextract
    url_length = len(str(site))
    hostname_length = len(urlparse(site).netloc)
    path_length = len(urlparse(site).path)
    def fd_length(url):
        urlpath= urlparse(url).path
        try:
            return len(urlpath.split('/')[1])
        except:
            return 0
    fd_length = fd_length(site)
    tld = get_tld(site,fail_silently=True)
    def tld_length(tld):
        try:
            return len(tld)
        except:
            return 0

    tld_length = tld_length(get_tld(site,fail_silently=True))
    def digit_count(url):
        digits = 0
        for i in url:
            if i.isnumeric():
                digits = digits + 1
        return digits
    count_digits= digit_count(site)
    def letter_count(url):
        letters = 0
        for i in url:
            if i.isalpha():
                letters = letters + 1
        return letters
    count_letters = letter_count(site)
    def no_of_dir(url):
        urldir = urlparse(url).path
        return urldir.count('/')
    count_dir=no_of_dir(site)
    count_ = site.count('-')
    count_ad = site.count('@')
    count_qu = site.count('?')
    count_dot = site.count('.')
    count_eql = site.count('=')
    count_http = site.count('http')
    count_https = site.count('https')
    count_www = site.count('www')

    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"


        # 8. Checking for Shortening Services in URL (Tiny_URL)
    def tinyURL(url):
        match=re.search(shortening_services,url)
        if match:
            return 1
        else:
            return 0
    tiny_url = tinyURL(site)
    def has_sensitive_keywords(url):
        path = urlparse(url).path
        keywords = ['login', 'banking', 'password', 'account',"password","account","verify","security","update","payment","confirmation","session","signin","logon","authenticate","validate","admin","billing","support"]
        for keyword in keywords:
            if keyword in path:
                return 1
        return 0

    sensitive_key = has_sensitive_keywords(site)
    def has_multiple_subdomains(url):
        domain = tldextract.extract(url).domain
        subdomains = tldextract.extract(url).subdomain.split('.')
        num_subdomains = len(subdomains)
        return num_subdomains

    mul_sub_domains= has_multiple_subdomains(site)







    site_dict = [url_length,hostname_length,
       path_length, fd_length, count_, count_ad, count_qu, count_dot, count_eql, count_http,count_https, count_www, tiny_url, count_digits,
       count_letters, count_dir, sensitive_key, mul_sub_domains]
    return site_dict















@app.route('/predict',methods=['post'])
def predict():
    # Get the URL from the request
    url = request.form.get('url')
    
    # Extract features from the URL
    features = website(url)
    
    # Use the pre-trained machine learning model to predict the output
    output = model.predict([features])[0]
    
    # Return the predicted output as a JSON response
    return jsonify({'output': str(output)})



    # def predict():

    #    url = request.json['url']
    #    response = requests.get(url)
    #    contents = response.text

    #    output = model.predict(0utput)[0]





# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
     
    