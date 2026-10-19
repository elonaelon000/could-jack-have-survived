# Why 18–25, 18–30 and 18–50?

**Methodological clarification added on 19 October 2026.** This explanation was written after analysis. The age cutoffs themselves already appear in the [original hypothesis commit](https://github.com/elonaelon000/could-jack-have-survived/commit/7a423658689667bbf34772da22bb66c945d7ee90). This document does not create a new preregistration or claim that a sample-size calculation established optimal cutoffs.

## They overlap; they are not three age categories

These are three alternative **analysis windows**. A 22-year-old belongs to all three, a 28-year-old to the last two, and a 42-year-old only to 18–50. Never add their denominators together as though they describe disjoint groups.

The endpoints are inclusive: `Age.between(18, 25)` selects recorded ages satisfying `18 <= Age <= 25`. Unknown ages cannot establish membership, so those passengers are excluded from age-dependent comparisons, not deleted from the master dataset. Fractional ages are not rounded into a group.

## What each window does

| Window | Full analysis population | Comparison or purpose |
|---|---|---|
| 18–25 / Jack-like | Male, third class, known age 18–25 | Primary character-proxy baseline. The first poster chart also compares women and men within third class at these ages. |
| 18–30 / H2 | Male, known age 18–30 | First-class versus third-class observed survival. Second class is also displayed to avoid hiding its different ranking. |
| 18–50 / H1 | All recorded classes, known age 18–50 | Female versus male observed survival separately within each class. |
| 18–50 / H3 | Male, third class, known age 18–50 | `SibSp + Parch > 0` versus `SibSp + Parch == 0`. |

H1 is not the same comparison as poster chart 1: H1 includes all three classes and ages 18–50, while the poster's contextual comparison uses third class and ages 18–25. The notebook reports the original H1 test separately.

## The reasoning and its cost

The narrow window prioritizes similarity to a young fictional character. The wider windows allow broader comparisons with more passengers. That is a trade-off between specificity and sample size, not proof that the wider group is more accurate.

The results illustrate the trade-off: first-class men aged 18–25 number only 10, with 3 survivors; at 18–30 there are 22, with 9 survivors. One different outcome changes the first rate by 10 percentage points. These are observations made during analysis, **not evidence that those outcome counts justified the original choice in advance**.

The exact endpoints 25, 30 and 50 are project design choices. They are not biologically necessary boundaries or statistically optimized thresholds. Ages 18–50 are a restricted adult group, not every adult passenger. A shared age window also does not fully adjust for age: two classes can have different age distributions even inside that window.

## What the website selector actually does

The dropdown changes only the age condition. The H1/H3 label reminds readers which registered questions use that window; selecting it does not automatically test those hypotheses.

For H1, keep class fixed and compare female and male groups at ages 18–50, without restricting relatives. Repeat for each class. For H3, keep male, third class and ages 18–50 fixed, then compare one-or-more versus no recorded close relatives. For H2, keep male and ages 18–30 fixed and compare ticket classes without restricting relatives.

Other combinations in the 54-profile explorer are descriptive exploration. Do not present every clicked combination as an originally registered hypothesis.

## Why the original windows stay visible

Changing the age range can change the answer. For example, among third-class men 18–50, survival with relatives recorded is 3/33 versus 25/168 with none recorded. At 18–25 the corresponding counts are 3/11 versus 7/75. This sensitivity is informative, but the narrower result does not replace H3's registered population.

Changing an age range after seeing results is allowed as a clearly labeled exploratory check. Silently replacing the original range to obtain a preferred result is not. The first hypothesis commit remains unchanged.

## A sentence for the presentation

> We used 18–25 for the closest Jack-like group and separately specified wider windows for the comparisons. This trades similarity to the character against subgroup size. The cutoffs are transparent design choices, not proven optimal boundaries, so every result is interpreted for its own population.

## Sources and implementation

Definitions come from the [initial notebook](https://github.com/elonaelon000/could-jack-have-survived/blob/7a423658689667bbf34772da22bb66c945d7ee90/notebooks/titanic_jack_analysis.ipynb); counts come from the unchanged repository CSV and the [generated evidence](https://elonaelon000.github.io/could-jack-have-survived/docs/evidence.json). Endpoint behavior is documented by [pandas Series.between](https://pandas.pydata.org/docs/reference/api/pandas.Series.between.html). The original age filters, outcome values and hypothesis decisions have not been changed by this clarification.
