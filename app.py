from flask import Flask, render_template, jsonify, request
import requests
import subprocess
import logging
import re

app = Flask(__name__) #INICIO DE LA FUNCIÓN PARA LLAMAR
app.config['DEBUG'] = True  # Activar el modo de depuración

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

# Ruta completa al ejecutable de amass
#AMASS_PATH = "C:/Users/Ricardo/Downloads/amass_Windows_amd64/amass_Windows_amd64/amass.exe"  # Cambia esto según tu ruta
#THE_HARVESTER_PATH = 'C:/Users/Ricardo/Documents/SeguridadInformatica/theHarvester/theHarvester.py'

@app.route('/')
def home():
    return render_template('index.html') #LLAMAR AL TEMPLATE INDEX.HTML
#############################################################

@app.route('/assetfinder', methods=['POST']) ## LLAMADA A LA APLICACIÓN DE SEGURIDADA ASSETFINDER
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

################################################
@app.route('/subdominios', methods=['POST']) ##PRIERA FUNCI[ON LLAMADNO A UNA API
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
        response.raise_for_status()  # Lanza una excepción para respuestas de error HTTP
        response_data = response.json()
        subdomains = response_data.get('subdomains', [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al llamar a la API de RapidAPI: {e}")
        return render_template('resultApiSubdomain.html', error=f"Error al llamar a la API de RapidAPI: {e}")
    except Exception as e:
        logging.error(f"Error general: {e}")
        return render_template('resultApiSubdomain.html', error=str(e))

    return render_template('resultApiSubdomain.html', subdomains=subdomains)


######################################################################################
@app.route('/whois', methods=['POST']) #FUNCION LLAMADA API WHOIS TOCA SEGUIR VIENDO
def whois():
    domain = request.form.get('domain')
    if not domain:
        return render_template('resultadosWhois.html', error='Dominio no proporcionado')

    try:
        url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
        params = {
            "apiKey": "at_gSMULVtWXXr4wff94NqNFOBUGZXK4",  # Reemplaza esto con tu API key
            "domainName": domain,
            "outputFormat": "JSON"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanza una excepción para respuestas de error HTTP
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al llamar a la API de WHOISXML: {e}")
        return render_template('resultadosWhois.html', error=f"Error al llamar a la API de WHOISXML: {e}")
    except Exception as e:
        logging.error(f"Error general: {e}")
        return render_template('resultadosWhois.html', error=str(e))

    return render_template('resultadosWhois.html', whois_data=response_data)




# @app.route('/theharvester', methods=['POST']) NO FUNCIONA 
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

if __name__ == "__main__":
    app.run(debug=True)
