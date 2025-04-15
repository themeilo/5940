from flask import Flask, jsonify, request, render_template_string
import datetime

app = Flask(__name__)

estado_impresora = {
    "estado": "ONLINE",
    "mensaje_actual": "Caja Producto A",
    "tinta": "OK",
    "hora": datetime.datetime.now().strftime("%H:%M:%S"),
    "contadores": {},
    "variables": {},
    "mensajes_disponibles": []
}

historial = []

html_template = """
<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <title>Estado Impresora 5940G</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; }
        .card { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 0 10px #ccc; max-width: 500px; margin: auto; }
        h2 { color: #333; }
        .item { margin-bottom: 10px; }
    </style>
    <script>
        setTimeout(() => { window.location.reload(); }, 300000);
    </script>
</head>
<body>
    <div class=\"card\">
        <h2>Estado de la Impresora 5940G</h2>
        <div class=\"item\"><strong>Estado:</strong> {{ estado }}</div>
        <div class=\"item\"><strong>Mensaje actual:</strong> {{ mensaje_actual }}</div>
        <div class=\"item\"><strong>Tinta:</strong> {{ tinta }}</div>
        <div class=\"item\"><strong>Hora:</strong> {{ hora }}</div>
        <div class=\"item\"><a href=\"/ver_historial\">Ver historial</a></div>
    </div>
</body>
</html>
"""

historial_template = """
<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <title>Historial Impresora 5940G</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; }
        table { width: 95%; margin: auto; border-collapse: collapse; background: white; box-shadow: 0 0 10px #ccc; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: center; }
        th { background-color: #f0f0f0; }
        h2 { text-align: center; }
    </style>
</head>
<body>
    <h2>Historial de Estados - Impresora 5940G</h2>
    <table>
        <tr>
            <th>Hora</th>
            <th>Estado</th>
            <th>Mensaje</th>
            <th>Tinta</th>
            <th>Contadores</th>
            <th>Variables</th>
            <th>Mensajes disponibles</th>
        </tr>
        {% for item in historial %}
        <tr>
            <td>{{ item.hora }}</td>
            <td>{{ item.estado }}</td>
            <td>{{ item.mensaje_actual }}</td>
            <td>{{ item.tinta }}</td>
            <td>{{ item.contadores }}</td>
            <td>{{ item.variables }}</td>
            <td>{{ item.mensajes_disponibles }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/actualizar', methods=['POST'])
def actualizar_estado():
    global estado_impresora, historial
    data = request.json
    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
    estado_impresora = {
        "estado": data.get("estado", "UNKNOWN"),
        "mensaje_actual": data.get("mensaje_actual", "N/A"),
        "tinta": data.get("tinta", "DESCONOCIDO"),
        "hora": hora_actual,
        "contadores": data.get("contadores", {}),
        "variables": data.get("variables", {}),
        "mensajes_disponibles": data.get("mensajes_disponibles", [])
    }
    historial.append(estado_impresora.copy())
    return jsonify({"msg": "Estado actualizado"}), 200

@app.route('/estado', methods=['GET'])
def estado():
    return jsonify(estado_impresora)

@app.route('/historial', methods=['GET'])
def ver_historial_json():
    return jsonify(historial)

@app.route('/ver_historial')
def ver_historial_html():
    return render_template_string(historial_template, historial=historial)

@app.route('/')
def home():
    return render_template_string(html_template, **estado_impresora)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
