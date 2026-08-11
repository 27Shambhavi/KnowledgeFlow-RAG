# import os
# import os
# import base64

# import streamlit as st

# from app.config import UPLOAD_DIR
# from app.ingestion.document_manager import process_document
# from app.pipeline.rag_pipeline import run_rag
# import streamlit as st

# from app.config import UPLOAD_DIR
# from app.ingestion.document_manager import process_document
# from app.pipeline.rag_pipeline import run_rag


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Knowledge Workspace",
#     page_icon="◈",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# # ============================================================
# # THEME-FRIENDLY CSS
# # ============================================================

# st.markdown(
#     """
#     <style>

#     /* ========================================================
#        GLOBAL LAYOUT
#        ======================================================== */

#     .block-container {
#         max-width: 1100px;
#         padding-top: 2rem;
#         padding-bottom: 4rem;
#     }


#     /* ========================================================
#        HEADER
#        ======================================================== */

#     .app-eyebrow {
#         font-size: 0.72rem;
#         font-weight: 700;
#         letter-spacing: 0.14em;
#         text-transform: uppercase;
#         color: var(--primary-color);
#         margin-bottom: 0.4rem;
#     }

#     .app-title {
#         font-size: 2.35rem;
#         font-weight: 750;
#         line-height: 1.15;
#         margin-bottom: 0.4rem;
#     }

#     .app-subtitle {
#         font-size: 0.95rem;
#         opacity: 0.65;
#         line-height: 1.5;
#         margin-bottom: 2rem;
#     }


#     /* ========================================================
#        SECTION HEADINGS
#        ======================================================== */

#     .section-title {
#         font-size: 1.15rem;
#         font-weight: 700;
#         margin-bottom: 0.25rem;
#     }

#     .section-description {
#         font-size: 0.85rem;
#         opacity: 0.65;
#         line-height: 1.5;
#         margin-bottom: 1rem;
#     }


#     /* ========================================================
#        SOURCE BOX
#        ======================================================== */

#     .source-box {
#         padding: 0.55rem 0.7rem;
#         margin-top: 0.4rem;
#         border-radius: 0.55rem;

#         background: var(--secondary-background-color);
#         border: 1px solid var(--secondary-background-color);

#         font-size: 0.75rem;
#         line-height: 1.4;
#     }

#     .source-score {
#         color: var(--primary-color);
#         font-weight: 650;
#     }


#     /* ========================================================
#        FILE UPLOADER
#        ======================================================== */

#     [data-testid="stFileUploader"] {
#         border-radius: 0.75rem;
#     }


#     /* ========================================================
#        BUTTONS
#        ======================================================== */

#     .stButton > button {
#         border-radius: 0.6rem;
#         min-height: 2.55rem;
#         font-weight: 600;
#     }


#     /* ========================================================
#        CHAT
#        ======================================================== */

#     [data-testid="stChatMessage"] {
#         border-radius: 0.75rem;
#     }


#     /* ========================================================
#        SIDEBAR
#        ======================================================== */

#     section[data-testid="stSidebar"] .stExpander {
#         border-radius: 0.65rem;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # ============================================================
# # SESSION STATE
# # ============================================================

# if "messages" not in st.session_state:
#     st.session_state.messages = []


# if "uploader_key" not in st.session_state:
#     st.session_state.uploader_key = 0


# # ============================================================
# # CONSTANTS
# # ============================================================

# NOT_FOUND_MESSAGE = (
#     "Information not found in the uploaded documents."
# )


# # ============================================================
# # HELPER FUNCTIONS
# # ============================================================

# def get_uploaded_documents():
#     """
#     Return all supported documents currently present
#     inside the upload directory.
#     """

#     os.makedirs(
#         UPLOAD_DIR,
#         exist_ok=True,
#     )

#     supported_extensions = {
#         ".pdf",
#         ".docx",
#         ".txt",
#     }

#     documents = []

#     for filename in os.listdir(UPLOAD_DIR):

#         extension = os.path.splitext(
#             filename
#         )[1].lower()

#         if extension in supported_extensions:

#             documents.append(
#                 filename
#             )

#     return sorted(documents)


