from flask import Flask, request, jsonify, render_template_string
import time
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
leituras = {} 

@app.route("/leitura", methods=["POST"])
def receber_leitura():
    dados = request.json
    agora = agora = datetime.now(pytz.timezone("America/Sao_Paulo"))
    dados["timestamp"] = agora.strftime("%H:%M:%S")
    dados["datetime"] = agora.isoformat()
    sensor_id = dados.get("sensor_id", "desconhecido")

    leituras[sensor_id] = dados

    return {"status": "ok"}

@app.route("/dados")
def dados():
    agora = datetime.now(pytz.timezone("America/Sao_Paulo"))
    dados_atualizados = []
    for sensor_id, dado in leituras.items():
        ultimo_envio = datetime.fromisoformat(dado["datetime"])
        ativo = (agora - ultimo_envio) < timedelta(seconds=5)
        dado["ativo"] = ativo
        dados_atualizados.append(dado)

    dados_ordenados = sorted(
        dados_atualizados,
        key=lambda d: (not d["ativo"], d["tipo"])
    )

    return jsonify(dados_ordenados)

@app.route("/painel")
def painel():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Painel de Sensores</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; padding: 20px; background: #f4f4f4; }
        table { border-collapse: collapse; width: 100%; background: white; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background-color: #007BFF; color: white; }
        h1 { color: #333; }
        .ativo { background-color: #c8f7c5; }
        .inativo { background-color: #f7c5c5; }
    </style>
</head>
<body>
    <h1>Painel de Leituras dos Sensores</h1>
    <table id="tabela">
        <thead>
            <tr>
                <th>Horário</th>
                <th>Sensor ID</th>
                <th>Tipo</th>
                <th>Valor</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
        async function carregarDados() {
            const res = await fetch("/dados");
            const dados = await res.json();
            const tbody = document.querySelector("#tabela tbody");
            tbody.innerHTML = "";
            dados.forEach(l => {
                const classe = l.ativo ? "ativo" : "inativo";
                const linha = `<tr>
                    <td>${l.timestamp}</td>
                    <td class="${classe}">${l.sensor_id}</td>
                    <td>${l.tipo}</td>
                    <td>${l.valor}</td>
                </tr>`;
                tbody.innerHTML += linha;
            });
        }

        setInterval(carregarDados, 1000);
        carregarDados();
    </script>
</body>
</html>
    """)

app.run(host="0.0.0.0", port=5000)
