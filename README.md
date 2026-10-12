# Could Jack Have Been Saved?

**Group 1 · One Page, One Finding · Presentation: 19 October 2026**

A pandas-based investigation of what the Titanic's real passenger records can—and cannot—tell us about a fictional young man in third class. **No predictive models.**

## One finding

Only **10 of 86 (11.6%)** third-class men aged 18–25 survived in the Kaggle Titanic training sample. Among men aged 18–30, **9/22 (40.9%)** first-class, **1/41 (2.4%)** second-class, and **19/130 (14.6%)** third-class passengers survived. First class was associated with higher survival than third class for these young men, **but second class actually had a lower observed rate than third class**. This undermines the simple idea of a smooth class-based survival ladder, not the data's inability to establish causal effects.

## Deliverables

- [**Jupyter notebook**](notebooks/titanic_jack_analysis.ipynb): seven required sections in the assignment's exact order; original preregistered hypotheses, justified cleaning, exploration, hypothesis tests, three demonstrated data problems, and a qualified conclusion.
- [**One-page PDF poster**](poster/titanic_jack_poster.pdf): exactly three code-generated charts, a one-sentence finding, one explanation under each chart, and one limitation.
- [**Poster preview**](poster/preview.png): easy to view without opening the PDF.
- [**Presentation notes**](docs/PRESENTATION_NOTES.md): suggested speaking script and answers to expected questions.
- [**Decision log**](docs/ANALYSIS_DECISIONS.md): what we chose to put on the poster, what we cut, and why.

## Dataset and reproducibility

The **unchanged** `data/train.csv` is the Kaggle Titanic competition training file: 891 passengers, 12 columns. Source: https://www.kaggle.com/c/titanic/data. We do not use the competition `gender_submission.csv`, which contains example predictions rather than observed survival outcomes. See [data provenance](data/DATA_SOURCE.md).

From the repository root with Python 3.10+:

```bash
python -m pip install -r requirements.txt
python src/build.py
python -m pytest -q tests
```

`src/build.py` regenerates the notebook, executes every cell from a clean kernel, and rebuilds the PDF and PNG. To work interactively, open `notebooks/titanic_jack_analysis.ipynb` with Jupyter Notebook or VS Code.

## Research integrity

- The three original hypotheses were written and committed first, *before group survival analysis*, in commit [`7a423658`](https://github.com/elonaelon000/could-jack-have-survived/commit/7a423658689667bbf34772da22bb66c945d7ee90).
- H1 **SURVIVED** (adult female rates higher in every class), H2 **SURVIVED** (first-class > third-class among young men), H3 **NOT SUPPORTED** (recorded relatives > none recorded among third-class men aged 18–50).
- Those decisions are about **observed directions in this sample**, not significant causal effects. The third hypothesis was **not rewritten** after the results.
- Age missingness, cabin missingness, and small subgroups constrain our conclusions. Jack is fictional and no one has demonstrated that changing his class would have saved him.

**Group members:** [ADD ALL GROUP NAMES BEFORE SUBMISSION]
