# COSDEM
Cosdem is a python package for comparing statistical differences of measurements in two-dimension data especially equivalent medical devices

## Introduction 

**Cosdem** aims to compare two-dimension data with many statistical tests and graphs in one method. 

As an open-source tasking library, **cosdem**, provides one report on the following tests and graphs:
### Tests
- Descriptive Statistics 
- Homogeneity Tests of Variances
- Normality Test: Shapiro Wilk
- Statistical Difference Tests
- Correlation Tests
- Regression Result

###Graphs
- Violin Plot
- Regression Line in Scatter Plot
- Blant Altman Plot

## Installation

Prerequisites: `python3 >= 5` and `pip3`.

``` pip install cosdem ```

or

``` git clone git@github.com:yigitsener/cosdem.git ```

## Usage

```python
from cosdem import Cosdem
import pandas as pd
import random

a = []
b = []
for i in range(50):
    a.append(random.uniform(10,15))
    b.append(random.uniform(10,15))

df = pd.DataFrame({"Feature A":a, "Feature B":b})

tests = Cosdem(df)

```
## Functions

Text results
```python
print(tests.report())
```

Save all tables in Excel file
```python
print(tests.save_all_tables())
```

Save all graphs/figures in Excel file
```python
print(tests.save_all_figures())
```