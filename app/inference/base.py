"""
Abstract interface for all language model implementations.
"""

from abc import ABC, abstractmethod
from typing import Iterator


class LanguageModel(ABC):
    """
    Contract for bounded, synchronous language model inference.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: int,
        timeout_s: float,
    ) -> str:
		pass
		
        """
        Generate text from a prompt.

        Guarantees:
        - Must respect max_tokens
        - Must respect timeout_s
        - Must never raise raw model exceptions
        """

    def generate_stream(
        self,
        prompt: str,
        max_tokens: int,
        timeout_s: float,
    ) -> Iterator[str]:
        """
        Optional streaming generation.
        Default: yield full output as a single chunk.
        """
        yield self.generate(prompt, max_tokens, timeout_s)
