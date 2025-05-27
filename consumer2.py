import boto3
import base64
import os
import json

sns_client = boto3.client("sns")

# Pega o valor padrão de uma variável de ambiente ou usa 100.0 como default
DEFAULT_PRICE = float(os.environ.get("DEFAULT_PRICE", 100.0))
TOPIC_ARN = "arn:aws:sns:region:account-id:topic-name"  # Substitua pelo ARN correto


def lambda_handler(event, context):
    try:
        records = event.get("Records", [])
        
        if not records:
            print("No records found.")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "No records found."})
            }

        for record in records:
            # Decodifica o payload do Kinesis
            encoded_data = record["kinesis"]["data"]
            decoded_data = base64.b64decode(encoded_data).decode("utf-8")
            
            # Converte o JSON para dicionário
            data = json.loads(decoded_data)
            
            price = float(data.get("Price", 0))

            # Verifica se o preço excedeu o limite
            if price > DEFAULT_PRICE:
                msg = f"The price has just passed {DEFAULT_PRICE}. The current price is {price}."

                # Publica no tópico SNS
                sns_client.publish(
                    TopicArn=TOPIC_ARN,
                    Message=msg,
                    Subject="Price Alert!"
                )
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Processed successfully!"})
        }

    except Exception as e:
        print(f"Error processing records: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Processing failed: {str(e)}"})
        }