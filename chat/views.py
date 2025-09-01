# chat/views.py
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import logging

logger = logging.getLogger(__name__)

# This view serves the chatbot page (chat.html)
class ChatPageView(TemplateView):
    template_name = "chat.html"   # make sure chat.html is inside templates/

# This view handles AJAX chat messages (POST)
@method_decorator(csrf_protect, name="dispatch")
class ChatApiView(View):
    def post(self, request, *args, **kwargs):
        try:
            user_message = request.POST.get("message", "").strip()

            if not user_message:
                return JsonResponse({"error": "Empty message"}, status=400)

            # Example chatbot logic (replace with LLM later)
            if "hello" in user_message.lower():
                bot_response = "Hello! I’m your medical chatbot. How can I help you today?"
            elif "fever" in user_message.lower():
                bot_response = "Fever is often a sign of infection. Drink fluids, rest, and consult a doctor if it persists."
            else:
                bot_response = "I can only provide general health info. Please consult a doctor for medical advice."

            return JsonResponse({"response": bot_response}, status=200)

        except Exception as e:
            logger.error(f"ChatApiView error: {e}")
            return JsonResponse({"error": "Something went wrong. Try again."}, status=500)
