from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest import mock

from django.core.management import call_command
from django.test import SimpleTestCase, override_settings


class BuildVectorStoreCommandTests(SimpleTestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.source_file = Path(self.tmpdir.name) / "doc.md"
        self.source_file.write_text("Contenido de ejemplo para pruebas.", encoding="utf-8")

    def test_dry_run_executes_without_errors(self) -> None:
        with override_settings(VECTORSTORE_DIR=Path(self.tmpdir.name) / "vs"):
            call_command(
                "build_vector_store",
                "--source",
                str(self.source_file),
                "--dry-run",
            )

    def test_command_persists_vector_store(self) -> None:
        os.environ["GEMINI_API_KEY"] = "fake-key"
        self.addCleanup(lambda: os.environ.pop("GEMINI_API_KEY", None))

        target_dir = Path(self.tmpdir.name) / "vectorstore"

        with override_settings(VECTORSTORE_DIR=target_dir):
            with mock.patch(
                "chat.management.commands.build_vector_store.create_embeddings"
            ) as mock_create, mock.patch(
                "chat.management.commands.build_vector_store.build_vector_store"
            ) as mock_build, mock.patch(
                "chat.management.commands.build_vector_store.save_vector_store"
            ) as mock_save:
                mock_create.return_value = object()
                mock_build.return_value = object()

                call_command(
                    "build_vector_store",
                    "--source",
                    str(self.source_file),
                    "--document-id",
                    "sample-doc",
                )

        mock_create.assert_called_once()
        mock_build.assert_called_once()
        mock_save.assert_called_once()
