# Package: generalvector
Vectors, featuring Vec and Vec2, inspired by Expression 2* in Wiremod inside Garry's Mod. 

The vectors are immutable, so any time a value inside one is changed it returns a new vector.

The bulk of the code is written twice, with one verion in vector and one version in vector2. I've begun adding new functions into general instead which both vectors inherit from, to make the code DRY. The GeneralVector class can take an arbitrary amount of axis which allows us to easily add, for example, a Vec4 in the future if all code is moved to general.

*https://github.com/wiremod/wire/wiki/Expression-2


## Installation
```
pip install generalvector
```

## Features
| Module   | Name   | Explanation       |
|:---------|:-------|:------------------|
| vector   | Vec    | Immutable vector  |
| vector2  | Vec2   | Immutable vector2 |

## Vector methods
| Name       | Explanation                                                                                                 |
|:-----------|:------------------------------------------------------------------------------------------------------------|
| absolute   | Return this vector with absolute values.                                                                    |
| confineTo  | Confine this vector to an area, but unlike clamp it subtracts axis * n to create an 'infinite' area effect. |
| sanitize   | Sanitize this vector with a bunch of optional flags.                                                        |
| clamp      | Get this vector clamped between two values as a new vector.                                                 |
| distance   | Return distance between two Vectors.                                                                        |
| hex        | Get a hex based on each value. Rounded and clamped between 0 and 255.                                       |
| inrange    | Return whether this vector is between two other vectors.                                                    |
| length     | Get the length of this vector using pythagorean theorem.                                                    |
| max        | Get a new vector containing the maximum value for each value in the two vectors.                            |
| min        | Get a new vector containing the minimum value for each value in the two vectors.                            |
| normalized | Get this vector normalized by dividing each value by it's length.                                           |
| range      | Get a range from two vectors.                                                                               |
| round      | Get this vector with each value rounded.                                                                    |

## Usage example
```python
from generalvector import Vec, Vec2
assert Vec(3) + 2 == Vec(5, 5, 5)
assert Vec2(3, 4).length() == 5
```

## Releases
#### generalvector 1.5
 * Moved test folder to inside generalvector package
 
#### generalvector 1.4
 * Updated readme

## Todo
 * Move everything to general.py