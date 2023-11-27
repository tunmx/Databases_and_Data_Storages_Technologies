# Practice.Functional dependences. X+. Key.

Check if DG is a key for 

R(A,B,D,E,G) and  F={D→G, G→ AB, D→ED, A→B}.

## Analysis

1. **Start with DG**: The initial set: **{D,G}**;
2. **Apply D->G**: G is already in the set, this dependency does not change the set: **{D,G}**;
3. **Apply G->AB**: Adding A and B to the set: **{D,G,A,B}**;
4. **Apply D->ED**: Adding E to the set: **{D,G,A,B,E}**;
5. **Apply A->B**: A and B is already in the set, this dependency does not change the set: **{D,G,A,B,E}**;
6. **Check the Closure**: If the closure set **{D,G,A,B,E}** includes all attributes **{A,B,D,E,G}**, then **DG** is a key.

Following these steps shows that DG’s closure includes all attributes, so DG is a key for relation R.

