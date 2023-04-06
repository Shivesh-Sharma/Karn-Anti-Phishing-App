import pickle
#import requests
from flask import Flask, request, jsonify,render_template

# with open('model.pkl', 'rb') as file:
#   model = pickle.load(file)

app = Flask(__name__)
model = pickle.load(open('mypickle.pkl','rb'))
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict',methods=['post'])
def predict():
    def website(site):
        from urllib.parse import urlparse

        from tld import get_tld

        import requests
        import re
        import ipaddress
        url_length = len(str(site))
        hostname_length = len(urlparse(site).netloc)
        path_length = len(urlparse(site).path)

        def fd_length(url):
            urlpath = urlparse(url).path
            try:
                return len(urlpath.split('/')[1])
            except:
                return 0

        fd_length = fd_length(site)
        tld = get_tld(site, fail_silently=True)

        def tld_length(tld):
            try:
                return len(tld)

            except:
                return -1

        tld_length = tld_length(get_tld(site, fail_silently=True))

        def digit_count(url):
            digits = 0
            for i in url:
                if i.isnumeric():
                    digits = digits + 1
            return digits

        count_digits = digit_count(site)

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

        count_dir = no_of_dir(site)
        count_ = site.count('-')
        count_ad = site.count('@')
        count_qu = site.count('?')
        count_pr = site.count('%')
        count_dot = site.count('.')
        count_eql = site.count('=')
        count_http = site.count('http')
        count_https = site.count('https')
        count_www = site.count('www')

        # 2.Checks for IP address in URL (Have_IP)
        def havingIP(url):
            try:
                ipaddress.ip_address(url)
                ip = 1

            except:
                ip = 0
            return ip

        having_ip = havingIP(site)

        # 6.Checking for redirection '//' in the url (Redirection)
        def redirection(url):
            pos = url.rfind('//')
            if pos > 6:
                if pos > 7:
                    return 1
                else:
                    return 0
            else:
                return 0

        red = redirection(site)
        # listing shortening services
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
            match = re.search(shortening_services, url)
            if match:
                return 1
            else:
                return 0

        tiny_url = tinyURL(site)

        # 15. IFrame Redirection (iFrame)
        def iframe(response):
            if response == "":
                return 1
            else:
                if re.findall(r"[|]", response.text):
                    return 0
                else:
                    return 1
            # 16.Checks the effect of mouse over on status bar (Mouse_Over)

        def mouseOver(response):
            if response == "":
                return 1
            else:
                if re.findall("", response.text):
                    return 1
                else:
                    return 0

            # 17.Checks the status of the right click attribute (Right_Click)

        def rightClick(response):
            if response == "":
                return 1
            else:
                if re.findall(r"event.button ?== ?2", response.text):
                    return 0
                else:
                    return 1

            # 18.Checks the number of forwardings (Web_Forwards)

        def forwarding(response):
            if response == "":
                return 1
            else:
                if len(response.history) <= 2:
                    return 0
                else:
                    return 1

        try:
            response = requests.get(site)
        except:
            response = ""
        i_frame = iframe(response)
        mouse_over = mouseOver(response)
        right_click = rightClick(response)
        forwar = forwarding(response)

        site_dict = [hostname_length,
                     path_length, fd_length, count_, count_ad, count_qu,
                     count_pr, count_dot, count_eql, count_http, count_https, count_www, having_ip, red, tiny_url,
                     i_frame, mouse_over, right_click, forwar, count_digits,
                     count_letters, count_dir]
        return site_dict

    u = request.form.get('url')
    #response = requests.get(url)
    feat = website(u)
    #contents = response.text

    output = model.predict([feat])[0]

    #return jsonify({"phising":str(output)})
    return str(output)
    #return jsonify(feat)



    # def predict():

    #    url = request.json['url']
    #    response = requests.get(url)
    #    contents = response.text

    #    output = model.predict(0utput)[0]




# Run the app
if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 8080, debug=True)
