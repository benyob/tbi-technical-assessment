# Document Analysis Prototype

**Offline-First, Reliable, and Auditable AI System**


## 1. Overview

This repository contains a production-oriented prototype for automated document analysis and summarization.
The system ingests long-form technical documents, answers natural-language queries, and generates bounded summaries under strict latency, cost, and stability constraints.

The design prioritizes:

- Trustworthiness over novelty

- Deterministic behavior over probabilistic cleverness

- Operational safety over model sophistication


## 2. Key Capabilities

- Browser-based UI (Chrome, Edge, Safari)

- Text upload or copy-paste (UTF-8 only)

- Natural-language querying

- Incremental (streamed) responses

- Visible chat history (user prompts + system responses)

- Clear error reporting without crashes

- Offline-first inference (no mandatory external APIs)

- Deterministic behavior under repeated usage

## 3. System Architecture
### 3.1 High-Level Flow:

```text
Browser UI
   ↓
FastAPI HTTP Layer
   ↓
Input Validation & Budget Enforcement
   ↓
Document Chunking & Retrieval
   ↓
Prompt Construction
   ↓
Local LLM Inference (Offline)
   ↓
Streaming / Response Assembly
````

Each stage is explicitly bounded, testable, and auditable

### 3.2 Code Structure


```text
app/
├── api/            # HTTP routes & schemas
├── core/           # Domain logic (documents, prompts, budgets)
├── inference/      # LLM abstraction & local inference
├── reliability/    # Timeouts, retries, canonical errors
├── data/           # Dataset utilities (arXiv)
├── ui/             # Static browser UI
├── config.py       # Centralized configuration
├── logging.py      # Structured logging & auditability
└── main.py         # Application entrypoint
```

This separation ensures:

- No business logic in HTTP handlers
- No model logic in UI or routing layers
- Reliability concerns are centralized, not scattered


## 4. Model & Inference Strategy
### 4.1 Model Choice:

The system uses a local, instruction-tuned encoder-decoder model:
```text
google/flan-t5-small
```

Why this model?:

- Runs reliably on CPU
- Predictable memory usage
- Deterministic latency
- No external API dependency
- Satisfies cost and stability constraints

### 4.2 Offline-First Design:

- No API keys required
- No environment variables required
- No external inference calls
- External cost per query: $0.00

**Internet access is required only on first run to download:**

- Model weights
- Dataset samples used in tests
- After that, the system runs fully offline.


## 5. Streaming & Latency Guarantees
### 5.1 Latency Definition (as required):

Time measured from the user submitting a query until the first words of the response are displayed

### 5.2 Implementation:

- Server-Sent Events (SSE)
- Sentence-level streaming (stable & deterministic)
- Hard wall-clock timeout enforcement
- Immediate UI rendering on first chunk

**This approach:**

- Meets p95 < 3s requirement
- Avoids fragile token-level hacks
- Works consistently across browsers


## 6. Reliability & Stability
### 6.1 Failure Handling Philosophy

The system is designed to fail closed, not fail silently.

- All errors derive from a canonical AppError
- No raw stack traces reach the user
- All failures return structured, predictable responses
- The UI never crashes on backend failures

### 6.2 Explicit Reliability Mechanisms

- Hard timeouts on inference
- Bounded retries (future-proofed)
- Input validation & size limits
- Deterministic chunking
- Stateless request handling

The system is validated to handle repeated requests without degradation.


## 7. Budget & Cost Discipline
### 7.1 Resource Budgets:

The system enforces explicit bounds on:
- Maximum document size
- Maximum chunk count
- Maximum prompt size (character-level proxy)
- Maximum output tokens
- Maximum wall-clock time

These constraints are:
- Encoded in code
- Verified via unit tests
- Enforced at runtime

### 7.2 Cost Guarantees:

- External API usage: none
- p99 external cost per query: $0.00
- Cost ceiling explicitly encoded and tested

## 8. Dataset Usage

The system uses the arXiv summarization dataset:

- Dataset: ccdv/arxiv-summarization
- Purpose:
    - Realistic long-form technical documents
    - Reference summaries for testing

- Usage:
    - Integration tests
    - Demonstration of realistic document handling

The system does not train or fine-tune models on this dataset, as the task focuses on reliable inference and system design, not model training.


## 9. Testing Strategy
### 9.1 Test Philosophy:
We test system guarantees, not model “accuracy”.
- The test suite avoids:
	- Brittle assertions on generated text
	- Token-level coupling
	- Timing flakiness

- Instead, it validates:
	- Determinism
	- Bounded behavior
	- Stability
	- Error normalization
	- Dataset compliance


### 9.2 Test Coverage:

- Unit tests:
	- Document validation
	- Chunking invariants
	- Prompt construction & budgets
	- Cost guards
	- Error taxonomy

- Integration tests:
	- /analyze API flow
	- Streaming endpoint behavior
	- Stability under repeated requests
	- Explicit dataset usage
	
All tests are executed via:
```bash
docker run <image_tag> python /home/src/tests/run_tests.py
```

## 10. Responsible AI Considerations

### 10.1 Scope Control:
- The system supports analysis; it does not make decisions.
- Outputs are summaries, not authoritative judgments.

### 10.2 Transparency:
- Model choice is explicit
- Failure modes are visible
- Limitations are documented

### 10.3 Hallucination Risk Mitigation:
- Retrieval-based prompting
- Explicit context boundaries
- No speculative reasoning chains

### 10.4 Human-in-the-Loop Ready:
- Designed to assist, not replace, expert judgment
- Outputs are explainable and auditable


## 11. Trade-Offs & Non-Goals
- Intentional Trade-Offs
	- Sentence-level streaming instead of token-level streaming
		-> favors correctness and stability

	- Local inference instead of hosted APIs
		-> favors cost, auditability, and offline operation

	- Character-level budget proxies instead of tokenizer coupling
		-> favors determinism and testability

- Explicit Non-Goals
	- Model training or fine-tuning
	- Benchmark optimization (ROUGE, BLEU, etc.)
	- Web-scale horizontal scaling
	- Autonomous decision-making
	
## 12. Running the Application
```bash
docker run -p 8080:8080 <image_tag>
```

Then open:
http://localhost:8080


## 13. Summary

- This prototype AI system is:
	- Reliable under repeated use
	- Predictable under failure
	- Auditable for compliance
	- Honest about limitations
	- Safe to deploy in high-stakes environments

The emphasis is not on what the model knows, but on how the system behaves.

