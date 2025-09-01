from django.db import transaction
from .models import ChatSession, Message
from .safety import is_emergency, requires_professional
from .llm import build_chain

_chain_cache = None

def get_chain():
    global _chain_cache
    if _chain_cache is None:
        _chain_cache = build_chain()
    return _chain_cache

DISCLAIMER_REPLY = (
    "I can share general health information, not a diagnosis or prescription. "
    "For specific medical advice, please consult a licensed clinician."
)

def run_inference(session: ChatSession, user_text: str) -> str:
    emergency = is_emergency(user_text)
    if emergency:
        response = (
            "This may be an emergency. Please call your local emergency number or go to the nearest hospital now."
        )
        _store(session, "assistant", response)
        return response

    professional_needed = requires_professional(user_text)

    chain, _ = get_chain()
    history = [{"role": m.role, "content": m.content} for m in session.messages.order_by("created_at")[:10]]

    result = chain.invoke({"question": user_text, "history": history})
    if professional_needed:
        result += "\n\nNote: For medications, dosages, or diagnosis, please see a licensed clinician."

    _store(session, "assistant", result)
    return result

@transaction.atomic
def _store(session: ChatSession, role: str, content: str):
    Message.objects.create(session=session, role=role, content=content)

def start_session(title: str | None = None) -> ChatSession:
    s = ChatSession.objects.create(title=title or "Medical chat")
    Message.objects.create(session=s, role="system", content=DISCLAIMER_REPLY)
    return s
