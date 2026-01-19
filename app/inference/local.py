"""
Local, offline language model implementation.
"""

import time
import threading
from typing import Iterator

from transformers import pipeline

from app.inference.base import LanguageModel
from app.reliability.timeouts import time_limit
from app.reliability.errors import TimeoutError


class LocalSummarizationModel(LanguageModel):
    """
    Local summarization model using Hugging Face transformers.

    Design goals:
    - Offline-first
    - CPU-safe by default
    - Hard timeout enforcement
    - Deterministic behavior
    """

    def __init__(self, model_name: str = "google/flan-t5-small"):
        self._model_name = model_name
        self._pipeline = pipeline(
            task="summarization",
            model=model_name,
            tokenizer=model_name,
            device=-1,  # CPU by default
        )

    def generate(
        self,
        prompt: str,
        max_tokens: int,
        timeout_s: float,
    ) -> str:
        """
        Run summarization with hard timeout enforcement.
        """

        result = {}
        exception = {}

        def _run():
            try:
                output = self._pipeline(
                    prompt,
                    max_length=max_tokens,
                    truncation=True,
                )
                result["text"] = output[0]["summary_text"]
            except Exception as e:
                exception["error"] = e

        thread = threading.Thread(target=_run)

        try:
            with time_limit(int(timeout_s)):
                thread.start()
                thread.join()
        except TimeoutError:
            return "Summary generation timed out."

        if thread.is_alive():
            return "Summary generation timed out."

        if "error" in exception:
            return "Summary generation failed."

        return result.get("text", "")

    def generate_stream(
        self,
        prompt: str,
        max_tokens: int,
        timeout_s: float,
    ) -> Iterator[str]:
        """
        Sentence-level streaming generation.
        """

        start_time = time.time()
        full_summary = self.generate(prompt, max_tokens, timeout_s)

        if not full_summary:
            yield ""
            return

        sentences = full_summary.split(". ")
        for sentence in sentences:
            if time.time() - start_time > timeout_s:
                yield "[Generation timed out]"
                return

            yield sentence.strip()
            if not sentence.endswith("."):
                yield ". "
            else:
                yield " "
