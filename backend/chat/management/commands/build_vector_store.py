from __future__ import annotations

import os
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from chat.vectorstore import (
    build_vector_store,
    chunk_documents,
    create_embeddings,
    load_documents,
    save_vector_store,
    slugify,
)


class Command(BaseCommand):
    help = "Build or update the FAISS vector store from sanitized documents."

    def add_arguments(self, parser):
        parser.add_argument("--source", required=True, help="File or directory with documents")
        parser.add_argument("--document-id", help="Identifier to tag the ingested documents")
        parser.add_argument("--output", help="Directory where the vector store will be saved")
        parser.add_argument("--chunk-size", type=int, default=int(os.environ.get("CHUNK_SIZE", 500)))
        parser.add_argument(
            "--chunk-overlap", type=int, default=int(os.environ.get("CHUNK_OVERLAP", 80))
        )
        parser.add_argument("--model", help="Embedding model identifier")
        parser.add_argument("--dry-run", action="store_true", help="Process documents without writing the index")
        parser.add_argument("--rebuild", action="store_true", help="Overwrite any existing index")

    def handle(self, *args, **options):
        source = Path(options["source"]).resolve()
        if not source.exists():
            raise CommandError(f"Source path not found: {source}")

        base_output = options.get("output") or getattr(settings, "VECTORSTORE_DIR", None)
        if base_output is None:
            base_output = settings.BASE_DIR / "vectorstore-data"
        base_output = Path(base_output).resolve()

        document_id = options.get("document_id") or slugify(source.stem)
        chunk_size = options["chunk_size"]
        chunk_overlap = options["chunk_overlap"]
        dry_run = options["dry_run"]
        rebuild = options["rebuild"]
        model_name = options.get("model")

        start = time.perf_counter()

        try:
            documents = load_documents(source, document_id=document_id)
        except Exception as exc:
            raise CommandError(f"Failed to load documents: {exc}") from exc

        chunks = chunk_documents(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        if not chunks:
            raise CommandError("No chunks generated from the provided documents")

        for index, chunk in enumerate(chunks):
            chunk.metadata.setdefault("document_id", document_id)
            chunk.metadata.setdefault("source", chunk.metadata.get("source", str(source)))
            chunk.metadata["chunk_id"] = index

        elapsed = time.perf_counter() - start
        self.stdout.write(
            self.style.NOTICE(
                f"Loaded {len(documents)} document(s) and generated {len(chunks)} chunks in {elapsed:.2f}s"
            )
        )

        if dry_run:
            return

        try:
            embeddings = create_embeddings(model=model_name)
        except Exception as exc:
            raise CommandError(f"Failed to initialise embeddings: {exc}") from exc

        try:
            vector_store = build_vector_store(chunks, embeddings)
        except Exception as exc:
            raise CommandError(f"Failed to build vector store: {exc}") from exc

        target_dir = base_output / document_id
        try:
            save_vector_store(vector_store, target_dir, rebuild=rebuild)
        except Exception as exc:
            raise CommandError(f"Failed to save vector store: {exc}") from exc

        total = time.perf_counter() - start
        self.stdout.write(
            self.style.SUCCESS(
                f"Vector store saved to {target_dir} ({len(chunks)} chunks, total {total:.2f}s)"
            )
        )
