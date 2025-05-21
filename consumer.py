import json
import base64
import os
import boto3

sns_client = boto3.client('sns')

# Substitua pelo ARN real do seu tópico SNS
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:XXXXXXXXXXXX:btc-alerta'

# Limite configurável por variável de ambiente
PRICE_THRESHOLD = float(os.environ.get('PRICE_THRESHOLD', 100000))

def lambda_handler(event, context):
    if 'Records' not in event:
        print("No records found.")
        return {
            'statusCode': 400,
            'body': json.dumps('No records found in the event')
        }

    for record in event['Records']:
        try:
            # Decodifica o dado base64
            payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            data = json.loads(payload)

            # Acessa o preço enviado pelo producer
            price = data.get("Price_usd", 0)

            print(f"Preço atual do BTC: {price}")

            # Se preço maior ou igual ao limite, envia alerta
            if price >= PRICE_THRESHOLD:
                message = f"ALERTA! Preço do Bitcoin passou de ${PRICE_THRESHOLD:.2f}\nPreço atual: ${price:.2f}"

                response = sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=message,
                    Subject='Alerta de Preço BTC'
                )

                print("Alerta enviado:", response)

        except Exception as ex:
            print(f"Erro ao processar registro: {ex}")

    return {
        'statusCode': 200,
        'body': json.dumps('Registros processados com sucesso')
    }
