"""
Centralized hard limits enforced by the system.
These are guarantees, not suggestions.
"""

MAX_DOCUMENT_CHARS = 50_000          # prevents memory abuse
MAX_CHUNKS = 20
CHUNK_SIZE_CHARS = 1_000
MAX_QUERY_CHARS = 500

MAX_INPUT_TOKENS_ESTIMATE = 1_500    # conservative estimate
MAX_OUTPUT_TOKENS = 300
