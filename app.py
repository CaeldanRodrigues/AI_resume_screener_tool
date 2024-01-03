import streamlit as st

def main():
    st.set_page_config(page_title="AI Resume Screener")
    st.title("AI Resume Screener")
    
    job_description = st.text_area("Job Description of the role", key="job_description")
    document_count = st.text_input("Number of Resumes to return", key="document_count")

    pdf = st.file_uploader("Upload resume(s)", type=["pdf"],accept_multiple_files=True)

    submit_button = st.button("Analyse")

    if submit_button:
        with st.spinner("Analysing Resumes..."):
            st.success("Completed")
            st.balloons()