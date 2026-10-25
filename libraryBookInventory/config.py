from pathlib import Path

book_inventory = Path(__file__).resolve().parent / "storage" / "book-catalogue.json"
issuer_detail = Path(__file__).resolve().parent / "storage" / "book-issue-details.json"
returner_detail = Path(__file__).resolve().parent / "storage" / "book-return-detail.json"