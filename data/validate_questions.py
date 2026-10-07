import csv
from collections import Counter
from pathlib import Path

CSV_FILE = Path(__file__).parent / "questions.csv"

with CSV_FILE.open("r", encoding="utf-8", newline="") as file:
    rows = list(csv.DictReader(file))

print(f"Loaded {len(rows)} questions.")

# 1. Check IDs
record_ids = [row["record_id"] for row in rows]
item_ids = [row["item_id"] for row in rows]

print("\nID CHECK")
print("Duplicate record IDs:", len(record_ids) != len(set(record_ids)))
print("Duplicate item IDs:", len(item_ids) != len(set(item_ids)))

# 2. Check required fields
required_fields = [
    "record_id",
    "item_id",
    "condition",
    "question",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_option",
    "category",
    "question_type",
    "expected_difficulty",
    "fact_source_name",
    "fact_source_url",
    "created_by",
    "review_status",
    "revision_version",
]

print("\nREQUIRED FIELD CHECK")

for row_number, row in enumerate(rows, start=2):
    missing = [field for field in required_fields if not row[field].strip()]

    if missing:
        print(f"Row {row_number}: missing {missing}")

# 3. Check correct answers
valid_options = {"A", "B", "C", "D"}

print("\nANSWER CHECK")

for row_number, row in enumerate(rows, start=2):
    correct = row["correct_option"].strip()

    if correct not in valid_options:
        print(f"Row {row_number}: invalid correct option: {correct}")

# 4. Count answer positions
answer_counts = Counter(row["correct_option"].strip() for row in rows)

print("\nANSWER POSITION COUNTS")
for option in ["A", "B", "C", "D"]:
    print(f"{option}: {answer_counts[option]}")

if max(answer_counts.values()) - min(answer_counts.values()) <= 2:
      print("Answer positions are reasonably balanced.")
else:
    print("WARNING: Answer positions are unbalanced.")
