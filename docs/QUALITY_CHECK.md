# Exhibit QA - 19 October 2026

The updated exhibit was built and verified locally before committing the source. The branch workflow repeats the data, notebook and poster checks before writing generated deliverables.

- Original CSV SHA-256 preserved, with 891 rows and 12 fields.
- Original hypothesis populations retained. The alternative notebook is archived unchanged, not a second canonical submission.
- Thirteen automated tests passed locally, including execution from an empty directory, all 54 profile calculations, Wilson endpoints, local resource links, and a one-page landscape PDF.
- Browser checks passed at 320, 390, 768, 1024 and 1440 pixels without horizontal overflow.
- All 54 browser profile displays matched the CSV-derived evidence.
- Dialog navigation, Escape, focus return and reduced motion checked; no JavaScript errors detected.
- Poster was rendered and visually inspected. Exactly three code-generated axes, labeled cohorts and denominators, team names, and one substantive limitation.

Not yet verified by these local tests: public hosting, a signed-out visitor's repository access, classroom projection, or each group member's understanding. GitHub Actions completion is a separate status from local validation.
