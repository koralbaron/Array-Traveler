# Array-Traveler
The program gets a file path from the user which contains one or more arrays, and prints to the screen a table whether reaching the last element for each array is possible, according to a set of rules.

# Rulse
1. The first index is 0, that’s where the algorithm starts.
2. Algorithm may only ‘jump’ forward or backwards in the array according to the value in the ‘current’ element (e.g. if the value at index 0 is 3 the algo may only advance to index 3. if the value at index 3 is 2 – the algo may advance to both index 5 and index 1).

## Examples
* **[4, 4, 1, 1, 2, 2, 1000, 1]** will return TRUE,
since there is a route from the first element to the last element which goes: 0 (4) → 4 (2) → 2 (1) → 1 (4) → 5 (2) → 7] .

* **[4, 2, 1, 3, 2, 2, 1000, 1]** will return FALSE,

since there is no route from the first element to the last element.

# User Attantion!    
* **The file should only be of the folowing formats : CSV, TSV, JSON.**
* **The file should only contain a single array Or a list of arrays of unsigned integers.**