# def save_uploaded_file(uploaded_file):
#     """
#     Save uploaded file to the upload directory.

#     Existing filenames are allowed because
#     document_manager.py determines whether the
#     document is new, unchanged, or updated.
#     """

#     os.makedirs(
#         UPLOAD_DIR,
#         exist_ok=True,
#     )

#     file_path = os.path.join(
#         UPLOAD_DIR,
#         uploaded_file.name,
#     )

#     with open(
#         file_path,
#         "wb",
#     ) as file:

#         file.write(
#             uploaded_file.getbuffer()
#         )

#     return file_path


# def clear_conversation():
#     """
#     Clear only chat history.

#     Documents and vector database remain untouched.
#     """

#     st.session_state.messages = []


# def is_not_found_answer(answer):
#     """
#     Check whether the RAG system returned
#     the not-found response.
#     """

#     if not answer:
#         return False

#     normalized_answer = (
#         str(answer)
#         .strip()
#         .lower()
#         .replace("**", "")
#     )

#     normalized_target = (
#         NOT_FOUND_MESSAGE
#         .strip()
#         .lower()
#     )

#     return (
#         normalized_answer
#         == normalized_target
#     )


# def display_sources(sources):
#     """
#     Display retrieved document sources.
#     """

#     if not sources:
#         return

#     st.markdown(
#         "**Sources**"
#     )

#     for source in sources:

#         filename = os.path.basename(
#             source.get(
#                 "source",
#                 "Unknown document",
#             )
#         )

#         page = source.get(
#             "page"
#         )

#         if page is not None:

#             page_text = (
#                 f"Page {page + 1}"
#             )

#         else:

#             page_text = (
#                 "Page unavailable"
#             )

#         score = source.get(
#             "score",
#             0.0,
#         )

#         st.markdown(
#             f"""
#             <div class="source-box">
#                 📄 <b>{filename}</b>
#                 &nbsp; · &nbsp;
#                 {page_text}
#                 &nbsp; · &nbsp;
#                 <span class="source-score">
#                     relevance {score:.2f}
#                 </span>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )


# # ============================================================
# # SIDEBAR
# # ============================================================

# with st.sidebar:

#     st.title(
#         "◈ Knowledge Workspace"
#     )

#     st.caption(
#         "Dynamic Document Intelligence"
#     )

#     st.divider()

#     # --------------------------------------------------------
#     # KNOWLEDGE BASE
#     # --------------------------------------------------------

#     st.subheader(
#         "Knowledge Base"
#     )

#     documents = get_uploaded_documents()

#     document_count = len(
#         documents
#     )

#     # Dynamic document count
#     if document_count > 0:

#         st.success(
#             f"{document_count} "
#             f"document(s) indexed"
#         )

#         st.caption(
#             "Your documents are available "
#             "for semantic search."
#         )

#     else:

#         st.info(
#             "No documents indexed yet."
#         )


#     # --------------------------------------------------------
#     # VIEW DOCUMENTS
#     # --------------------------------------------------------

#     if document_count > 0:

#         with st.expander(
#             f"View documents ({document_count})"
#         ):

#             for index, filename in enumerate(
#                 documents,
#                 start=1,
#             ):

#                 st.caption(
#                     f"{index}.  {filename}"
#                 )


#     st.divider()


#     # --------------------------------------------------------
#     # STATUS
#     # --------------------------------------------------------

#     st.caption(
#         "STATUS"
#     )

#     if document_count > 0:

#         st.markdown(
#             "🟢 **Knowledge base active**"
#         )

#     else:

#         st.markdown(
#             "⚪ **Waiting for documents**"
#         )


#     st.divider()


#     # --------------------------------------------------------
#     # CONVERSATION
#     # --------------------------------------------------------

#     st.subheader(
#         "Conversation"
#     )

#     if st.button(
#         "＋ New Conversation",
#         use_container_width=True,
#     ):

#         clear_conversation()

#         st.rerun()

#     st.caption(
#         "Start a new conversation without "
#         "removing your documents."
#     )


# # ============================================================
# # MAIN HEADER
# # ============================================================

