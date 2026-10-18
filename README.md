# Could Jack Have Been Saved?

**The Jack File** - Group 1 / One Page, One Finding  
**Kleant Laboti | Elona Tarja | Sarita Koci**

A Titanic-themed interactive research exhibit with a reproducible pandas analysis. No trained models, individual predictions, or invented historical evidence.

## Start here

| Open | Purpose |
|---|---|
| [Interactive exhibit](docs/index.html) | Jack's story, the research finding, 54 selectable passenger profiles, and an explicitly fictional motion storyboard. Serve locally or through Pages; GitHub's file viewer does not execute HTML. |
| [One-page PDF poster](poster/titanic_jack_poster.pdf) | Exactly three code-generated charts, visible denominators, group names, and one consequential limitation. |
| [Canonical notebook](notebooks/titanic_jack_analysis.ipynb) | The single final analysis, executed and self-contained. |
| [Browser-readable notebook](docs/notebook.html) | Executed cells, tables and charts without a notebook runtime. |
| [Presentation and audit notes](docs/EXHIBIT_AUDIT.md) | What changed, the rubric, and what remains a human check. |

## One finding

Only **10 of 86 (11.6%)** third-class men aged 18-25 with recorded ages survived in the Kaggle training sample. Among men aged 18-30, first class had **9/22 (40.9%)**, second **1/41 (2.4%)**, and third **19/130 (14.6%)** survivors. Class was not a simple survival ladder in this subgroup. None of these comparisons proves what would happen to a fictional Jack after changing his ticket.

## Reproduce everything

Python 3.10 or newer:

```bash
python -m pip install -r requirements.txt
python src/build.py
python -m pytest -q tests
python -m http.server 8000 --directory docs
```

Open `http://localhost:8000`. The exhibit uses plain HTML, CSS and JavaScript, no front-end build system, CDN, analytics, paid service, or external rendering dependency.

The build preserves `data/train.csv`, keeps the original hypothesis generator, creates a portable notebook, executes every cell, regenerates the three-chart poster, and publishes the results to `docs/`. Website profile statistics are computed from the source data, not manually guessed.

## Google Colab

Download `docs/titanic_jack_analysis.ipynb`, open Google Colab, choose **File > Upload notebook**, then **Runtime > Run all**. The notebook embeds a compressed copy of the exact original CSV and the helper functions, validates the original SHA-256, and does not require a repository checkout or network data download. Pandas, NumPy and Matplotlib are its analysis dependencies.

The [direct GitHub-to-Colab link](https://colab.research.google.com/github/elonaelon000/could-jack-have-survived/blob/main/notebooks/titanic_jack_analysis.ipynb) uses `main` and requires repository access. Before merging the exhibit branch, use that branch's downloaded notebook instead.

## Research integrity

The original operational definitions precede outcome exploration in commit [`7a423658`](https://github.com/elonaelon000/could-jack-have-survived/commit/7a423658689667bbf34772da22bb66c945d7ee90): H1 ages 18-50 within class; H2 men 18-30, first versus third; H3 third-class men 18-50, recorded close relatives versus none recorded. Jack's primary proxy remains male, third class, known age 18-25.

H1 and H2 **survived in observed direction**; H3 was **not supported**. These are descriptive decisions, not claims of statistical significance. Wilson intervals do not remove selection bias, missingness, confounding, or family dependence. The alternative notebook is preserved under `archive/` and is **not** a second final or preregistered analysis.

## Publishing status

Implementation and publication are separate. No public URL is claimed until deployment is verified. Repository visibility is not changed by this code.

To publish the built site, configure **Settings > Pages > Deploy from a branch**, choose the branch containing this work and **/docs**, then verify the resulting URL in a signed-out browser. GitHub Free requires a public repository for Pages; eligible paid plans can publish from a private source repository. The professor separately requires a repository link accessible from a private browser window.

The branch build workflow regenerates and checks the deliverables, then commits only the generated files to its own branch. It does not publish a website, change permissions, or modify another branch.

## Sources

- [Assignment](https://evisp.github.io/ml-handbook/projects/one-page-finding/)
- [Kaggle Titanic data](https://www.kaggle.com/c/titanic/data) and [local provenance](data/DATA_SOURCE.md)
- [Film context: Paramount Pictures](https://www.paramountpictures.com/movies/titanic)
- [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

The story's emotional interpretation is editorial. The ship artwork and motion sequence are original stylized visuals, not film footage, an AI-generated movie, or evidence of an actual rescue.
