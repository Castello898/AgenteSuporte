# Em agents/feedback_agent.py
import google.generativeai as genai
from config import GOOGLE_API_KEY
from services import internal_db # Importa a API do DB

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def process_feedback(user_id: str, rating: int, comment: str):
    """
    1. Usa IA para analisar o sentimento do feedback.
    2. Salva o feedback na API (fake) do banco de dados.
    """
    
    # 1. Usar IA (Gemini) para analisar o sentimento
    prompt = f"""
    Analise o sentimento do seguinte feedback (escala 1-5):
    Nota: {rating}
    Comentário: "{comment}"
    
    Responda apenas com 'positivo', 'negativo' ou 'neutro'.
    """
    sentiment_response = model.generate_content(prompt)
    sentiment = sentiment_response.text.strip().lower().replace("'", "").replace("\"", "")
    
    print(f"[AGENT_FEEDBACK] Sentimento detectado: {sentiment}")

    # 2. Chamar a API (fake) para salvar no DB
    db_result = internal_db.save_feedback(user_id, rating, comment, sentiment)
    
    if db_result["success"]:
        return (f"Obrigado pelo seu feedback (Nota: {rating})!\n"
                f"Nosso sistema detectou um sentimento **{sentiment}** e registrou seu comentário.")
    else:
        return "Obrigado, mas tivemos um problema ao salvar seu feedback."