# Titanic dataset — profile, characteristics and conclusion

**Dataset:** Kaggle Titanic training sample (891 rows, 12 fields). Source: https://www.kaggle.com/c/titanic/data

Use `df.shape` for dimensions; `df.info()` for data types and non-null counts; `df.isnull().sum()` for missingness; `df.describe()` and `df.describe(include='all')` for statistical summaries. The notebook contains runnable code and explanations of every column.

| Field | Missing | Share |
|---|---:|---:|
| Age | 177 | 19.9% |
| Cabin | 687 | 77.1% |
| Embarked | 2 | 0.2% |
| The other nine fields | 0 | 0% |

**Descriptive results:** 342 survived and 549 did not (38.4% survived). Male: 577; female: 314. Ticket classes: first 216, second 184, third 491. Ages are recorded for 714 passengers: mean 29.70 years, median 28, range 0.42–80. Mean fare 32.20, median 14.45, maximum 512.33. `Pclass` and `PassengerId` are encoded labels/identifiers, not meaningful continuous measurements.

**Qualified finding:** In the predefined group of third-class men aged 18–25, 10 of 86 (11.6%) survived. Among men aged 18–30, rates were 9/22 (40.9%) first class, 1/41 (2.4%) second class, and 19/130 (14.6%) third class. The second-class reversal warns against overgeneralizing from class averages. This training sample is incomplete, and neither observational comparisons nor summary statistics establish that changing Jack's class would have saved him.