# st.markdown(
#     '<div class="app-eyebrow">'
#     'AI DOCUMENT INTELLIGENCE'
#     '</div>',
#     unsafe_allow_html=True,
# )

# st.markdown(
#     '<div class="app-title">'
#     'Ask your knowledge base.'
#     '</div>',
#     unsafe_allow_html=True,
# )

# st.markdown(
#     '<div class="app-subtitle">'
#     'Upload documents, expand your knowledge base, '
#     'and ask questions grounded in your documents.'
#     '</div>',
#     unsafe_allow_html=True,
# )


# # ============================================================
# # DOCUMENT UPLOAD
# # ============================================================

# st.markdown(
#     '<div class="section-title">'
#     '＋ Add Knowledge'
#     '</div>',
#     unsafe_allow_html=True,
# )

# st.markdown(
#     '<div class="section-description">'
#     'Upload a PDF, DOCX, or TXT document. '
#     'New documents are added to the knowledge base, '
#     'while modified documents are automatically updated.'
#     '</div>',
#     unsafe_allow_html=True,
# )


# uploaded_file = st.file_uploader(
#     "Choose a document",
#     type=[
#         "pdf",
#         "docx",
#         "txt",
#     ],
#     key=(
#         f"document_uploader_"
#         f"{st.session_state.uploader_key}"
#     ),
# )


# if uploaded_file is not None:

#     st.success(
#         f"Ready: {uploaded_file.name}"
#     )

#     if st.button(
#         "Add / Update Knowledge Base",
#         type="primary",
#         use_container_width=True,
#     ):

#         try:

#             # ------------------------------------------------
#             # SAVE FILE
#             # ------------------------------------------------

#             file_path = save_uploaded_file(
#                 uploaded_file
#             )


#             # ------------------------------------------------
#             # PROCESS DOCUMENT
#             # ------------------------------------------------

#             with st.spinner(
#                 "Processing knowledge base..."
#             ):

#                 result = process_document(
#                     file_path
#                 )


#             status = result.get(
#                 "status"
#             )

#             chunk_count = result.get(
#                 "chunks",
#                 0,
#             )

#             filename = result.get(
#                 "filename",
#                 uploaded_file.name,
#             )


#             # ------------------------------------------------
#             # RESULT
#             # ------------------------------------------------

#             if status == "added":

#                 st.success(
#                     f"'{filename}' was added "
#                     "to the knowledge base."
#                 )

#                 st.caption(
#                     f"{chunk_count} knowledge "
#                     "chunks indexed."
#                 )


#             elif status == "updated":

#                 st.success(
#                     f"'{filename}' was updated "
#                     "successfully."
#                 )

#                 st.caption(
#                     f"Old chunks were replaced "
#                     f"with {chunk_count} new "
#                     "knowledge chunks."
#                 )


#             elif status == "unchanged":

#                 st.info(
#                     f"'{filename}' has not changed."
#                 )

#                 st.caption(
#                     "No re-indexing was required."
#                 )


#             else:

#                 st.warning(
#                     "Document processing completed "
#                     "with an unknown status."
#                 )


#             # ------------------------------------------------
#             # RESET UPLOADER
#             # ------------------------------------------------

#             st.session_state.uploader_key += 1

#             st.rerun()


#         except Exception as error:

#             st.error(
#                 "Document processing failed."
#             )

#             st.exception(
#                 error
#             )


# # ============================================================
# # CHAT / Q&A SECTION
# # ============================================================

# st.divider()

# st.markdown(
#     '<div class="section-title">'
#     '◉ Ask the Knowledge Base'
#     '</div>',
#     unsafe_allow_html=True,
# )

# st.markdown(
#     '<div class="section-description">'
#     'Ask questions about your uploaded documents. '
#     'The assistant answers using relevant retrieved content.'
#     '</div>',
#     unsafe_allow_html=True,
# )


# # ============================================================
# # CHAT HISTORY
# # ============================================================

# for message in st.session_state.messages:

#     with st.chat_message(
#         message["role"]
#     ):

#         st.markdown(
#             message["content"]
#         )

#         if (
#             message["role"] == "assistant"
#             and message.get("sources")
#             and not is_not_found_answer(
#                 message["content"]
#             )
#         ):

