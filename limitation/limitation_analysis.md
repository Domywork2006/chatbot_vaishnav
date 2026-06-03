# Phase 2 RAG System - Limitations Analysis

## Project

AI Chatbot & RAG Document Assistant

---

# 1. Duplicate Chunk Retrieval

## Observation

During testing, the semantic retriever occasionally returns multiple chunks containing very similar information.

## Root Cause

The current implementation uses similarity search, which retrieves the highest-scoring chunks independently without considering diversity.

## Business Impact

* Repeated information in context
* Reduced context diversity
* Potential loss of important information from other sections

## Proposed Solution

* Implement Maximum Marginal Relevance (MMR)
* Add chunk deduplication
* Improve chunking strategy

---

# 2. No Relevance Threshold

## Observation

The system always retrieves Top-K chunks even when the question is unrelated to the uploaded documents.

## Example

Document:
Deep Learning Notes

Question:
Who won the FIFA World Cup 2022?

The system may still retrieve unrelated chunks.

## Business Impact

* Misleading responses
* Reduced user trust

## Proposed Solution

Introduce a similarity score threshold before retrieval results are used.

---

# 3. Hallucination Risk

## Observation

Although retrieval provides context, the LLM may occasionally generate information beyond the retrieved content.

## Business Impact

* Reduced answer reliability
* Potential misinformation

## Proposed Solution

* Stronger prompt constraints
* Confidence scoring
* Response validation mechanisms

---

# 4. Slow Re-Indexing

## Observation

When new PDFs are uploaded, embeddings must be generated again.

## Root Cause

Current implementation rebuilds indexing for newly uploaded content.

## Business Impact

* Increased response latency
* Reduced scalability

## Proposed Solution

* Incremental indexing
* Better caching mechanisms
* Background document processing

---

# 5. Limited File Format Support

## Observation

The current system supports PDF documents only.

## Business Impact

Organizations often use:

* DOCX
* TXT
* PPTX
* Excel files

## Proposed Solution

Extend support for additional document formats.

---

# 6. Multi-PDF Retrieval Challenges

## Observation

When multiple PDFs are uploaded, retrieval may not always select the most relevant document source.

## Business Impact

* Reduced answer quality
* Retrieval from unintended documents

## Proposed Solution

* Metadata filtering
* Document-aware retrieval
* Source prioritization

---

# 7. Context Loss Across Chunks

## Observation

Important information may be split between chunks.

## Example

Part of a concept may appear in one chunk while its explanation appears in another.

## Business Impact

* Incomplete answers
* Missing context

## Proposed Solution

* Optimize chunk size
* Experiment with chunk overlap
* Context-aware chunking

---

# 8. Lack of Retrieval Confidence

## Observation

Users cannot determine how confident the system is about retrieved results.

## Business Impact

* Reduced transparency
* Lower trust in responses

## Proposed Solution

Display:

* Similarity scores
* Confidence indicators
* Retrieval quality metrics

---

# Future Direction

Based on the observations above, the following improvements are recommended:

1. Hybrid Retrieval (Semantic + Keyword Search)
2. Maximum Marginal Relevance (MMR)
3. Better Caching
4. Incremental Indexing
5. Cloud Deployment
6. Additional Document Format Support
7. Confidence Scoring
8. Advanced Reranking

---

# Conclusion

The current RAG system successfully demonstrates document-aware question answering using semantic retrieval and vector search. The identified limitations primarily relate to retrieval quality, scalability, and user experience. Addressing these limitations would improve the system's accuracy, efficiency, and suitability for real-world business environments.
