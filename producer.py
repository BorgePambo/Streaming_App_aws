import requests
import boto3
import json
from datetime import datetime  # Corrigido o import do datetime

REGION = "us-east-1"
STREAM_NAME = "broker"
kinesis = boto3.client("kinesis", region_name=REGION)

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

def lambda_handler(event, context):
    try:
        response = requests.get(url)
        data = response.json()
        
        price = data["bitcoin"]["usd"] 
        
        btc_data = {
            "Price_usd": price,
            "timestamp": datetime.utcnow().isoformat()  
        }
        
        kinesis.put_record(
            StreamName=STREAM_NAME,  
            Data=json.dumps(btc_data),  
            PartitionKey="btc"  
        )
        
        return {
            "StatusCode": 200,
            "body": json.dumps("Dados enviados com sucesso no Kinesis..!")
        }

    except Exception as ex:
        return {
            "StatusCode": 500,
            "body": json.dumps(f"Erro ao enviar dados: {str(ex)}")
        }
