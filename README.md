# Knowledge Workspace-RAG

### Dynamic Document Intelligence powered by Retrieval-Augmented Generation

Knowledge Workspace-RAG is an end-to-end document-based RAG application that allows users to upload documents, build a persistent knowledge base, and ask questions using natural language.

The system retrieves relevant information from uploaded documents and uses an LLM to generate grounded answers. It also supports dynamic knowledge-base updates: new documents are added, unchanged documents are skipped, and modified documents are re-indexed automatically.

---

## Features

- 📄 Upload PDF, DOCX, and TXT documents
- 🔄 Dynamically add new documents to the knowledge base
- ♻️ Automatically detect modified documents
- 🚫 Avoid duplicate indexing of unchanged documents
- ✂️ Recursive Character Text Splitting
- 🧠 Gemini-based document embeddings
- 🗄️ Persistent Chroma vector database
- 🔎 Semantic similarity search
- 🎯 Relevance filtering
- 🤖 LLM-based answer generation
- 📚 Source-aware responses
- ❌ "Information not found" handling for unrelated questions
- 💬 Chat-style question-answer interface
- 🌓 Light/Dark theme compatible UI
- 📊 Dynamic document count
- 📂 Expandable document list
- 👁️ In-app PDF document preview
- 🧪 RAG quality and out-of-scope evaluation tests

---

# Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  │                                   │
                  ▼                                   ▼
          UPLOAD DOCUMENT                         ASK QUESTION
                  │                                   │
                  ▼                                   ▼
        Document Manager                      Query Embedding
                  │                                   │
              SHA-256                                │
                Hash                                  │
                  │                                   ▼
        ┌─────────┼─────────┐                 Chroma Search
        │         │         │                       │
       NEW      SAME     CHANGED                    ▼
        │         │         │                  Top-K Chunks
        │         │         │                       │
        │         │      Delete Old                ▼
        │         │      Chunks              Relevance Filter
        │         │         │                       │
        ▼         ▼         ▼                 ┌─────┴─────┐
      Load      Skip      Re-index            │           │
        │                   │              Relevant    Not Relevant
        ▼                   ▼                 │           │
      Chunk                Chunk              ▼           ▼
        │                   │                LLM       NOT FOUND
        ▼                   ▼                 │
     Embedding           Embedding            ▼
        │                   │               ANSWER
        └──────────┬────────┘
                   ▼
RAG Pipeline

KnowledgeFlow-RAG follows a standard Retrieval-Augmented Generation architecture.

Document
   ↓
Document Loading
   ↓
Text Chunking
   ↓
Metadata Enrichment
   ↓
Embedding Generation
   ↓
Chroma Vector Database
   ↓
Semantic Retrieval
   ↓
Relevance Filtering
   ↓
Relevant Context
   ↓
LLM
   ↓
Grounded Answer

1. Document Ingestion

When a user uploads a document, the application first saves it into the upload directory.

Supported formats:

PDF
DOCX
TXT

The document manager then determines whether the document is:

NEW
UNCHANGED
UPDATED

This decision is made using a SHA-256 content hash.

2. Document Hashing

Every uploaded document receives a SHA-256 hash based on its content.

Example:

document.pdf
     ↓
SHA-256
     ↓
ABC123...

The hash is stored in the document registry.

When the same document is uploaded again:

Old Hash == New Hash
        ↓
    UNCHANGED
        ↓
       SKIP

If the content has changed:

Old Hash != New Hash
        ↓
      UPDATED
        ↓
Delete old chunks
        ↓
Index new chunks

This prevents duplicate vectors and stale document information.

3. Document Registry

The application maintains a document registry to track indexed documents.

The registry stores information such as:

filename
document hash
chunk count
created time
updated time

The registry is stored locally under:

data/registry/
4. Document Loading

The document loader extracts readable text from the uploaded document.

The extracted content is converted into LangChain document objects.

Conceptually:

PDF
 ↓
Text Extraction
 ↓
Document Objects

