import re

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^*?]>', '', text)
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z0-9]', '', text)
    # Remove URLs
    text = re.sub(r'http\[S]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove multiple space with single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim Leading and trailing whitespaces
    text = text.strip()
    #Remove extra whitespace
    text = ' '.join(text.split())
    return text