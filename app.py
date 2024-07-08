from flask import Flask, render_template, jsonify, request
import requests
import subprocess
import logging
import re

app = Flask(__name__)
app.config['DEBUG'] = True

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assetfinder', methods=['POST'])
def assetfinder():
    data = request.get_json()
    domain = data.get('domain')
    if not domain:
        return jsonify({'error': 'Dominio no proporcionado'}), 400

    try:
        result = subprocess.run(['assetfinder', domain], capture_output=True, text=True)
        output = result.stdout
        subdomains = output.splitlines()
    except Exception as e:
        logging.error(f"Error al ejecutar assetfinder: {e}")
        return jsonify({'error': str(e)}), 500

    return jsonify({'subdomains': subdomains})

@app.route('/subdominios', methods=['POST'])
def subdominios():
    domain = request.form.get('domain')
    if not domain:
        return render_template('resultApiSubdomain.html', error='Dominio no proporcionado')

    try:
        url = "https://subdomain-finder3.p.rapidapi.com/v1/subdomain-finder/"
        querystring = {"domain": domain}
        headers = {
            "x-rapidapi-key": "374e647756mshaed1e310a2b449cp12cd97jsn5fbafbd9880d",
            "x-rapidapi-host": "subdomain-finder3.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        response_data = response.json()
        subdomains = response_data.get('subdomains', [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al llamar a la API de RapidAPI: {e}")
        return render_template('resultApiSubdomain.html', error=f"Error al llamar a la API de RapidAPI: {e}")
    except Exception as e:
        logging.error(f"Error general: {e}")
        return render_template('resultApiSubdomain.html', error=str(e))

    return render_template('resultApiSubdomain.html', subdomains=subdomains)

@app.route('/whois', methods=['POST'])
def whois():
    domain = request.form.get('domain')
    if not domain:
        return render_template('resultadosWhois.html', error='Dominio no proporcionado')

    try:
        url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
        params = {
            "apiKey": "at_gSMULVtWXXr4wff94NqNFOBUGZXK4",
            "domainName": domain,
            "outputFormat": "JSON"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al llamar a la API de WHOISXML: {e}")
        return render_template('resultadosWhois.html', error=f"Error al llamar a la API de WHOISXML: {e}")
    except Exception as e:
        logging.error(f"Error general: {e}")
        return render_template('resultadosWhois.html', error=str(e))

    return render_template('resultadosWhois.html', whois_data=response_data)

if __name__ == "__main__":
    app.run(debug=True)


# @app.route('/amass', methods=['POST']) NO FUNCIONA 
# def amass():
#     domain = request.form.get('domain')
#     if not domain:
#         return render_template('result.html', error='Dominio no proporcionado')

#     try:
#         result = subprocess.run([AMASS_PATH, 'intel', '-whois', '-d', domain], capture_output=True, text=True)
#         output = result.stdout
#         subdomains = output.splitlines()
#     except Exception as e:
#         logging.error(f"Error al ejecutar amass: {e}")
#         return render_template('result.html', error=f"Error al ejecutar amass: {e}")

#     return render_template('result.html', subdomains=subdomains)








# @app.route('/theharvester', methods=['POST']) NO FUNCIONA HARVESTER
# def theharvester():
#     domain = request.form.get('domain')
#     if not domain:
#         return render_template('resultTheHarvester.html', error='Dominio no proporcionado')

#     try:
#         result = subprocess.run(['python', THE_HARVESTER_PATH, '-d', domain, '-b', 'bing'], capture_output=True, text=True)
#         output = result.stdout
#         emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', output)
#     except Exception as e:
#         logging.error(f"Error al ejecutar The Harvester: {e}")
#         return render_template('resultTheHarvester.html', error=f"Error al ejecutar The Harvester: {e}")

#     return render_template('resultTheHarvester.html', emails=emails)

