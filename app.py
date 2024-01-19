from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pay', methods=['POST'])
def pay():
    # Lógica de procesamiento de pago aquí (integra con pasarelas de pago reales)

    # Ejemplo de datos recibidos desde el formulario
    amount = request.form['amount']
    description = request.form['description']

    return render_template('payment_confirmation.html', amount=amount, description=description)

if __name__ == '__main__':
    app.run(debug=True)