#             display_sources(
#                 message["sources"]
#             )


# # ============================================================
# # CHAT INPUT
# # ============================================================

# question = st.chat_input(
#     "Ask something about your documents..."
# )


# if question:

#     # --------------------------------------------------------
#     # USER MESSAGE
#     # --------------------------------------------------------

#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": question,
#         }
#     )

#     with st.chat_message(
#         "user"
#     ):

#         st.markdown(
#             question
#         )


#     # --------------------------------------------------------
#     # RAG RESPONSE
#     # --------------------------------------------------------

#     with st.chat_message(
#         "assistant"
#     ):

#         with st.spinner(
#             "Searching the knowledge base..."
#         ):

#             try:

#                 result = run_rag(
#                     question
#                 )

#                 answer = result.get(
#                     "answer",
#                     NOT_FOUND_MESSAGE,
#                 )

#                 sources = result.get(
#                     "sources",
#                     [],
#                 )

#             except Exception as error:

#                 answer = (
#                     "I couldn't process "
#                     "that question."
#                 )

#                 sources = []

#                 st.error(
#                     "RAG pipeline error."
#                 )

#                 st.exception(
#                     error
#                 )


#         # ----------------------------------------------------
#         # ANSWER
#         # ----------------------------------------------------

#         st.markdown(
#             "**Answer**"
#         )

#         st.markdown(
#             answer
#         )


#         # ----------------------------------------------------
#         # SOURCES
#         # ----------------------------------------------------

#         if (
#             sources
#             and not is_not_found_answer(
#                 answer
#             )
#         ):

#             display_sources(
#                 sources
#             )


#     # --------------------------------------------------------
#     # SAVE ASSISTANT RESPONSE
#     # --------------------------------------------------------

#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": answer,
#             "sources": sources,
#         }
#     )
import os
import base64

import streamlit as st

