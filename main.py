import streamlit as st

from chain import Chain
from portfolio import Portfolio
from utils import fetch_page_text


def create_streamlit_app():
    st.set_page_config(layout="wide", page_title="Cold Email Generator")
    st.title("Cold Mail Generator")
    st.caption("Paste a public job URL and generate a tailored outreach email.")

    url_input = st.text_input(
        "Enter a job URL",
        value="https://jobs.nike.com/job/R-43526?from=job%20search%20funnel",
    )

    if st.button("Generate Email", type="primary"):
        if not url_input.strip():
            st.error("Please enter a job URL.")
            return

        try:
            with st.spinner("Reading the job page..."):
                page_text = fetch_page_text(url_input.strip())

            with st.spinner("Loading portfolio and generating email..."):
                chain = Chain()
                portfolio = Portfolio()
                portfolio.load_portfolio()
                jobs = chain.extract_jobs(page_text)

            if not jobs:
                st.error("No job details could be extracted from that page.")
                return

            for index, job in enumerate(jobs, start=1):
                links = portfolio.query_links(job.get("skills", []))
                email = chain.write_mail(job, links)

                st.subheader(f"Generated Email {index}")
                st.code(email, language="markdown")

                with st.expander("Extracted Job Data"):
                    st.json(job)

                if links:
                    st.write("Suggested portfolio links:")
                    for link in links:
                        st.write(f"- {link}")

        except Exception as exc:
            st.error(f"An error occurred: {exc}")


if __name__ == "__main__":
    create_streamlit_app()
