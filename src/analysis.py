"""Transparent descriptive computations shared by the notebook, poster, and tests.

No predictive models and no claim of a causal effect on individual survival.
"""
from __future__ import annotations

from math import sqrt
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'train.csv'


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    data = pd.read_csv(path)
    assert data.shape == (891, 12), 'Expected the official Kaggle Titanic train.csv'
    assert data.PassengerId.is_unique, 'Duplicate passenger IDs require investigation'
    assert data.Survived.isin([0, 1]).all()
    assert data.Pclass.isin([1, 2, 3]).all()
    assert data.Sex.isin(['male', 'female']).all()
    assert data.Age.dropna().between(0, 110).all()
    return data


def observed(data: pd.DataFrame, keys: list[str] | str) -> pd.DataFrame:
    return data.groupby(keys, observed=True, dropna=False).Survived.agg(
        survived='sum', passengers='count', rate='mean'
    )


def jack_like(data: pd.DataFrame) -> pd.DataFrame:
    return data.loc[(data.Sex == 'male') & (data.Pclass == 3) & data.Age.between(18, 25)]


def young_men(data: pd.DataFrame, low: int = 18, high: int = 30) -> pd.DataFrame:
    return data.loc[(data.Sex == 'male') & data.Age.between(low, high)]


def adults(data: pd.DataFrame) -> pd.DataFrame:
    return data.loc[data.Age.between(18, 50)]


def family_group(data: pd.DataFrame) -> pd.DataFrame:
    people = data.loc[(data.Sex == 'male') & (data.Pclass == 3) & data.Age.between(18, 50)].copy()
    people['RecordedRelatives'] = (people.SibSp + people.Parch) > 0
    return people


def wilson(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Approximate 95% Wilson interval for the observed binary rate."""
    if total <= 0:
        return float('nan'), float('nan')
    p = successes / total
    denominator = 1 + z*z/total
    midpoint = (p + z*z/(2*total))/denominator
    half = z*sqrt(p*(1-p)/total + z*z/(4*total*total))/denominator
    return midpoint-half, midpoint+half


def summaries(data: pd.DataFrame) -> dict:
    jack = jack_like(data)
    h1 = observed(adults(data), ['Pclass', 'Sex'])
    h2 = observed(young_men(data), 'Pclass')
    h3 = observed(family_group(data), 'RecordedRelatives')
    return {
        'jack': {'survived': int(jack.Survived.sum()), 'passengers': len(jack), 'rate': jack.Survived.mean()},
        'h1': h1,
        'h2': h2,
        'h3': h3,
    }


if __name__ == '__main__':
    d = load_data()
    s = summaries(d)
    print('Jack-like:', s['jack'])
    for key in ('h1', 'h2', 'h3'):
        print('\n', key, '\n', s[key])
