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