Metadata such as source and page information can be preserved for source tracking.

5. Chunking

The project uses:

RecursiveCharacterTextSplitter

The splitter recursively attempts to split the document using boundaries such as:

\n\n
\n
. 
space
character

The configured parameters are:

CHUNK_SIZE
CHUNK_OVERLAP

The chunk size is character-based rather than word-based.

The overlap helps preserve contextual continuity between neighboring chunks.

Example:

Document
   ↓
┌───────────────┐
│    Chunk 1    │
└───────────────┘
        │
        │ overlap
        ▼
    ┌───────────────┐
    │    Chunk 2    │
    └───────────────┘
6. Metadata

Each chunk can carry metadata associated with the original document.

Typical metadata includes:

source
page
document_id
chunk information

This allows the system to associate retrieved information with its original document.

7. Embeddings

Each document chunk is converted into a numerical vector using Google's Gemini embedding model:

gemini-embedding-001

Conceptually:

Text Chunk
    ↓
Embedding Model
    ↓
Vector

The embedding model represents the semantic meaning of the text in vector space.

The default output dimensionality of gemini-embedding-001 is:

3072 dimensions

These vectors are stored in Chroma.

8. Vector Database

The project uses:

Chroma

as the vector database.

Each stored record contains conceptually:

Vector
+
Document Chunk
+
Metadata

The vector store is persistent, so the knowledge base remains available across application restarts.

9. Query Processing

When a user asks a question:

"What is the closing balance?"

the query is also converted into an embedding using the same embedding model.

User Question
      ↓
Gemini Embedding
      ↓
Query Vector

This allows the query and document chunks to exist in the same vector space.

10. Semantic Retrieval

The query vector is compared against stored document vectors.

The most semantically similar chunks are retrieved.

Example:

Query
 ↓
Chroma
 ↓
Top-K Results

This is semantic search rather than simple keyword matching.

For example:

"How much money was left at the end?"

can potentially retrieve a chunk containing:

"Closing Balance: $4,250"

even though the exact phrase "closing balance" may not appear in the query.

11. Relevance Filtering

Retrieved chunks are further evaluated using a relevance threshold.

The purpose is to prevent weakly related chunks from being passed to the LLM.

Conceptually:

Retrieved Chunks
      ↓
Relevance Check
      ↓
 ┌────┴────┐
 │         │
Relevant  Irrelevant
 │
 ▼
LLM Context

This is especially important for unrelated questions.

12. Not-Found Handling

If no sufficiently relevant information is found in the uploaded documents, the system returns:

Information not found in the uploaded documents.

For example:

User:
What is the capital of France?

        ↓

No sufficiently relevant document context

        ↓

Information not found in the uploaded documents.

This prevents the system from answering unrelated questions using unsupported information.

13. LLM Generation

The project uses:

Gemini 2.5 Flash

for answer generation.

The LLM receives:

User Question
+
Relevant Retrieved Context

Conceptually:

Question
   +
Relevant Chunks
   ↓
Gemini 2.5 Flash
   ↓
Natural Language Answer

The LLM is therefore the generation component of the RAG architecture.

The documents themselves are not used to retrain or fine-tune the LLM.

14. Dynamic Knowledge Base

One of the main features of KnowledgeFlow-RAG is dynamic document management.

New document
New PDF
   ↓
Hash
   ↓
Not found in registry
   ↓
Load
   ↓
Chunk
   ↓
Embed
   ↓
Store in Chroma

The document count increases.

Same document
Same PDF
   ↓
Same Hash
   ↓
UNCHANGED
   ↓
Skip indexing

No duplicate chunks are created.

Updated document
Modified PDF
      ↓
New Hash
      ↓
Existing document detected
      ↓
Delete old chunks
      ↓
Load modified document
      ↓
Chunk
      ↓
Embed
      ↓
Store new chunks

The document count does not increase because it is an update to an existing document.

UI

The application uses:

Streamlit

The UI provides:

