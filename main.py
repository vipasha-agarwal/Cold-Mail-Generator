# llama3-8b-8192

from chain import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain.document_loaders import WebBaseLoader
import streamlit as st

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-43526?from=job%20search%20funnel")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language = 'markdown')

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
        chain = Chain()
        portfolio = Portfolio()
        st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="")
        create_streamlit_app(chain, portfolio, clean_text)