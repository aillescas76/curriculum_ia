from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ChatEndpointTests(APITestCase):
    def test_returns_placeholder_reply(self) -> None:
        response = self.client.post(
            reverse("chat:chat"),
            {"message": "¿Cuál es su experiencia?"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "reply" in response.data
        assert "pregunta" in response.data["reply"].lower()

    def test_requires_message_field(self) -> None:
        response = self.client.post(reverse("chat:chat"), {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "message" in response.data
