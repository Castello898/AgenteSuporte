# Em agents/initial_agent.py
import google.generativeai as genai
from config import GOOGLE_API_KEY
from services import crm_api # Importa a nova API fake

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def greet_and_classify(user_id: str, query: str):
    """
    1. Busca dados do cliente na API do CRM.
    2. Usa o Gemini para classificar a intenção da consulta.
    """
    
    # 1. Chamar a API (fake) do CRM
    customer_name = "cliente" # Nome padrão
    crm_data = crm_api.get_customer_details(user_id)
    if crm_data["success"]:
        # Pega o primeiro nome para ser mais pessoal
        customer_name = crm_data["data"]["name"].split(" ")[0] 

    # 2. Usar IA (Gemini) para classificar a intenção
    prompt = f"""
    Classifique a seguinte dúvida de cliente em UMA das categorias: 
    'shipping' (frete/pedido), 
    'billing' (fatura/pagamento), 
    'technical' (problema técnico/bug), 
    'other' (outros).
    
    Dúvida: "{query}"
    
    Responda APENAS a categoria.
    """
    response = model.generate_content(prompt)
    # Limpa a resposta para ter apenas a categoria
    intent = response.text.strip().lower().replace("'", "").replace("\"", "")

    print(f"[AGENT_INITIAL] Intenção detectada: {intent}")

    # 3. Gerar uma saudação personalizada
    greeting = f"Olá {customer_name}! 👋 Vi que você é um cliente {crm_data['data']['level']}. Recebi sua mensagem sobre: '{query}'. Estou direcionando seu caso..."
    
    # Retorna a saudação (para o usuário) e a intenção (para o orquestrador)
    return greeting, intent