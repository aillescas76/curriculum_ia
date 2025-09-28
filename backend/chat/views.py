from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ChatRequestSerializer, ChatResponseSerializer


class ChatView(APIView):
    """Simple placeholder chatbot endpoint returning canned responses."""

    def post(self, request, *args, **kwargs):  # noqa: D401
        request_serializer = ChatRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        message = request_serializer.validated_data["message"].strip()
        reply = (
            "Esta es una versión inicial del chatbot. "
            "Todavía no tengo acceso al vector store ni a Gemini, pero ya recibí tu pregunta: "
            f"\"{message}\"."
        )

        response_payload = {
            "reply": reply,
            "suggested_questions": [
                "¿Qué habilidades técnicas domina?",
                "Háblame de sus proyectos recientes.",
                "¿Cuál es su experiencia con IA?",
            ],
        }
        response_serializer = ChatResponseSerializer(data=response_payload)
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
