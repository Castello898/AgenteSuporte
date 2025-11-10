import requests
from config import SHIPPING_API_URL, SHIPPING_API_KEY

def get_order_status(order_id: str):
    """
    Busca o status de um pedido na API de transporte.
    (Esta é uma implementação de exemplo)
    """
    try:
        headers = {"Authorization": f"Bearer {SHIPPING_API_KEY}"}
        response = requests.get(f"{SHIPPING_API_URL}/status/{order_id}", headers=headers)

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": "Pedido não encontrado ou API falhou."}
            
    except Exception as e:
        return {"success": False, "error": f"Erro de conexão: {e}"}