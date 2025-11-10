# Em services/crm_api.py

def get_customer_details(user_id: str):
    """
    FAKE API: Simula a busca de dados do cliente no CRM (Salesforce, Hubspot, etc.)
    """
    # Imprime no terminal para "provar" que a API foi chamada
    print(f"\n[API_CALL_CRM] Buscando dados do user_id: {user_id}...")
    
    # Simula diferentes usuários
    if user_id == "user-123":
        print("[API_CALL_CRM] ...Cliente 'Ana Silva' (Premium) encontrado.")
        return {"success": True, "data": {"name": "Ana Silva", "level": "premium", "open_tickets": 0}}
    elif user_id == "user-456":
        print("[API_CALL_CRM] ...Cliente 'Bruno Costa' (Standard) encontrado.")
        return {"success": True, "data": {"name": "Bruno Costa", "level": "standard", "open_tickets": 1}}
    else:
        print("[API_CALL_CRM] ...Cliente não encontrado.")
        return {"success": False, "error": "User not found"}