import csv
from collections import Counter, defaultdict
from pathlib import Path

# This script lives inside data/, so don't append another /data.
DATA_DIR = Path(__file__).parent
SPEC_FILE = DATA_DIR / "item_specifications.csv"
QUESTIONS_FILE = DATA_DIR / "experiment_questions.csv"

CONDITIONS = {
    "english_original",
    "machine_translated_mn_cyrl",
    "native_authored_mn_cyrl",
    "native_authored_mn_latn",
}

TASK_TYPES = {
    "factual_recall",
    "mathematical_reasoning",
    "logical_reasoning",
    "commonsense_reasoning",
}

SPEC_FIELDS = {
    "item_id", "task_type", "problem_specification",
    "answer_format", "gold_answer", "source_name",
    "source_url", "source_item_id", "source_access_date",
    "source_license", "source_attribution", "adaptation_notes",
    "created_by", "revision_version",
}

QUESTION_FIELDS = {
    "record_id", "item_id", "condition", "question",
    "assessed_difficulty", "difficulty_assessed_by",
    "difficulty_assessed_date", "difficulty_rubric_version",
    "difficulty_assessment_status", "translation_tool",
    "translation_mode", "translation_date", "translation_notes",
    "transliteration_convention", "created_by", "reviewed_by",
    "review_status", "revision_version",
}

errors = []
warnings = []


def load_csv(path, required_fields):
    if not path.exists():
        errors.append(f"File not found: {path}")
        return None

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            errors.append(f"{path.name}: missing CSV header")
            return None

        missing = required_fields - set(reader.fieldnames)
        if missing:
            errors.append(
                f"{path.name}: missing columns {sorted(missing)}"
            )
            return None

        rows = []
        for line, row in enumerate(reader, start=2):
            if None in row:
                errors.append(
                    f"{path.name}, row {line}: too many CSV fields"
                )
                continue
            rows.append((line, row))

        return rows


def get(row, field):
    return (row.get(field) or "").strip()


def check_unique(rows, field, filename):
    seen = set()

    for line, row in rows:
        value = get(row, field)

        if not value:
            errors.append(f"{filename}, row {line}: missing {field}")
        elif value in seen:
            errors.append(
                f"{filename}, row {line}: duplicate {field} {value!r}"
            )

        seen.add(value)


print("Checking research dataset...")

spec_rows = load_csv(SPEC_FILE, SPEC_FIELDS)
question_rows = load_csv(QUESTIONS_FILE, QUESTION_FIELDS)

if spec_rows is not None and question_rows is not None:

    # 1. Check identifiers.
    check_unique(spec_rows, "item_id", SPEC_FILE.name)
    check_unique(question_rows, "record_id", QUESTIONS_FILE.name)

    spec_by_id = {
        get(row, "item_id"): row
        for _, row in spec_rows
        if get(row, "item_id")
    }

    # 2. Check each underlying problem.
    for line, row in spec_rows:
        item_id = get(row, "item_id")

        for field in (
            "task_type", "problem_specification", "answer_format",
            "gold_answer", "source_name", "source_url",
            "source_access_date", "created_by", "revision_version",
        ):
            if not get(row, field):
                errors.append(
                    f"{SPEC_FILE.name}, row {line}: missing {field}"
                )

        if get(row, "task_type") not in TASK_TYPES:
            errors.append(f"{item_id}: invalid task_type")

        if get(row, "source_license").lower() in {"", "unknown"}:
            warnings.append(
                f"{item_id}: source license still needs verification"
            )

    # 3. Check prompts and their links to specifications.
    records_by_item = defaultdict(list)

    for line, row in question_rows:
        record_id = get(row, "record_id")
        item_id = get(row, "item_id")
        condition = get(row, "condition")

        for field in (
            "item_id", "condition", "question",
            "created_by", "review_status", "revision_version",
        ):
            if not get(row, field):
                errors.append(
                    f"{QUESTIONS_FILE.name}, row {line}: missing {field}"
                )

        if item_id and item_id not in spec_by_id:
            errors.append(
                f"{record_id}: no matching item specification"
            )

        if condition not in CONDITIONS:
            errors.append(
                f"{record_id}: invalid condition {condition!r}"
            )

        if get(row, "review_status") not in {
            "not_reviewed", "approved", "revision_needed",
        }:
            errors.append(f"{record_id}: invalid review_status")

        # Difficulty is optional during the pilot.
        difficulty = get(row, "assessed_difficulty")
        if difficulty and difficulty not in {"easy", "medium", "hard"}:
            errors.append(f"{record_id}: invalid assessed_difficulty")

        # Only machine-translated prompts need translation metadata.
        if condition == "machine_translated_mn_cyrl":
            if not get(row, "translation_tool"):
                errors.append(f"{record_id}: missing translation_tool")

            mode = get(row, "translation_mode").lower()
            if mode not in {"classic", "advanced", "unknown"}:
                errors.append(
                    f"{record_id}: translation_mode must be "
                    "classic, advanced, or unknown"
                )
            elif mode == "unknown":
                warnings.append(
                    f"{record_id}: translation mode is unknown; "
                    "verify or regenerate before final evaluation"
                )
            elif mode == "advanced":
                warnings.append(
                    f"{record_id}: Advanced translation is excluded "
                    "from the main experiment"
                )

        elif any(get(row, field) for field in (
            "translation_tool", "translation_mode", "translation_date",
        )):
            errors.append(
                f"{record_id}: translation metadata should be blank "
                "for non-machine-translated prompts"
            )

        # Record the convention used for native Latin transliteration.
        if (
            condition == "native_authored_mn_latn"
            and not get(row, "transliteration_convention")
        ):
            errors.append(
                f"{record_id}: missing transliteration_convention"
            )

        try:
            if int(get(row, "revision_version")) < 1:
                raise ValueError
        except ValueError:
            errors.append(
                f"{record_id}: revision_version must be a positive integer"
            )

        if item_id:
            records_by_item[item_id].append(row)

    # 4. Check that each item has four distinct conditions.
    for item_id, records in records_by_item.items():
        found = [get(row, "condition") for row in records]
        counts = Counter(found)

        missing = CONDITIONS - set(found)
        repeated = [
            condition for condition, count in counts.items()
            if count > 1
        ]

        if missing:
            warnings.append(
                f"{item_id}: still missing {sorted(missing)}"
            )

        if repeated:
            errors.append(
                f"{item_id}: duplicate conditions {sorted(repeated)}"
            )

    print(f"\nSpecifications: {len(spec_rows)}")
    print(f"Prompt records: {len(question_rows)}")

print("\nVALIDATION RESULTS")
print(f"Errors: {len(errors)}")
print(f"Warnings: {len(warnings)}")

for message in errors:
    print("ERROR:", message)

for message in warnings:
    print("WARNING:", message)

if errors:
    print("\nValidation failed. Fix the errors above.")
else:
    print("\nNo blocking errors found. Review warnings before proceeding.")