Document upload
Knowledge-base status
Dynamic document count
Expandable document list
Clickable document opening
PDF preview
Chat-style question answering
Source display
New conversation option
Light/Dark theme compatibility

Example:

┌─────────────────────────────────────────────┐
│          Knowledge Workspace                │
│                                             │
│  Ask your knowledge base.                   │
│                                             │
│  ＋ Add Knowledge                            │
│  [ Choose a document ]                      │
│  [ Add / Update Knowledge Base ]            │
│                                             │
│  ─────────────────────────────────────────  │
│                                             │
│  ◉ Ask the Knowledge Base                   │
│                                             │
│  User: What is the closing balance?         │
│                                             │
│  Assistant:                                 │
│  The closing balance is $4,250.             │
│                                             │
│  Sources                                    │
│  📄 document.pdf · Page 1                   │
│                                             │
└─────────────────────────────────────────────┘

The sidebar displays the current number of uploaded documents:

Knowledge Base

🟢 7 documents indexed

▾ View documents (7)
    📄 document1.pdf
    📄 document2.pdf
    📄 document3.pdf

Clicking Open allows the user to preview the document inside the application.

Project Structure
KnowledgeFlow-RAG/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── document_loader.py
│   │   ├── document_manager.py
│   │   ├── document_registry.py
│   │   ├── chunker.py
│   │   └── indexer.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── retriever.py
│   │   └── relevance.py
│   │
│   ├── generation/
│   │   └── llm.py
│   │
│   └── pipeline/
│       └── rag_pipeline.py
│
├── data/
│   ├── uploads/
│   └── registry/
│       └── documents.json
│
├── vectorstore/
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   ├── test_registry.py
│   └── test_rag_quality.py
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
Technology Stack
Component	Technology
Programming Language	Python
UI	Streamlit
RAG Framework	LangChain
Embeddings	Google Gemini Embedding
Generative Model	Gemini 2.5 Flash
Vector Database	Chroma
Document Processing	LangChain Document Loaders
Text Splitting	RecursiveCharacterTextSplitter
Testing	Python test modules
Environment Management	Python Virtual Environment
Installation
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>

Move into the project:

cd KnowledgeFlow-RAG
2. Create a virtual environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\activate

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure Gemini API Key

Create a .env file in the project root:

GOOGLE_API_KEY=your_gemini_api_key_here

Do not commit .env to GitHub.

The API key should remain private.

5. Run the application

From the project root:

streamlit run app/main.py

The application will open in the browser.

Usage
Step 1 — Upload a document

Choose a:

PDF
DOCX
TXT

document from the UI.

Click:

Add / Update Knowledge Base
Step 2 — Ask a question

Example:

What is the closing balance?

The system:

Question
 ↓
Embedding
 ↓
Vector Search
 ↓
Relevant Chunks
 ↓
Relevance Filtering
 ↓
LLM
 ↓
Answer
Step 3 — Add another document

Upload another document.

The new document will be added to the existing knowledge base.

The existing documents remain searchable.

Step 4 — Update an existing document

Modify an existing document and upload it again.

The system detects the changed content using SHA-256 hashing.

The old indexed chunks are removed and the new version is indexed.

Step 5 — Ask an unrelated question

Example:

What is the capital of France?

If the uploaded documents do not contain relevant information, the application returns:

Information not found in the uploaded documents.
Testing

The project contains separate tests for different parts of the system.

Ingestion test
python -m tests.test_ingestion

Tests:

Document loading
Chunk creation
Basic ingestion flow
Retrieval test
python -m tests.test_retrieval

Tests:

Query retrieval
Retrieved chunks
Relevant chunks
Registry test
python -m tests.test_registry

Tests:

New document detection
Unchanged document detection
Updated document detection
RAG Quality Test
python -m tests.test_rag_quality

Tests:

Expected document questions
Expected answers
Out-of-scope questions
Not-found behavior

Example:

RAG QUALITY EVALUATION

