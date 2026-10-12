# Could Jack Have Been Saved? — Group 1 speaking guide

## Suggested 90-second talk

> "Our question was whether Jack could have been saved. He was fictional, so we defined a comparable passenger as a third-class man aged 18 to 25 with a known age. In the Kaggle training sample, just **10 of 86 — 11.6%** — survived.
>
> Our first chart compares him with third-class women of the same age range: **14 of 30 women (46.7%)** survived. Being a young woman was associated with a strikingly different outcome even within Jack's class.
>
> Next, we asked whether first class would have helped a young man. Among men aged 18 to 30, **40.9% of first-class**, **2.4% of second-class**, and **14.6% of third-class** passengers survived. First class was better than third in this sample, but we found something unexpected: second class was worse than third. The overall class ladder does not apply neatly to every subgroup.
>
> Our final chart shows a rejected hypothesis. Among third-class men aged 18 to 50, recorded family ties did not correlate with higher survival: **3 of 33** survived with close relatives recorded, compared with **25 of 168** without. The group is small, and 'no recorded close relatives' does not mean alone.
>
> We conclude that some Jack-like passengers survived and that class, sex and recorded family circumstances were associated with different outcomes. But we cannot prove what would have happened to an individual Jack: the dataset does not include lifeboat access or evacuation timing."

## Questions to anticipate

**Why did you choose these three charts?** They move from a direct Jack-like comparison, to the nonmonotonic class finding, to a genuinely rejected hypothesis. Rates include denominators. Other charts remain in the notebook.

**Why three different age ranges?** The Jack-like profile was preregistered as 18–25; H2 preregistered 18–30; H3 preregistered 18–50 so the hypothesis groups would be large enough to investigate. All are shown explicitly, not presented as interchangeable cohorts.

**Can you say buying first class would save Jack?** No. Ticket class correlates with other factors and we did not observe evacuation logistics or causal interventions. Our conclusion is about the survival outcomes of comparable real passengers, not a hypothetical individual's guaranteed outcome.

**Is this Simpson's paradox?** We can demonstrate a *ranking reversal* in certain subgroups relative to whole-sample class ordering; we do not claim the strict mathematical conditions for Simpson's paradox are met.

**Why is second-class young male survival so low?** Only one of 41 records with known ages survived in the chosen group. We cannot isolate the cause from this dataset. The rates also change with alternative age bands, and missingness may affect the results.

**Does the rejected family hypothesis mean family makes survival worse?** No. The original directional H3 was not supported in its predefined sample; the recorded-family subgroup is small, and `SibSp`/`Parch` do not encode friends, a romantic partner or every travelling companion. Among men 18–30 in third class the group difference almost disappears.

**What's wrong with the data?** Missing ages unevenly distributed across classes, cabin data missing for nearly all third class, and small groups in important comparisons. Each is quantified in the notebook.

**Why rate rather than count?** First, second and third class have different numbers of passengers; the proportion surviving is the meaningful descriptive comparison.

**Why could another group get different results?** Different Jack proxy, inclusion of missing ages through imputation, wider age bands, or alternative handling of the small family group would change rates. We explicitly document our decisions.

**What is the worst poster misunderstanding?** Treating 40.9% first-class survival as Jack's probability after an upgrade. It is not.

**Why did you keep the rejected hypothesis?** Preserving it is the evidence of honest pre-outcome scientific thinking, as required in the marking brief.

**Before presenting:** insert the 3–4 group names in the poster source footer and README, regenerate the PDF, rehearse with the full-size PDF projected, and verify your GitHub link in a private window.
