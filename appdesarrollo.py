import subprocess
import re
from flask import Flask, render_template, request

app = Flask(__name__)

def run_theharvester(domain):
    # Especificar la ruta completa al script de TheHarvester
    command = f'python C:/Users/Ricardo/Documents/SeguridadInformatica/theHarvester/theHarvester.py -d {domain} -b bing'
    result = subprocess.run(command.split(), capture_output=True, text=True)
    return result.stdout

def extract_emails(output):
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    return email_pattern.findall(output)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form['domain']
        try:
            output = run_theharvester(domain)
            emails = extract_emails(output)
            return render_template('resultdesarollo.html', emails=emails)
        except Exception as e:
            app.logger.error(f"Error: {e}")
            return render_template('resultdesarollo.html', error=str(e))
    return render_template('indexdesarrollo.html')

if __name__ == '__main__':
    app.run(debug=True)
