from flask import Flask, jsonify, request
from urllib.parse import urlparse
import socket
import geocoder

app = Flask(__name__)

@app.route('/location', methods=['POST'])
def location():
    url = request.form.get('url')
    s = urlparse(url).netloc
    ip_address = socket.gethostbyname(s)
    geo_code_of_ip = geocoder.ip(ip_address)
    location_data = {
        'ip_address': ip_address,
        'latitude': str(geo_code_of_ip.latlng[0]),
        'longitude': str(geo_code_of_ip.latlng[1]),
        'address': geo_code_of_ip.address,
    }
    return jsonify(location_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)







    
   