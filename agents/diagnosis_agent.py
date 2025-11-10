import google.generativeai as genai
from config import GOOGLE_API_KEY
from services import shipping_api # Importamos nosso serviço!

# Configura o modelo Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') # Substitui o "gemini-2.5-pro"

def analyze_problem(user_query: str, chat_history: list):
    """
    Tenta diagnosticar e resolver o problema do cliente.
    """
    
    # 1. Usar IA para extrair dados (Ex: ID do Pedido)
    prompt_extract = f"""
    Histórico da conversa: {chat_history}
    Última mensagem do usuário: "{user_query}"
    
    Analise a mensagem. Se for um problema de "pedido não chegou", 
    extraia o NÚMERO DO PEDIDO. 
    Responda APENAS com o número do pedido. Se não encontrar, responda "N/A".
    """
    
    response_extract = model.generate_content(prompt_extract)
    order_id = response_extract.text.strip()

    # 2. Se for um problema de pedido, usar nossa API!
    if order_id != "N/A":
        # Chama a API de serviço que criamos!
        api_result = shipping_api.get_order_status(order_id)
        
        if api_result["success"]:
            # 3. Usar IA para formatar a resposta da API
            api_data = api_result["data"]
            prompt_format = f"""
            O cliente perguntou sobre o pedido {order_id}.
            Os dados da API de transporte são: {api_data}
            
            Formule uma resposta amigável e útil para o cliente.
            (Ex: "Verifiquei aqui e seu pedido {order_id} está com a transportadora...")
            """
            final_response = model.generate_content(prompt_format)
            return final_response.text, True # True = Problema resolvido
        
        else:
            # A API falhou, mas o Gemini pode explicar
            return "Não consegui encontrar os dados do seu pedido no sistema da transportadora. Você pode confirmar o número, por favor?", False

    # 4. Se não for problema de pedido, tenta diagnóstico genérico
    prompt_generic = f"""
    Responda à seguinte dúvida de suporte: "{user_query}"
    Se for um problema técnico complexo, sugira que o usuário 
    descreva melhor o problema para que possamos analisar.
    """
    generic_response = model.generate_content(prompt_generic)
    return generic_response.text, False # False = Não resolvido, precisa escalar