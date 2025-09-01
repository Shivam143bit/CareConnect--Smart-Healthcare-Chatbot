import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import ChatSession, Message
from .services import get_chain
from .safety import is_emergency, requires_professional

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    @sync_to_async
    def _get_session(self, sid): return ChatSession.objects.get(pk=sid)

    @sync_to_async
    def _save(self, session, role, content):
        return Message.objects.create(session=session, role=role, content=content)

    async def receive(self, text_data):
        data = json.loads(text_data)
        session_id = data.get("session_id")
        question = (data.get("content") or "").strip()
        if not session_id or not question:
            await self.send(json.dumps({"error": "session_id and content required"}))
            return

        session = await self._get_session(session_id)
        await self._save(session, "user", question)

        if is_emergency(question):
            msg = "This may be an emergency. Please call your local emergency number or visit the nearest hospital."
            await self._save(session, "assistant", msg)
            await self.send(json.dumps({"type": "final", "content": msg}))
            return

        chain, _ = get_chain()
        history = [{"role": m.role, "content": m.content} async for m in session.messages.order_by("created_at").aiterator()]

        # Fallback: generate full then send; for true token streaming, wrap the LLM call that supports it
        result = await sync_to_async(chain.invoke)({"question": question, "history": history})
        if requires_professional(question):
            result += "\n\nNote: For medications, dosages, or diagnosis, please see a licensed clinician."
        await self._save(session, "assistant", result)
        await self.send(json.dumps({"type": "final", "content": result, "ts": timezone.now().isoformat()}))
