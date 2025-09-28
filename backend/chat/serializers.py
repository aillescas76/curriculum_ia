from __future__ import annotations

from typing import Any

from rest_framework import serializers


class ConversationTurnSerializer(serializers.Serializer):
    """Serializes prior conversation turns so we can stub memory handling now."""

    role = serializers.ChoiceField(choices=("user", "assistant", "system"))
    content = serializers.CharField(allow_blank=False)


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=False)
    history = ConversationTurnSerializer(many=True, required=False, default=list)

    def to_internal_value(self, data: Any) -> dict[str, Any]:
        validated = super().to_internal_value(data)
        # Ensure history defaults to a list instead of DRF's Empty structure.
        validated.setdefault("history", [])
        return validated


class ChatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()
    suggested_questions = serializers.ListField(
        child=serializers.CharField(), allow_empty=True, default=list
    )
