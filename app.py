from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# --- НАСТРОЙКИ ДЛЯ ИМИТАЦИИ ---
# Балансы в wei (1 ETH = 10^18 wei). Для BTC и BNB используем 18 decimals.
FAKE_BALANCES = {
    "ETH": hex(10 * 10**18),  # 10 ETH
    "BTC": hex(5 * 10**18),   # 5 BTC
    "BNB": hex(100 * 10**18), # 100 BNB
}

FAKE_STAKING_HISTORY = [
    {"type": "Staking", "amount": "-2.5 ETH", "status": "Completed"},
    {"type": "Staking", "amount": "-1.0 BTC", "status": "Completed"},
]

@app.route('/', methods=['POST'])
def handle_rpc():
    data = request.get_json()
    if not data:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})

    method = data.get('method')
    params = data.get('params', [])
    req_id = data.get('id')

    print(f"Получен запрос: {method} с параметрами {params}")

    # 1. Баланс кошелька (самый важный запрос)
    if method == 'eth_getBalance':
        # Возвращаем баланс ETH по умолчанию
        result = FAKE_BALANCES["ETH"]
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

    # 2. Номер последнего блока
    elif method == 'eth_blockNumber':
        result = hex(12345678)
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

    # 3. Информация о сети (Chain ID)
    elif method == 'net_version':
        result = "31337"
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

    # 4. Количество транзакций (для nonce)
    elif method == 'eth_getTransactionCount':
        result = hex(0)
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

    # 5. Заглушка для истории транзакций (логов)
    elif method == 'eth_getLogs':
        # Возвращаем пустой список, чтобы не было ошибки
        result = []
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

    # 6. Имитация вызовов к смарт-контракту (для стейкинга и токенов)
    elif method == 'eth_call':
        # Здесь можно добавить логику для разных токенов (BTC, BNB)
        # Пока возвращаем баланс по умолчанию
        result = FAKE_BALANCES["ETH"]
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

    else:
        print(f"Метод {method} не реализован, возвращаем заглушку.")
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x0"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)