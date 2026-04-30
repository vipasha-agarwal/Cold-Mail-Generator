# Cold Email Generator

This project is a Streamlit app that reads a job post from a URL, extracts the job details with Groq + LangChain, and generates a tailored cold email using your portfolio links.

## Local Setup

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
streamlit run main.py
```

Add your Groq key to `.streamlit/secrets.toml` or a local `.env` file:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

## Free Deployment

This app is prepared for **Streamlit Community Cloud**.

1. Push this folder to GitHub.
2. Open `https://share.streamlit.io/`.
3. Click **Create app**.
4. Select this repository and set the entrypoint file to `main.py`.
5. In **Advanced settings**, choose Python `3.12`.
6. Paste the contents of your secret file and deploy.

Detailed steps are in `DEPLOYMENT.md`.

## Project Files

- `main.py` contains the Streamlit UI.
- `chain.py` handles job extraction and email generation.
- `portfolio.py` loads portfolio data into ChromaDB.
- `Portfolio.csv` stores the skill/link pairs used in email generation.
