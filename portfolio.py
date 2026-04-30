import csv
import re
from pathlib import Path


def _tokenize(text):
    return {
        token
        for token in re.findall(r"[a-z0-9+#.]+", str(text).lower())
        if len(token) > 1
    }


class Portfolio:
    def __init__(self, file_path=None):
        base_dir = Path(__file__).resolve().parent
        self.file_path = Path(file_path) if file_path else base_dir / "Portfolio.csv"
        self.records = []

    def load_portfolio(self):
        if self.records:
            return

        with self.file_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                skill_text = row.get("Programming", "")
                self.records.append(
                    {
                        "skill_text": skill_text,
                        "skill_tokens": _tokenize(skill_text),
                        "link": row.get("Links", ""),
                    }
                )

    def query_links(self, skills, limit=2):
        query_tokens = set()
        for skill in skills:
            query_tokens.update(_tokenize(skill))

        scored_records = []
        for record in self.records:
            overlap = len(query_tokens & record["skill_tokens"])
            if overlap:
                scored_records.append((overlap, record["link"]))

        scored_records.sort(key=lambda item: item[0], reverse=True)

        unique_links = []
        for _, link in scored_records:
            if link and link not in unique_links:
                unique_links.append(link)
            if len(unique_links) == limit:
                break

        if unique_links:
            return unique_links

        return [record["link"] for record in self.records[:limit] if record["link"]]
