"""Build the classroom research notebook without revising registered hypotheses."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'notebooks' / 'titanic_jack_analysis.ipynb'

cells = []

def md(value: str) -> None:
    cells.append(nbf.v4.new_markdown_cell(value.strip()))


def code(value: str) -> None:
    cells.append(nbf.v4.new_code_cell(value.strip()))

md('''# Could Jack Have Been Saved?
**Group 1 | One Page, One Finding | 19 October 2026**

**Research question:** What would have to be different about a passenger resembling fictional Jack Dawson to be associated with a better *observed* chance of survival?

Our evidence consists of 891 historical passenger records in the Kaggle Titanic **training sample**. Jack is fictional, so the data cannot answer what would have happened to him personally. We do **descriptive pandas analysis only**: no machine learning, prediction, or causal models.

**Research chronology:** Initial dataset profiling and the three unchanged hypotheses were committed on GitHub **before any outcome-based exploratory analysis**. See the original commit `7a423658689667bbf34772da22bb66c945d7ee90`.''')

md('''## 1. Load and profile

Inspect dimensions, data types, missingness, and the meaning of the columns. This is the only inspection completed before writing the three hypotheses.''')
code('''from pathlib import Path
import sys, math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
from matplotlib.ticker import PercentFormatter

ROOT = Path.cwd()
if not (ROOT/'data'/'train.csv').exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT/'src'))
from analysis import load_data, observed, jack_like, young_men, adults, family_group, wilson

df = load_data(ROOT/'data'/'train.csv')
print('Dataset shape (passengers, columns):', df.shape)
print('PANDAS INFO:')
df.info()
print('NULL VALUES:')
print(df.isnull().sum().to_string())
print('NULL PERCENTAGES:')
display((df.isnull().mean()*100).round(1).rename('missing_%').to_frame())
profile = pd.DataFrame({'dtype':df.dtypes.astype(str), 'missing':df.isna().sum(),
                        'missing_%':100*df.isna().mean()})
display(profile.round(1))
print('SAMPLE RECORDS:')
display(df.head(5))''')
md('''**Column dictionary.** `Survived`: observed 0/1 outcome; `Pclass`: ticket class (1–3); `Sex` and `Age`: recorded demographics; `SibSp`: siblings/spouses aboard; `Parch`: parents/children aboard; `Ticket`: ticket identifier; `Fare`: ticket fare recorded; `Cabin`: cabin label; `Embarked`: port code; `PassengerId` and `Name`: passenger identifiers. **The 891 records are not the whole Titanic population, and this Kaggle training set excludes the competition test set.**

**Profiling observation:** 177 ages (19.9%), 687 cabins (77.1%), and two embarkation entries (0.2%) are missing. None of those numbers reveals group survival outcomes.''')

md('''### All 12 original columns explained

| Column | Description | Interpretation |
|---|---|---|
| PassengerId | Unique integer passenger ID | Identifier, not an explanation |
| Survived | 0 = no, 1 = yes | Binary outcome |
| Pclass | 1, 2, or 3 | Ticket-class category |
| Name | Passenger name | Historical record, not fictional Jack |
| Sex | Male or female | Recorded demographic category |
| Age | Age in years | 177 missing ages |
| SibSp | Siblings/spouses aboard | Does not include friends |
| Parch | Parents/children aboard | Not all travelling companions |
| Ticket | Ticket number/reference | May be shared |
| Fare | Recorded fare | Not an individual's income |
| Cabin | Cabin label | Mostly missing |
| Embarked | S, C or Q | Southampton, Cherbourg or Queenstown |

**Profile conclusion:** 891 records and 12 original fields; 177 unknown ages (19.9%), 687 unknown cabins (77.1%), and 2 unknown embarkation ports (0.2%). The other nine fields have no null values. These structural checks do not demonstrate survival causes.''')

md('''## 2. Three hypotheses — written before outcome exploration

**Fixed Jack-like proxy:** male, third-class passenger, **18–25 inclusive**, recorded age. This operational definition cannot identify a fictional character. Wider age bands are allowed only as *labelled exploratory sensitivity checks*, not changes to the registered hypotheses.

**H1 · Sex (directional):** Among passengers aged **18–50 inclusive**, women have higher observed survival rates than men **within each passenger class**. **Test:** compare female and male rates independently in classes 1, 2, and 3; report all denominators.

**H2 · Class (directional):** Among **men aged 18–30 inclusive**, first-class passengers have higher observed survival rates than third-class passengers. **Test:** compare first vs third with denominators and a percentage-point difference; show the second class too when interpreting the *overall* class gradient.

**H3 · Recorded relatives (directional):** Among **third-class men aged 18–50 inclusive**, passengers with `SibSp + Parch > 0` have higher observed survival rates than those with `SibSp + Parch == 0`. **Test:** compare recorded-close-relative groups with counts and rates. Zero is NOT proof of travelling alone.

**Decision criterion:** *SURVIVED* means the observed direction agrees with the stated hypothesis; *NOT SUPPORTED* means it does not. Neither label is a population-level significance claim, and small samples must be disclosed. These hypotheses are preserved exactly from the earlier preregistered GitHub version.''')

md('''## 3. Cleaning — every decision has a reason

| Data issue or decision | Action | Why it matters |
|---|---|---|
| Raw data must be auditable | Keep `train.csv` unchanged; analyze a copy | Reproducibility and provenance |
| Duplicate records | Check whole rows and unique `PassengerId`; do not deduplicate valid IDs | Avoid treating ticket sharers as duplicate passengers |
| Missing `Age` | Do **not** impute; exclude missing-age rows **only for age-dependent comparisons** | Filling ages would invent Jack-like membership and can distort rates |
| Missing `Cabin` | Preserve nulls; do **not** use cabin availability as a survival intervention | Missingness is severe and differs by class |
| Family status | Derive `RecordedRelatives = SibSp + Parch > 0` | Counts only certain relatives, **not** friends or other companions |
| `Fare` | Keep raw; do not equate it with individual wealth or individual rescue access | Tickets and fares can be shared/complex |
| `Embarked` missing in two records | Leave missing; they do not affect our core tests | Avoid unjustified fabrication or unnecessary row loss |''')
code('''assert df.PassengerId.is_unique
print('Entire-row duplicates:',df.duplicated().sum())
print('Missing ages:',df.Age.isna().sum(),'; zero recorded fares:',int((df.Fare==0).sum()))
clean = df.copy()
clean['RecordedRelatives'] = (clean.SibSp+clean.Parch)>0
assert len(clean)==len(df)
print('No passenger was deleted from the master dataset. Age restrictions will be explicit per analysis.')''')

md('''## 4. Explore: distributions before relationships

Start with what the sample contains, **not** with which conclusion looks attractive. Charts discarded from the final poster stay here.''')
md('''### Statistical summary for every column

Use `df.describe()` for numeric count, mean, standard deviation, quartiles and range; use `df.describe(include=['object'])` for text-column count, unique values, most frequent value and its frequency; and use `df.describe(include='all')` to cover all twelve columns. `PassengerId` is an identifier and `Pclass` is a coded category, so their arithmetic means are not meaningful continuous measurements.

**Data overview:** 342/891 (38.4%) passengers survived and 549/891 (61.6%) did not. There were 577 men, 314 women; 216 first-class, 184 second-class and 491 third-class passengers. Among 714 known ages, mean age was 29.70 years, median 28, range 0.42–80. Mean recorded fare was 32.20, median 14.45, maximum 512.33. The large fare mean relative to the median suggests a strongly right-skewed distribution.

**Interpretation:** These descriptive statistics summarize the training sample, not all Titanic passengers. Groups have different sizes, and age/cabin missingness limits comparisons. Test subgroup survival **rates with denominators**, not raw survival counts.''')
code('''print('All 12 original fields — comprehensive describe:')
display(clean[df.columns].describe(include='all').T.round(2))
print('Text and category summary:')
display(clean[df.columns].describe(include=['object']).T)
for field in ['Survived','Sex','Pclass','Embarked']:
    print('Value counts:',field)
    display(clean[field].value_counts(dropna=False).rename('passengers').to_frame())''')
code('''print('Descriptive statistics (recorded ages only):')
display(clean[['Age','Fare','SibSp','Parch']].describe().round(1))
display(pd.crosstab(clean.Pclass,clean.Sex,margins=True))
fig,axes=plt.subplots(1,3,figsize=(14,3.5))
clean.Age.dropna().hist(ax=axes[0],bins=24,color='#DF4D70')
axes[0].set(xlabel='Age (years)',ylabel='Passengers',title='Age distribution (known ages)')
clean.Pclass.value_counts().sort_index().plot.bar(ax=axes[1],color='#39445B',rot=0)
axes[1].set(xlabel='Ticket class',ylabel='Passengers',title='Class distribution')
clean.Sex.value_counts().plot.bar(ax=axes[2],color='#9B8A98',rot=0)
axes[2].set(xlabel='Recorded sex',ylabel='Passengers',title='Sex distribution')
plt.tight_layout();plt.show()''')
code('''overall=clean.Survived.agg(['sum','count','mean'])
print(f'Overall observed survival: {int(overall["sum"])}/{int(overall["count"])} = {overall["mean"]:.1%}')
by_sex_class=observed(clean,['Pclass','Sex'])
display(by_sex_class)
ax=by_sex_class['rate'].unstack('Sex').plot.bar(figsize=(9,4),color=['#DF4D70','#343D56'],rot=0)
ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_ylim(0,1)
ax.set(xlabel='Passenger class',ylabel='Survival rate',title='Overall survival is not evenly distributed by class or sex')
plt.tight_layout();plt.show()''')
md('''**Why we do not compare raw survivor counts alone:** Class sizes differ, and sex composition differs within class. A class with more survivors could merely contain more passengers. Conditional **rates with numerators and denominators** are the appropriate comparison.''')
code('''clean['AgeBand']=pd.cut(clean.Age,[-0.01,12,17,25,35,50,65,110],
    labels=['0–12','13–17','18–25','26–35','36–50','51–65','66+'])
print('Age-band survival (recorded ages only):')
display(observed(clean,'AgeBand'))
fig,ax=plt.subplots(figsize=(9,3.6))
rg=observed(clean,'AgeBand').reset_index()
ax.bar(rg['AgeBand'].astype(str),rg.rate*100,color='#DF4D70')
ax.set_ylim(0,100);ax.set(xlabel='Recorded age band',ylabel='Survival rate (%)',title='Age patterns differ, but missing ages complicate comparisons')
for i,r in rg.iterrows():ax.text(i,r.rate*100+2,f'n={int(r.passengers)}',ha='center',fontsize=9)
plt.tight_layout();plt.show()
print('Recorded relatives overall (NOT the H3 test):')
display(observed(clean,'RecordedRelatives'))''')

md('''### Jack-like baseline and prespecified robustness exploration

The proxy was defined before viewing results. Any sensitivity band is an additional **exploratory** analysis, not a redefinition of Jack or H2/H3.''')
code('''jack=jack_like(clean)
print(f'Jack-like men (third class, age 18–25): {int(jack.Survived.sum())}/{len(jack)} = {jack.Survived.mean():.1%}')
for high in (25,30,35):
    sub=clean.loc[(clean.Sex=='male')&(clean.Pclass==3)&clean.Age.between(18,high)]
    print(f'Third-class men ages 18–{high}: {int(sub.Survived.sum())}/{len(sub)} = {sub.Survived.mean():.1%}')
print('Same-age (18–25) women in third class for context:')
peers=clean.loc[(clean.Pclass==3)&clean.Age.between(18,25)]
display(observed(peers,'Sex'))''')

md('''## 5. Test the original three hypotheses

**The hypotheses below are reported as registered; none has been rewritten to match the results.** Every result uses the numerator, denominator and percentage-point difference (not a raw-count comparison).''')
code('''# H1 — Female rate > male rate in EACH class, among ages 18–50
h1=observed(adults(clean),['Pclass','Sex'])
display(h1)
h1_outcomes=[]
for c in (1,2,3):
    f=h1.loc[(c,'female')];m=h1.loc[(c,'male')]
    h1_outcomes.append(f.rate>m.rate)
    print(f'Class {c}: women {int(f.survived)}/{int(f.passengers)} = {f.rate:.1%}; '
          f'men {int(m.survived)}/{int(m.passengers)} = {m.rate:.1%}; '
          f'gap {100*(f.rate-m.rate):+.1f} percentage points')
print('H1:', 'SURVIVED' if all(h1_outcomes) else 'NOT SUPPORTED')''')
code('''# H2 — First-class versus third-class young men; second class also shown to test easy narratives.
h2=observed(young_men(clean),'Pclass')
display(h2)
for c,r in h2.iterrows():
    lo,hi=wilson(int(r.survived),int(r.passengers))
    print(f'Class {c}: {int(r.survived)}/{int(r.passengers)} = {r.rate:.1%} '
          f'(95% Wilson interval approx. {lo:.1%}–{hi:.1%})')
gap=100*(h2.loc[1,'rate']-h2.loc[3,'rate'])
print(f'First vs third gap: {gap:+.1f} percentage points')
print('H2:', 'SURVIVED' if gap>0 else 'NOT SUPPORTED')
print('IMPORTANT CONTRADICTION TO A SIMPLE CLASS LADDER: '
      'the second-class rate is LOWER than the third-class rate in this age/sex group.')
fig,ax=plt.subplots(figsize=(8.5,3.7))
ax.bar(['1st class','2nd class','3rd class'],h2.rate*100,color=['#43516A','#DF4D70','#9C9BAB'])
ax.set_ylim(0,100);ax.set(ylabel='Observed survival rate (%)',title='Young men did not follow a simple three-class survival ladder')
for i,(_,r) in enumerate(h2.iterrows()):ax.text(i,r.rate*100+2,f'{r.rate:.1%} · n={int(r.passengers)}',ha='center',fontsize=10)
plt.tight_layout();plt.show()''')
code('''# H3 — Recorded close relatives in third-class men aged 18–50
h3=observed(family_group(clean),'RecordedRelatives')
display(h3)
yes=h3.loc[True];no=h3.loc[False]
for label,r in [('Recorded relatives',yes),('No relatives recorded',no)]:
    lo,hi=wilson(int(r.survived),int(r.passengers))
    print(f'{label}: {int(r.survived)}/{int(r.passengers)} = {r.rate:.1%} '
          f'(95% Wilson interval approx. {lo:.1%}–{hi:.1%})')
print(f'Observed gap (with minus without): {100*(yes.rate-no.rate):+.1f} percentage points')
print('H3:', 'SURVIVED' if yes.rate>no.rate else 'NOT SUPPORTED')
print('A rejected directional hypothesis does NOT establish that family has no effect.')''')

md('''### Confront the central trap: aggregation and subgroup instability

In the **full training sample**, overall survival increases from third to second to first class. But for **men aged 18–30 with known ages**, second class has a lower observed rate than third class. This is a **subgroup ranking reversal**, not evidence that second-class tickets caused harm, and not by itself proof of a formal Simpson's paradox. Sex/age composition and sampling uncertainty complicate the picture.''')
code('''print('Overall class rates (all recorded ages, both sexes):')
display(observed(clean,'Pclass'))
print('Young men ages 18–30 class rates:')
display(h2)
print('SENSITIVITY: class pattern among men at alternative upper-age cutoffs')
for high in (25,30,35,50):
    rows=observed(young_men(clean,18,high),'Pclass')
    print(f'Ages 18–{high}:', '; '.join(f'class {c}: {int(r.survived)}/{int(r.passengers)} ({r.rate:.1%})' for c,r in rows.iterrows()))
print('SENSITIVITY: H3 family association for ages 18–30 instead of registered 18–50:')
fam=young_men(clean,18,30).query('Pclass==3').copy()
fam['RecordedRelatives']=(fam.SibSp+fam.Parch)>0
display(observed(fam,'RecordedRelatives'))''')
md('''**Interpretation:** H1 survived all three within-class tests; H2 survived the prespecified first-versus-third comparison but class was **not monotonically associated** with survival in young men; H3 was **NOT SUPPORTED** and the family result changes noticeably under a narrower exploratory age filter. We would not claim that having recorded relatives increased or decreased the chance of rescue from these data alone.''')

md('''## 6. Three evidence-backed problems with the dataset

The task is to *prove* problems, not merely report there are blanks. The three problems below are quantified and each directly affects the Jack question.

**Problem 1 — Ages are systematically unevenly recorded across groups.** Missingness changes the denominator of every Jack-like analysis. Compare the missing share by sex/class and by recorded survival outcome. This is evidence against treating known ages as a simple representative cross-section, not proof of why ages are missing.

**Problem 2 — The `Cabin` column is not a reliable proxy for where passengers were located.** It is missing for the great majority of passengers, especially lower classes; comparisons restricted to known cabins would select a very different mix of travellers.

**Problem 3 — Tiny comparison groups make dramatic rates fragile.** The first-class young-men group has only 22 people and the family-positive third-class adult-male group has 33. Show denominators and approximate intervals; do not turn rate gaps into individual predictions.

An additional **scope limitation**: the 891 Kaggle training records exclude competition-test passengers and crew, and there is no lifeboat access or evacuation timeline.''')
code('''# Evidence for the three problems
print('Problem 1: missing ages by class and sex')
age_miss=clean.groupby(['Pclass','Sex']).Age.agg(
    missing=lambda s:int(s.isna().sum()),total='size',fraction_missing=lambda s:s.isna().mean())
display(age_miss.round(3))
print('Age missingness by observed survival outcome:')
display(pd.crosstab(clean.Survived,clean.Age.isna(),normalize='index').rename(columns={False:'age recorded',True:'age missing'}).round(3))
print('Problem 2: missing cabins by class')
cabin_miss=clean.groupby('Pclass').Cabin.agg(
    missing=lambda s:int(s.isna().sum()),total='size',fraction_missing=lambda s:s.isna().mean())
display(cabin_miss.round(3))
print('Problem 3: small-n comparisons with intervals:')
for label,r in [('First-class young men',h2.loc[1]),('Second-class young men',h2.loc[2]),
                ('Third-class young men',h2.loc[3]),('Third-class adult men with recorded relatives',h3.loc[True])]:
    lo,hi=wilson(int(r.survived),int(r.passengers))
    print(f'{label}: {int(r.survived)}/{int(r.passengers)} ({r.rate:.1%}), '
          f'approx 95% interval {lo:.1%}–{hi:.1%}')''')
code('''fig,axes=plt.subplots(1,2,figsize=(11,3.7))
m_age=clean.groupby('Pclass').Age.apply(lambda s:100*s.isna().mean())
m_cabin=100*clean.groupby('Pclass').Cabin.apply(lambda s:s.isna().mean())
for ax,series,title in ((axes[0],m_age,'Age missingness differs by class'),
                        (axes[1],m_cabin,'Cabin missingness differs dramatically by class')):
    ax.bar([str(i) for i in series.index],series.values,color=['#43516A','#9C9BAB','#DF4D70'])
    ax.set_ylim(0,105);ax.set(xlabel='Passenger class',ylabel='Missing (%)',title=title)
    for i,v in enumerate(series):ax.text(i,v+2,f'{v:.1f}%',ha='center')
plt.tight_layout();plt.show()''')

md('''## 7. Conclusion and limitations

**Answer:** Only **10 of 86 (11.6%)** third-class men aged 18–25 with known ages survived in this training sample. Among men aged 18–30, survival was **9/22 (40.9%)** in first class, **1/41 (2.4%)** in second class, and **19/130 (14.6%)** in third class. Being a first-class young man was associated with a higher observed survival rate than being a third-class young man (**+26.3 percentage points**), **but class was not a simple survival ladder**.

**Original hypothesis decisions:** H1 **SURVIVED** (within each class, adult women had higher observed rates), H2 **SURVIVED** (first-class vs third-class young men), H3 **NOT SUPPORTED** (recorded relatives were not associated with higher observed survival in the registered adult third-class male group).

**What this cannot establish:** Jack did not exist in the data; observations do not show what would have happened had he changed a characteristic. The sample is not a complete record of those aboard and lacks lifeboat access, evacuation timing, detailed location and social processes. Age and cabin are incompletely recorded, group composition differs, and small denominators make comparisons imprecise. Rates must not be interpreted as the causal effect of upgrading a ticket, of sex, or of having family present.

**Why the rejected hypothesis remains:** The question was genuinely asked in advance. Removing it now would conceal an important uncertainty and undermine the research chronology.

**Data source:** [Kaggle Titanic competition, `train.csv`](https://www.kaggle.com/c/titanic/data). The raw file is preserved under `data/`.''')

NOTEBOOK.parent.mkdir(parents=True, exist_ok=True)
nb = nbf.v4.new_notebook(cells=cells,metadata={
    'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
    'language_info':{'name':'python'}
})
nbf.write(nb,NOTEBOOK)
print(f'Created {NOTEBOOK}: {len(cells)} cells')
