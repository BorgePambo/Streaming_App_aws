# AWS Lambda - Bitcoin Price to Kinesis

Esta função AWS Lambda coleta o preço atual do **Bitcoin (BTC)** em dólares americanos (USD) usando a **API pública da CoinGecko** e envia esses dados para um **Amazon Kinesis Data Stream** chamado `broker`.

## 🔧 Tecnologias Utilizadas

- Python 3.x
- AWS Lambda
- Amazon Kinesis Data Streams
- Boto3 (SDK da AWS para Python)
- CoinGecko API (https://www.coingecko.com/en/api)

## ⚙️ Como Funciona

1. A função é acionada (por evento, cron job, etc.).
2. Faz uma requisição HTTP para a API da CoinGecko.
3. Extrai o preço do Bitcoin em USD.
4. Adiciona um timestamp (UTC).
5. Envia os dados para o Kinesis Data Stream no formato JSON.

### Exemplo de dado enviado para o Kinesis:

```json
{
  "Price_usd": 67123.45,
  "timestamp": "2025-05-21T14:32:10.123456"
}



Objetivo do código:
Uma função Lambda que age como consumer do Kinesis, verifica o preço do Bitcoin, e se o valor ultrapassar um limite, envia um alerta por e-mail usando SNS.

Tecnologias e Serviços

- AWS Lambda
- Amazon Kinesis
- Amazon SNS
- Python 3.9+
- API do CoinGecko

---

## 🛠️ Configuração

### 1. Variáveis de Ambiente no Lambda (Consumer)

| Nome                     | Descrição                              | Exemplo       |
|--------------------------|------------------------------------------|---------------|
| `PRICE_THRESHOLD`        | Preço limite do BTC para alertar         | `100000`      |

---

### 2. Producer (exemplo)

Função Lambda (ou script Python) que consome a API do CoinGecko e envia os dados para o Kinesis.

```python
import requests
import boto3
import json
import datetime

kinesis = boto3.client("kinesis", region_name="us-east-1")
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

def lambda_handler(event, context):
    response = requests.get(url)
    price = response.json()["bitcoin"]["usd"]
    data = {
        "Price_usd": price,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    kinesis.put_record(
        StreamName="broker",
        Data=json.dumps(data),
        PartitionKey="btc"
    )
    return {"statusCode": 200, "body": "Preço enviado"}
