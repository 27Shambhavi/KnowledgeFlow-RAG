import os

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
       LAYOUT
       ======================================================== */

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
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
        margin-bottom: 0.35rem;
    }

    .app-title {
        font-size: 2.25rem;
        font-weight: 750;
        line-height: 1.15;
        margin-bottom: 0.35rem;
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
       SOURCE
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
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] .stButton > button {
        border-radius: 0.6rem;
        font-weight: 600;
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
    Return supported documents currently stored
    in the upload directory.
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
            documents.append(filename)

    return sorted(documents)


def save_uploaded_file(uploaded_file):
    """
    Save the uploaded file to data/uploads/.

    Important:
    We intentionally allow an existing filename to be
    overwritten here.

    The document manager will compare the new file hash
    with the registered hash and decide whether to:

        ADD
        UNCHANGED
        UPDATE
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
    Clear only the current chat history.

    Documents and the vector database remain untouched.
    """

    st.session_state.messages = []


def is_not_found_answer(answer):
    """
    Determine whether the RAG pipeline returned
    the not-found response.

    This prevents irrelevant retrieved chunks
    from being displayed as sources.
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
# MAIN COLUMNS
# ============================================================

upload_column, chat_column = st.columns(
    [0.9, 1.6],
    gap="large",
)


# ============================================================
# UPLOAD SECTION
# ============================================================

with upload_column:

    st.markdown(
        '<div class="section-title">'
        '＋ Add Knowledge'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Upload a PDF, DOCX, or TXT document. '
        'New documents are added to the existing '
        'knowledge base. Updated documents are '
        're-indexed automatically.'
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
                # SAVE UPLOADED FILE
                # ------------------------------------------------

                file_path = save_uploaded_file(
                    uploaded_file
                )

                # ------------------------------------------------
                # PROCESS DOCUMENT
                #
                # document_manager decides:
                #
                # NEW FILE
                #       → ADD
                #
                # SAME FILE CONTENT
                #       → UNCHANGED
                #
                # SAME FILENAME + CHANGED CONTENT
                #       → UPDATE
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
                # RESULT MESSAGES
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
                # RESET FILE UPLOADER
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
# CHAT SECTION
# ============================================================

with chat_column:

    st.markdown(
        '<div class="section-title">'
        '◉ Ask the Knowledge Base'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Ask questions about your uploaded documents. '
        'The assistant answers using relevant '
        'retrieved content.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()


    # ========================================================
    # DISPLAY CHAT HISTORY
    # ========================================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            # ------------------------------------------------
            # SOURCES
            # ------------------------------------------------

            if (
                message["role"] == "assistant"
                and message.get("sources")
                and not is_not_found_answer(
                    message["content"]
                )
            ):

                st.markdown(
                    "**Sources**"
                )

                for source in message["sources"]:

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


    # ========================================================
    # QUESTION INPUT
    # ========================================================

    question = st.chat_input(
        "Ask something about your documents..."
    )

    if question:

        # ----------------------------------------------------
        # STORE USER MESSAGE
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # RAG RESPONSE
        # ----------------------------------------------------

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


            # ------------------------------------------------
            # ANSWER
            # ------------------------------------------------

            st.markdown(
                "**Answer**"
            )

            st.markdown(
                answer
            )


            # ------------------------------------------------
            # SOURCES
            # ------------------------------------------------

            if (
                sources
                and not is_not_found_answer(
                    answer
                )
            ):

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


        # ----------------------------------------------------
        # STORE ASSISTANT RESPONSE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources,
            }
        )