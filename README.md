# Mersenne Twister algorithm, as implemented by Python

A *pseudo-random number generator* (PRNG) is an algorithm that produces sequences of numbers $(x_i)_{i\in \mathbb{N}}$ designed 
to imitate independently and identically distributed (IID) random variables from a given distribution. Despite appearing
random, these sequences are entirely deterministic, controlled by an initial value called the *seed*.

Among all probability distributions, the uniform $U(0,1)$ is particularly important because it serves as a
building block for sampling from other distributions. One of the earliest PRNGs for this distribution, the 
[middle-square method](https://en.wikipedia.org/wiki/Middle-square_method), was 
proposed in 1946. Since then, there have been many [improvements](https://en.wikipedia.org/wiki/List_of_random_number_generators#Pseudorandom_number_generators_(PRNGs)).


Here, we focus on the *Mersenne Twister algorithm*, developed in 1997. While it is no longer the best PRNG
available today, it remains the default pseudo-random generator in Python, as well as in many other programming
languages including R, Ruby, MATLAB, and Julia.

While the underlying algorithm is the same across these languages (specifically, the MT19937-32 version), each 
implementation has its own quirks. The goal of this repository is to recreate exactly the same behavior as Python's `random` 
module (which is implemented in C).

## Usage
To initialize the PRNG:
```python
from mersenne_twister import MersenneTwister

generator = MersenneTwister()
```

To generate a number in [0,1):
```python
generator.random()
# Example output: 0.6499291071489846
```

To seed the generator and ensure reproducibility:
```python
generator.seed(42)
```

## Benchmarking against Python's `random` module

This implementation is designed to match Python's built-in PRNG when given the same seed:

```python
import random
from mersenne_twister import MersenneTwister

random.seed(7)
generator = MersenneTwister()
generator.seed(7)

print(generator.random())  # 0.32383276483316237
print(random.random())     # 0.32383276483316237
```