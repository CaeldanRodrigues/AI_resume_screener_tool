import streamlit as st
import uuid

from utils import *

if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] = ''

def main():
    # st.set_page_config(page_title="AI Resume Screener")
    st.title("AI Resume Screener")
    
    job_description = st.text_area("Job Description of the role", key="job_description")
    resume_count = st.text_input("Number of Resumes to return", key="resume_count")

    pdf = st.file_uploader("Upload resume(s)", type=["pdf"], accept_multiple_files=True)

    submit_button = st.button("Analyse")

    if submit_button:
        with st.spinner("Analysing Resumes..."):

            st.session_state['unique_id'] = uuid.uuid4().hex
            # st.write(st.session_state['unique_id'])

            docs = create_docs(pdf, st.session_state['unique_id'])
            # st.write(docs)
            embeddings = create_embeddings()
            push_to_pinecone("gcp-starter", "test-index", embeddings, docs)

            relevant_docs = similar_docs(job_description, resume_count, "gcp-starter", "test-index", embeddings, st.session_state['unique_id'])

            st.write(relevant_docs)

            st.success("Completed")


if __name__ == "__main__":
    main()