from app.config import UPLOAD_DIR
from app.ingestion.document_manager import process_document
from app.pipeline.rag_pipeline import run_rag


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Knowledge Workspace",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# THEME-FRIENDLY CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL LAYOUT
       ======================================================== */

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .app-eyebrow {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--primary-color);
        margin-bottom: 0.4rem;
    }

    .app-title {
        font-size: 2.35rem;
        font-weight: 750;
        line-height: 1.15;
        margin-bottom: 0.4rem;
    }

    .app-subtitle {
        font-size: 0.95rem;
        opacity: 0.65;
        line-height: 1.5;
        margin-bottom: 2rem;
    }


    /* ========================================================
       SECTION HEADINGS
       ======================================================== */

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .section-description {
        font-size: 0.85rem;
        opacity: 0.65;
        line-height: 1.5;
        margin-bottom: 1rem;
    }


    /* ========================================================
       SOURCE BOX
       ======================================================== */

    .source-box {
        padding: 0.55rem 0.7rem;
        margin-top: 0.4rem;
        border-radius: 0.55rem;

        background: var(--secondary-background-color);
        border: 1px solid var(--secondary-background-color);

        font-size: 0.75rem;
        line-height: 1.4;
    }

    .source-score {
        color: var(--primary-color);
        font-weight: 650;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        border-radius: 0.75rem;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 0.6rem;
        min-height: 2.55rem;
        font-weight: 600;
    }


    /* ========================================================
       CHAT
       ======================================================== */

    [data-testid="stChatMessage"] {
        border-radius: 0.75rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] .stExpander {
        border-radius: 0.65rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "selected_document" not in st.session_state:
    st.session_state.selected_document = None


# ============================================================
# CONSTANTS
# ============================================================

NOT_FOUND_MESSAGE = (
    "Information not found in the uploaded documents."
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_uploaded_documents():
    """
    Return all supported documents currently present
    inside the upload directory.
    """

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True,
    )

    supported_extensions = {
        ".pdf",
        ".docx",
        ".txt",
    }

    documents = []

    for filename in os.listdir(UPLOAD_DIR):

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension in supported_extensions:

            documents.append(
                filename
            )

    return sorted(documents)


def display_pdf(file_path):
    """Display a PDF directly inside the Streamlit app."""

    if not os.path.exists(file_path):
        st.error("Document not found.")
        return

    with open(file_path, "rb") as file:
        pdf_bytes = file.read()

    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{base64_pdf}"
        width="100%"
        height="750"
        type="application/pdf"
        style="border: 1px solid #888; border-radius: 10px;"
    ></iframe>
    """

    st.markdown(
        pdf_display,
        unsafe_allow_html=True,
    )


def save_uploaded_file(uploaded_file):
    """
    Save uploaded file to the upload directory.

    Existing filenames are allowed because
    document_manager.py determines whether the
    document is new, unchanged, or updated.
    """

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True,
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        uploaded_file.name,
    )

    with open(
        file_path,
        "wb",
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return file_path


def clear_conversation():
    """
    Clear only chat history.

    Documents and vector database remain untouched.
    """

    st.session_state.messages = []


def is_not_found_answer(answer):
    """
    Check whether the RAG system returned
    the not-found response.
    """

    if not answer:
        return False

    normalized_answer = (
        str(answer)
        .strip()
        .lower()
        .replace("**", "")
    )

    normalized_target = (
        NOT_FOUND_MESSAGE
        .strip()
        .lower()
    )

    return (
        normalized_answer
        == normalized_target
    )


def display_sources(sources):
    """
    Display retrieved document sources.
    """

    if not sources:
        return

    st.markdown(
        "**Sources**"
    )

    for source in sources:

        filename = os.path.basename(
            source.get(
                "source",
                "Unknown document",
            )
        )

        page = source.get(
            "page"
        )

        if page is not None:

            page_text = (
                f"Page {page + 1}"
            )

        else:

            page_text = (
                "Page unavailable"
            )

        score = source.get(
            "score",
            0.0,
        )

        st.markdown(
            f"""
            <div class="source-box">
                📄 <b>{filename}</b>
                &nbsp; · &nbsp;
                {page_text}
                &nbsp; · &nbsp;
                <span class="source-score">
                    relevance {score:.2f}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "◈ Knowledge Workspace"
    )

    st.caption(
        "Dynamic Document Intelligence"
    )

    st.divider()

    # --------------------------------------------------------
    # KNOWLEDGE BASE
    # --------------------------------------------------------

    st.subheader(
        "Knowledge Base"
    )

    documents = get_uploaded_documents()

    document_count = len(
        documents
    )

    # Dynamic document count
    if document_count > 0:

        st.success(
            f"{document_count} "
            f"document(s) indexed"
        )

        st.caption(
            "Your documents are available "
            "for semantic search."
        )

    else:

        st.info(
            "No documents indexed yet."
        )


    # --------------------------------------------------------
    # VIEW DOCUMENTS
    # --------------------------------------------------------

    if document_count > 0:

        with st.expander(
            f"View documents ({document_count})"
        ):

            for index, filename in enumerate(
                documents,
                start=1,
            ):

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.caption(f"📄 {filename}")

                with col2:
                    if st.button(
                        "Open",
                        key=f"open_doc_{index}",
                    ):
                        st.session_state.selected_document = filename
                        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    st.caption(
        "STATUS"
    )

    if document_count > 0:

        st.markdown(
            "🟢 **Knowledge base active**"
        )

    else:

        st.markdown(
            "⚪ **Waiting for documents**"
        )


    st.divider()


    # --------------------------------------------------------
    # CONVERSATION
    # --------------------------------------------------------

    st.subheader(
        "Conversation"
    )

    if st.button(
        "＋ New Conversation",
        use_container_width=True,
    ):

        clear_conversation()

        st.rerun()

    st.caption(
        "Start a new conversation without "
        "removing your documents."
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="app-eyebrow">'
    'AI DOCUMENT INTELLIGENCE'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-title">'
    'Ask your knowledge base.'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    'Upload documents, expand your knowledge base, '
    'and ask questions grounded in your documents.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">'
    '＋ Add Knowledge'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Upload a PDF, DOCX, or TXT document. '
    'New documents are added to the knowledge base, '
    'while modified documents are automatically updated.'
    '</div>',
    unsafe_allow_html=True,
)


