from flask import Flask, render_template, request, redirect, url_for
import mercadopago

app = Flask(__name__)

# Configura tu clave de acceso a MercadoPago
mp = mercadopago.MP("APP_USR-4635163528194726-081114-947d66a69ac58b5d9ca17c18de0eeb4e-1071307545")

@app.route('/')
def index():
    return render_template('formulario_pago.html')

@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    # Obtén los datos del formulario
    nombre_apellido = request.form.get('nombre_apellido')
    telefono = request.form.get('telefono')
    email = request.form.get('email')
    motivo = request.form.get('motivo')
    monto = float(request.form.get('amount'))  # Asegúrate de manejar correctamente el monto
    descripcion = request.form.get('description')

    # Crea un ítem para la preferencia de MercadoPago
    item = {
        'title': motivo,
        'quantity': 1,
        'currency_id': 'ARS',  # Moneda (puede cambiar según tu configuración)
        'unit_price': monto,
    }

    # Crea la preferencia de pago
    preference = {
        'items': [item],
        'payer': {
            'name': nombre_apellido,
            'email': email,
        },
        'back_urls': {
            'success': url_for('exito', _external=True),
            'pending': url_for('pendiente', _external=True),
            'failure': url_for('fracaso', _external=True),
        },
    }

    # Crea la preferencia y obtén la URL de pago
    preference_result = mp.create_preference(preference)
    payment_url = preference_result['response']['sandbox_init_point']  # Usa 'init_point' en producción

    #Redirige al usuario a la página de pago de MercadoPago
    return redirect(payment_url)

# Rutas adicionales para manejar redirecciones de MercadoPago
@app.route('/exito')
def exito():
    return render_template('exito.html')  # Página de éxito

@app.route('/pendiente')
def pendiente():
    return render_template('pendiente.html')  # Página de estado pendiente

@app.route('/fracaso')
def fracaso():
    return render_template('fracaso.html')  # Página de fallo

if __name__ == '__main__':
    app.run(debug=True)
