# Em agents/escalation_agent.py
import google.generativeai as genai
from config import GOOGLE_API_KEY
from services import ticketing_api # Importa a API de tickets

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def create_human_ticket(chat_history: list, last_query: str, user_id: str, diagnosis_attempt: str):
    """
    1. Usa IA para resumir o caso para um humano.
    2. Chama a API de tickets para registrar o chamado.
    """
    
    # 1. Usar IA (Gemini) para resumir o caso
    full_conversation = "\n".join(chat_history) + f"\nÚltima msg cliente: {last_query}"
    prompt_summary = f"""
    Resuma o seguinte chat de suporte em 1-2 frases para um atendente humano. 
    Seja direto e inclua o problema principal.
    
    Histórico:
    {full_conversation}
    
    Tentativa de diagnóstico automático (o que o bot tentou fazer):
    {diagnosis_attempt}
    
    Resumo para o atendente:
    """
    summary_response = model.generate_content(prompt_summary)
    summary = summary_response.text.strip()

    # 2. Chamar a API (fake) para criar o ticket
    ticket_result = ticketing_api.create_ticket(
        summary=summary, 
        user_id=user_id, 
        urgency="high"
    )

    # 3. Formular a resposta para o usuário com o número do ticket
    if ticket_result["success"]:
        ticket_id = ticket_result["data"]["ticket_id"]
        response_msg = (
            f"Não consegui resolver seu problema automaticamente. 😥\n"
            f"Mas não se preocupe! Acabei de abrir um chamado para nossa equipe humana.\n"
            f"**Seu número de ticket é: {ticket_id}**.\n\n"
            f"Nossa equipe recebeu este resumo: '{summary}'"
        )
        return response_msg
    else:
        return "Não consegui resolver e também falhei ao criar um ticket. Por favor, tente novamente mais tarde."