uploaded_file = st.file_uploader(
    "Choose a document",
    type=[
        "pdf",
        "docx",
        "txt",
    ],
    key=(
        f"document_uploader_"
        f"{st.session_state.uploader_key}"
    ),
)


if uploaded_file is not None:

    st.success(
        f"Ready: {uploaded_file.name}"
    )

    if st.button(
        "Add / Update Knowledge Base",
        type="primary",
        use_container_width=True,
    ):

        try:

            # ------------------------------------------------
            # SAVE FILE
            # ------------------------------------------------

            file_path = save_uploaded_file(
                uploaded_file
            )


            # ------------------------------------------------
            # PROCESS DOCUMENT
            # ------------------------------------------------

            with st.spinner(
                "Processing knowledge base..."
            ):

                result = process_document(
                    file_path
                )


            status = result.get(
                "status"
            )

            chunk_count = result.get(
                "chunks",
                0,
            )

            filename = result.get(
                "filename",
                uploaded_file.name,
            )


            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            if status == "added":

                st.success(
                    f"'{filename}' was added "
                    "to the knowledge base."
                )

                st.caption(
                    f"{chunk_count} knowledge "
                    "chunks indexed."
                )


            elif status == "updated":

                st.success(
                    f"'{filename}' was updated "
                    "successfully."
                )

                st.caption(
                    f"Old chunks were replaced "
                    f"with {chunk_count} new "
                    "knowledge chunks."
                )


            elif status == "unchanged":

                st.info(
                    f"'{filename}' has not changed."
                )

                st.caption(
                    "No re-indexing was required."
                )


            else:

                st.warning(
                    "Document processing completed "
                    "with an unknown status."
                )


            # ------------------------------------------------
            # RESET UPLOADER
            # ------------------------------------------------

            st.session_state.uploader_key += 1

            st.rerun()


        except Exception as error:

            st.error(
                "Document processing failed."
            )

            st.exception(
                error
            )


# ============================================================
# DOCUMENT PREVIEW
# ============================================================

selected_document = st.session_state.selected_document

if selected_document:

    selected_path = os.path.join(
        UPLOAD_DIR,
        selected_document,
    )

    st.divider()

    st.markdown(
        f"### 📄 {selected_document}"
    )

    if os.path.exists(selected_path):

        if selected_document.lower().endswith(".pdf"):
            display_pdf(selected_path)

        elif selected_document.lower().endswith(".txt"):

            try:
                with open(
                    selected_path,
                    "r",
                    encoding="utf-8",
                ) as file:
                    text_content = file.read()

                st.text_area(
                    "Document content",
                    text_content,
                    height=500,
                    disabled=True,
                )

            except Exception:
                st.error(
                    "Unable to preview this text document."
                )

        else:
            st.info(
                "Preview is currently available for PDF and TXT documents."
            )

    else:
        st.error(
            "The selected document could not be found."
        )

    if st.button(
        "✕ Close document",
        key="close_document",
    ):
        st.session_state.selected_document = None
        st.rerun()

    st.divider()


# ============================================================
# CHAT / Q&A SECTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '◉ Ask the Knowledge Base'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Ask questions about your uploaded documents. '
    'The assistant answers using relevant retrieved content.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and message.get("sources")
            and not is_not_found_answer(
                message["content"]
            )
        ):

            display_sources(
                message["sources"]
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask something about your documents..."
)


if question:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    # --------------------------------------------------------
    # RAG RESPONSE
    # --------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Searching the knowledge base..."
        ):

            try:

                result = run_rag(
                    question
                )

                answer = result.get(
                    "answer",
                    NOT_FOUND_MESSAGE,
                )

                sources = result.get(
                    "sources",
                    [],
                )

            except Exception as error:

                answer = (
                    "I couldn't process "
                    "that question."
                )

                sources = []

                st.error(
                    "RAG pipeline error."
                )

                st.exception(
                    error
                )


        # ----------------------------------------------------
        # ANSWER
        # ----------------------------------------------------

        st.markdown(
            "**Answer**"
        )

        st.markdown(
            answer
        )


        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        if (
            sources
            and not is_not_found_answer(
                answer
            )
        ):

            display_sources(
                sources
            )


    # --------------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )