# Em services/ticketing_api.py
import random

def create_ticket(summary: str, user_id: str, urgency: str = "medium"):
    """
    FAKE API: Simula a abertura de um ticket no Zendesk, Jira, etc.
    """
    # Simula a criação de um ID de ticket
    ticket_id = f"SUP-{random.randint(1000, 9999)}"
    
    print(f"\n[API_CALL_TICKETING] Criando ticket para {user_id} (Urgência: {urgency})")
    print(f"[API_CALL_TICKETING] Conteúdo do Resumo: {summary}")
    print(f"[API_CALL_TICKETING] ...Ticket {ticket_id} criado com sucesso!")
    
    # Retorna o número do ticket, o que é crucial para a demo
    return {"success": True, "data": {"ticket_id": ticket_id, "status": "open"}}