from fastapi import FastAPI
from pydantic import BaseModel
from agents import initial_agent, diagnosis_agent, escalation_agent, feedback_agent
from services import crm_api, ticketing_api, internal_db # Importamos só para garantir

app = FastAPI(
    title="Customer Support App",
    description="Sistema de atendimento automatizado com orquestração de agentes de IA."
)

# --- Modelos de Requisição (Entrada) ---
class SupportRequest(BaseModel):
    user_id: str
    query: str
    chat_history: list = [] # Opcional: para manter o contexto

class FeedbackRequest(BaseModel):
    user_id: str
    rating: int # Ex: 1 a 5
    comment: str

# --- Modelos de Resposta (Saída) ---
class SupportResponse(BaseModel):
    response_text: str
    status: str # Ex: "resolved", "escalated", "awaiting_info"
    intent: str # A intenção que o agente inicial detectou

class FeedbackResponse(BaseModel):
    response_text: str


# --- Ponto 1: O FLUXO PRINCIPAL DE SUPORTE ---
@app.post("/support", response_model=SupportResponse)
async def handle_support(request: SupportRequest):
    """
    Este é o orquestrador principal.
    Ele decide qual agente chamar em sequência.
    """
    print(f"\n--- NOVA REQUISIÇÃO /support DE {request.user_id} ---")
    
    # 1. AGENTE INICIAL: Sempre executa primeiro.
    # Ele chama a API do CRM e classifica a intenção.
    (greeting, intent) = initial_agent.greet_and_classify(
        user_id=request.user_id, 
        query=request.query
    )
    
    # Adiciona a saudação ao histórico para os próximos agentes
    current_history = request.chat_history + [f"Bot (Inicial): {greeting}"]
    
    # 2. ORQUESTRAÇÃO: Decide o próximo passo baseado na intenção.
    
    # Se for "shipping", tentamos o diagnóstico automático
    if intent == "shipping":
        print("[ORQUESTRADOR] Intenção 'shipping'. Chamando Agente de Diagnóstico...")
        (diag_response, resolved) = diagnosis_agent.analyze_problem(
            user_query=request.query, 
            chat_history=current_history
        )
        
        # 2a. Problema resolvido pelo diagnóstico!
        if resolved:
            print("[ORQUESTRADOR] Problema RESOLVIDO pelo Agente de Diagnóstico.")
            full_response = f"{greeting}\n\n{diag_response}"
            return SupportResponse(
                response_text=full_response, 
                status="resolved", 
                intent=intent
            )
        
        # 2b. Diagnóstico falhou, precisamos escalar.
        else:
            print("[ORQUESTRADOR] Diagnóstico FALHOU. Chamando Agente de Escalonamento...")
            escalation_response = escalation_agent.create_human_ticket(
                chat_history=current_history,
                last_query=request.query,
                user_id=request.user_id,
                diagnosis_attempt=diag_response # Informa o que o bot anterior tentou
            )
            full_response = f"{greeting}\n\n{diag_response}\n\n{escalation_response}"
            return SupportResponse(
                response_text=full_response, 
                status="escalated", 
                intent=intent
            )

    # Se for "billing", "technical" ou "other", escalamos diretamente
    else:
        print(f"[ORQUESTRADOR] Intenção '{intent}'. Chamando Agente de Escalonamento direto...")
        escalation_response = escalation_agent.create_human_ticket(
            chat_history=current_history,
            last_query=request.query,
            user_id=request.user_id,
            diagnosis_attempt="Nenhuma, escalado diretamente pela intenção."
        )
        full_response = f"{greeting}\n\n{escalation_response}"
        return SupportResponse(
            response_text=full_response, 
            status="escalated", 
            intent=intent
        )


# --- Ponto 2: O FLUXO DE FEEDBACK ---
@app.post("/feedback", response_model=FeedbackResponse)
async def handle_feedback(request: FeedbackRequest):
    """
    Endpoint separado para demonstrar o Agente de Feedback.
    Ele analisa o sentimento e salva no DB (fake).
    """
    print(f"\n--- NOVA REQUISIÇÃO /feedback DE {request.user_id} ---")
    
    response = feedback_agent.process_feedback(
        user_id=request.user_id,
        rating=request.rating,
        comment=request.comment
    )
    
    return FeedbackResponse(response_text=response)

# Comando para rodar (lembre-se):
# uvicorn main:app --reload