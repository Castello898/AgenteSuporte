import random

def save_feedback(user_id: str, rating: int, comment: str, sentiment: str):
    """
    FAKE API: Simula o salvamento do feedback em um banco de dados interno.
    """
    print(f"\n[API_CALL_DB] Salvando feedback de {user_id}...")
    print(f"[API_CALL_DB] Rating: {rating} | Sentimento: {sentiment} | Comentário: {comment}")
    print(f"[API_CALL_DB] ...Feedback salvo com ID: fb_{random.randint(100, 999)}")
    return {"success": True, "feedback_id": f"fb_{random.randint(100, 999)}"}