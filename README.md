# Could Jack Have Been Saved?

**The Jack File · Storytelling, data analysis, and front-end design**

### [Explore the live Titanic website →](https://elonaelon000.github.io/could-jack-have-survived/)

[Read the executed notebook](https://elonaelon000.github.io/could-jack-have-survived/docs/notebook.html) · [Open the one-page poster](https://elonaelon000.github.io/could-jack-have-survived/docs/titanic_jack_poster.pdf) · [Open in Google Colab](https://colab.research.google.com/github/elonaelon000/could-jack-have-survived/blob/feature/titanic-interactive-exhibit/notebooks/titanic_jack_analysis.ipynb)

[![The live Titanic website opens with Jack's story](https://raw.githubusercontent.com/elonaelon000/could-jack-have-survived/feature/titanic-interactive-exhibit/docs/preview-desktop.jpg)](https://elonaelon000.github.io/could-jack-have-survived/)

The film asks us to imagine a different ending. This project asks what the real passenger records can support. Start with Jack's story, understand the dataset, and explore the evidence through an interactive Titanic-themed website.

**Jack is fictional. The 891 passenger records are real. No predictive model is trained, and no comparison establishes his individual fate.**

## The finding

Among third-class men aged **18–25 with recorded ages**, **10 of 86 survived (11.6%)**. Among men aged **18–30**, the recorded rates were **9/22 in first class, 1/41 in second, and 19/130 in third**. First class exceeded third in that comparison, but class was not a simple survival ladder.

## Why three age ranges?

These are **overlapping analysis windows, not three separate age categories**. A 22-year-old belongs to all three. Bounds are inclusive; passengers with unknown ages are excluded only from age-dependent comparisons.

| Window | Purpose | Trade-off |
|---|---|---|
| **18–25 · Jack-like** | Male, third-class baseline, close to the young fictional character. | A narrower profile, but small comparison groups. |
| **18–30 · H2** | Compare first- and third-class young men; also show second class. | Includes more passengers while retaining a young-adult window. |
| **18–50 · H1 and H3** | H1 compares women and men within each class; H3 compares recorded relatives versus none among third-class men. | Broader adult groups, less specific to Jack; not all adult ages. |

The operational definitions were recorded in [the original hypothesis commit](https://github.com/elonaelon000/could-jack-have-survived/commit/7a423658689667bbf34772da22bb66c945d7ee90). **The explanation above is a later methodological clarification, not a new preregistration.** The cutoffs are design choices, not statistically optimized boundaries. A larger group is not automatically a better comparison, and a shared age window does not fully control for age.

The website selector changes **only the age filter**. Choosing an H1/H3 window does not perform those comparisons by itself; sex, class and recorded-relative filters still matter.

[Read the full age-window explanation](https://elonaelon000.github.io/could-jack-have-survived/docs/methods.html)

## Explore the work

The website combines a story-first introduction, six dataset-feature panels, 54 passenger-profile combinations with denominators and uncertainty, and direct access to the research deliverables. The optional alternate-rescue sequence is an explicitly fictional browser animation, not historical footage or an AI-generated film.

**Learning the analysis:** [Notebook explained in Albanian, code cell by code cell](https://elonaelon000.github.io/could-jack-have-survived/docs/notebook-guide-sq.html).

H1 and H2 agree with the registered **observed directions**; H3 is **not supported** in its registered group. These are descriptive checks, not claims of statistical significance or causation. Unknown ages, missing cabins, and small subgroups remain substantive limitations.

## Run locally

The live implementation and updated deliverables are on **`feature/titanic-interactive-exhibit`** while [PR #1](https://github.com/elonaelon000/could-jack-have-survived/pull/1) remains separate from the original analysis on `main`.

```bash
git clone --branch feature/titanic-interactive-exhibit https://github.com/elonaelon000/could-jack-have-survived.git
cd could-jack-have-survived
python -m http.server 8000 --directory docs
```

Open `http://localhost:8000`. To rebuild the notebook, poster, website and learning notes with Python 3.10+:

```bash
python -m pip install -r requirements.txt
python src/build.py
python -m pytest -q tests
```

The portable notebook embeds the original CSV with a checksum and can be uploaded to Google Colab. No repository checkout is required for that downloaded notebook.

## Team and sources

**Group 1 : Elona Tarja ·  Kleant Laboti · Sarita Koci**

[Assignment](https://evisp.github.io/ml-handbook/projects/one-page-finding/) · [Kaggle dataset](https://www.kaggle.com/competitions/titanic/data) · [Original screenplay](https://imsdb.com/scripts/Titanic.html) · [Artwork attribution](https://github.com/elonaelon000/could-jack-have-survived/blob/feature/titanic-interactive-exhibit/docs/assets/ATTRIBUTION.md)

The historical artwork is a public-domain interpretation of the sinking; it is not a photograph or a reconstruction of passengers' evacuation routes.