Test 1
Question : What is the closing balance?
Expected : $4,250.00
Actual   : The closing balance is $4,250.00.
STATUS   : PASS
Complete Testing Flow

A complete manual test can be performed using this sequence:

1. Upload Document A
          ↓
2. Ask a question about Document A
          ↓
3. Verify the answer
          ↓
4. Upload Document B
          ↓
5. Ask a question about Document B
          ↓
6. Verify both documents are searchable
          ↓
7. Ask an unrelated question
          ↓
8. Verify "Information not found"
          ↓
9. Modify Document A
          ↓
10. Upload Document A again
          ↓
11. Verify it is updated rather than duplicated
          ↓
12. Ask the same question again
          ↓
13. Verify the updated information
Why RAG?

Traditional LLM applications depend primarily on the knowledge contained in the model.

A RAG system separates knowledge from generation.

Knowledge
   ↓
Vector Database

Reasoning / Language
   ↓
LLM

This allows documents to be updated without retraining the LLM.

When new information is added:

New Document
     ↓
Embedding
     ↓
Vector Database

There is no need to retrain the generative model.

RAG vs LLM

KnowledgeFlow-RAG is not simply an LLM chatbot.

The LLM is one component of the complete architecture.

RAG System
│
├── Document ingestion
├── Chunking
├── Embeddings
├── Vector storage
├── Retrieval
├── Relevance filtering
└── LLM generation

In this project:

Gemini Embedding
        ↓
Vector Representation

Chroma
        ↓
Retrieval

Gemini 2.5 Flash
        ↓
Answer Generation

Therefore:

RAG is the overall retrieval-augmented architecture, while the LLM is used for the final generation stage.

Key Design Decisions
Recursive chunking

Recursive Character Text Splitting was selected to preserve meaningful text boundaries instead of blindly splitting every fixed number of words.

Persistent vector store

Chroma is configured as a persistent vector database so that indexed documents remain available between application sessions.

Hash-based document management

SHA-256 hashing provides a simple mechanism for determining whether a document is:

New
Unchanged
Updated

This prevents unnecessary re-indexing.

Relevance filtering

Retrieval results are filtered before being passed to the LLM.

This helps reduce irrelevant context and improves the system's ability to reject unsupported questions.

Security

Never commit sensitive credentials to GitHub.

The following should remain local:

.env
.venv/
data/uploads/
vectorstore/
data/registry/

The .gitignore file is configured to prevent these files from being committed.

Limitations

Current implementation is designed as a local document intelligence application.

Potential production-level improvements include:

Authentication and authorization
Multi-user knowledge bases
Cloud vector database
Document deletion UI
Better document preview support
Advanced metadata filtering
Reranking models
Hybrid keyword + semantic search
Streaming LLM responses
Observability and tracing
Evaluation dashboards
Cloud deployment
Rate-limit handling and retries
Future Improvements

Possible future enhancements:

Hybrid Search
      ↓
Semantic + Keyword Retrieval

Reranking
      ↓
More precise context selection

Multi-user Knowledge Bases
      ↓
User-specific document collections

Document Versioning
      ↓
Track historical document versions

Advanced Evaluation
      ↓
Faithfulness
Context Relevance
Answer Relevance
Retrieval Recall
Project Objective

The primary objective of KnowledgeFlow-RAG is to demonstrate how an end-to-end Retrieval-Augmented Generation system can dynamically ingest documents, maintain an updatable knowledge base, retrieve relevant information, and generate grounded answers through an interactive user interface.

Summary

KnowledgeFlow-RAG combines:

Document Processing
        +
Recursive Chunking
        +
Embeddings
        +
Chroma Vector Database
        +
Semantic Retrieval
        +
Relevance Filtering
        +
LLM Generation
        +
Dynamic Document Management
        +
Streamlit UI

The result is a dynamic document intelligence application where users can continuously expand and update their knowledge base without retraining the underlying LLM.

             Chroma Vector DB
                   │
                   └───────────────► Retrieval
