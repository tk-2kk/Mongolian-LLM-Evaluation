# Mongolian LLM Evaluation: Experiment Protocol

## 1. Research Question

Does the way Mongolian prompts are constructed, and the script used to write them, affect large language model performance across different reasoning tasks?

## 2. Research Objective

Evaluate model performance across English, machine-translated Mongolian, native-authored Mongolian in Cyrillic script, and native-authored Mongolian in Latin transliteration.

## 3. Experimental Conditions

- `english_original`: Original English question.
- `machine_translated_mn_cyrl`: English question translated into Mongolian Cyrillic using Google Translate. Preserve the output exactly.
- `native_authored_mn_cyrl`: Question independently formulated in Mongolian by a native speaker, represented in Cyrillic and reviewed for meaning and naturalness.
- `native_authored_mn_latn`: The same native-authored Mongolian wording represented in Latin transliteration.

## 4. Planned Dataset

Target: 60 underlying questions, divided into four categories.

- Factual recall: 15 questions.
- Mathematical reasoning: 15 questions.
- Logical reasoning: 15 questions.
- Commonsense reasoning: 15 questions.

Each underlying question should have a shared `item_id` across its language/script conditions. Each condition-specific record must have a unique `record_id`.

The initial GQ01–GQ10 questions are pilot/development material and are excluded from the final evaluation dataset.

## 5. Question Sources and Review

Prefer established datasets and traceable sources. Record the source, original item identifier where available, source URL, access date, license information, and any adaptations.

A native-speaker reviewer should assess the Mongolian questions without being told which versions were machine-translated or independently authored. Review meaning equivalence, naturalness, ambiguity, and possible changes in difficulty.

## 6. Model Evaluation

Use the same task instructions and scoring rules across conditions wherever applicable. Record the exact model identifier, evaluation date, settings, prompt, raw model output, and score for every run.

Use predetermined answer keys and scoring rules. Do not change the scoring rules after seeing model results without documenting the change.

## 7. Analysis Plan

Compare accuracy across the four conditions overall and within each question category. Report the number of evaluated items and any missing or invalid responses.

Distinguish the comparison between native-authored and machine-translated Mongolian from the comparison between native Mongolian Cyrillic and Latin transliteration.

## 8. Limitations

Potential limitations include imperfect equivalence between question versions, variation in Latin transliteration, limited reviewer availability, model-version changes, and possible prior exposure to public benchmark questions.

## 9. Status

This is a working protocol. Dataset sources, licensing, model choices, scoring details, and the final analysis plan must be confirmed before the main evaluation begins.
## 10. Native-Authored Question Construction Protocol

### 10.1 Source Selection

Select a question from a traceable source or established dataset. Record the original item identifier, source URL, license, and any restrictions on redistribution or adaptation.

### 10.2 Language-Neutral Specification

Before formulating the native-authored version, create a specification containing:

- The task being tested.
- All necessary facts, values, and context.
- The reasoning required.
- The gold answer and answer format.
- Relevant constraints and assumptions.
- Criteria for determining whether alternative versions test the same task.

The specification describes the problem's meaning and requirements, not its exact wording.

### 10.3 Native Formulation

Formulate the native Mongolian question from the specification rather than copying the English sentence structure. Preserve the intended task, necessary information, constraints, and expected answer while allowing natural Mongolian phrasing.

For items whose author has already seen the English source, do not claim blind or independent-from-source formulation. Record these as pilot items or document the deviation from the protocol.

### 10.4 Script Representation

Store the native-authored question in Mongolian Cyrillic and Latin transliteration. The two versions must represent the same intended wording. Record the transliteration convention and document any conversion or spelling decisions. Review the Cyrillic rendering and Latin transliteration for equivalence.

### 10.5 Equivalence Review

Before model evaluation, a reviewer should assess each version against the language-neutral specification for meaning, naturalness, ambiguity, completeness, and reasoning difficulty. Where possible, the reviewer should not be told which translation or authorship condition produced each version.

Document disagreements, corrections, and unresolved issues. Do not silently modify machine-translated records.

### 10.6 Item Approval

Freeze an item only after its source information, specification, gold answer, language/script records, and review status have been recorded. Keep a revision history for any subsequent changes.

### 10.7 Pilot Status

Pilot items are used to test the construction and evaluation workflow. They are not automatically included in the final dataset. Any deviations from the protocol must be documented before the main evaluation.