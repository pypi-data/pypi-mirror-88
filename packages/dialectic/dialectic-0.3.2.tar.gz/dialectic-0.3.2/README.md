# Dialectic

Mathematical logic implementation using python.

### Install

```
pip install dialectic
```

### Usage

```python
from dialectic import Atomic

# Atomic objects
a = Atomic('a')
b = Atomic('b')

# Invert
invert = ~a

# Conjunction
conjunction = (a & b)

# Disjunction
disjunction = (a | b)

# Implication
implication = (a > b)

# Equality (iff)
equality = (a == b)

# Validation with given sentence set
implication.validate({a, b})

# Parsing a sentence list
from dialectic import parse_sentences

parsed_set = parse_sentences([implication, a])

# Inference
from dialectic import Inference

is_valid = Inference((a > b), [b]).is_valid_argument()
is_tautology = Inference((a | ~a)).is_tautology()
is_contradictory = Inference((a & ~a)).is_contradictory()
is_contingent = Inference((a & b)).is_contingent()
```