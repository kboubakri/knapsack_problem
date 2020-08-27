# Algorithms in Logistics : the KnapSack Problem

## Context and introduction 
The knapSack problem is a very famous problem of combinatorial optimization as it is one of the 21 NP-complete problems presented by Richard Karp in 1971 . 

It appears in many situation in transport and logistic and can be illustrated by the following example : 

A logistic company wants to optmize its shipments. To do so, it has to choose among 
several items, each having their own value and volume, a subset of items fitiing in 
the cargo truck while having the maximal sum of values.

To give a concrete example, *what would be the optimal subset for the following group of items if the maximal capacity of the cargo trick is 15 L?*

| id                | A | B | C | D  | E  | F | G  |
|-------------------|---|---|---|----|----|---|----|
| values (in euros) | 7 | 9 | 5 | 12 | 14 | 6 | 12 |
| volumes (in L)     | 3 | 4 | 2 | 6  | 7  | 3 | 5  |

## First approach 

The first approach I had has been to quantify how profitable each items were. Intuitively, it is easy to say that the item F is more profitable than the item A
as it has more value for the same volume. Therefore, the quantifier I used was the ratio **value/volume** so I sorted the items from the higher ratio to the lowest.

| id            | C   | G   | A   | B    | D | E | F |
|---------------|-----|-----|-----|------|---|---|---|
| ratio   (€/L) | 2.5 | 2.4 | 2.3 | 2.25 | 2 | 2 | 2 |

Once sorted, I only had to add the first volumes until there was no room left for a new vitem's volume in the imaginary cargo.
This is when I noticed a limit of this method or at least for its implementation. Indeed, after summing the volumes of the items C,G,A and B,
I ended up with a __total volume of 14L and a total value of 33 euros__. But if I had swapt the items C and F, I would have ended up with a __total volume of 15L and a 
total value of 34 euros__. 
It was obvious that the algorithm was not capable of giving the optimal solution. 

## Complexity Analysis 
### Greedy algorithm resolution 
This first intuition is indeed close to the greedy algorithm's resolution of this problem which makes locally optimal solution. 
Therefore, it is higly dependent of the volumes' value and if their sum is equal to the cargo truck capacity. 

Moreover, to implement this algorithm, I have to sort the ratio's array in a first time. 
I used to python's built-in function "sorted" of temporal complexity equal to O(nlog(n)), where n is the number of items.
Then in the second part, in the worst case scenario a loop goes over all the items which correspond to a O(n) complexity. 
Therefore, the **temporal complexity of the algorithm is O(nlog(n))**. 
Regarding the spatial complexity, only an array of length n needs to be created in order to keep track of the ratios. 
Thus, the **spatial complexity of the algorithm is O(n)**. 

### Dynamic Programming resolution

## Implementation 

## Conclusion

## Sources 
