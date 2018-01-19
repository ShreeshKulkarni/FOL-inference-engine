# FOL-inference-engine
Deduces entailment of given queries over a specified Knowledge Base in First-Order-Logic. Applies FOL Resolution with Forward Chaining.


Description
-----------
The program does "Proof by Refutation" to establish the validity of each of the given queries over the given Knowledge Base (KB). That is, for each query, its negation is added to the KB, and the resultant new KB is searched for presence of any contradiction by doing Forward Chaining using First-Order-Logic Resolution. If a contradiction is found, then it can be inferred that the corresponding query is entailed by the KB.


Assumptions
-----------
- The FOL Knowledge Base provided as input contains sentences with the following defined operators:
    NOT X, represented as ~X
    X or Y, represented as X | Y
where X, Y are predicates.
- Variables are all single lowercase letters. 
- All variables are assumed to be universally quantified.
- All predicates (such as Sibling) and constants (such as John) are case-sensitive alphabetical strings that begin with an uppercase letter.
- Each predicate takes at least one argument. Predicates will take at most 100 arguments. A given predicate name will not appear with different number of arguments.
- Each query will be a single literal of the form Predicate(Constant) or ~Predicate(Constant).
- The KB that will be given is consistent. That is, there will be no contradicting rules or facts in the given KB.


Input
-----
The program reads a text file "input.txt" in the current directory. The format is as follows:

<NQ = NUMBER OF QUERIES>
<QUERY 1>
…
<QUERY NQ>
<NS = NUMBER OF SENTENCES IN THE GIVEN KNOWLEDGE BASE>
<SENTENCE 1>
…
<SENTENCE NS>
  
  
Output
------
Solution is written to "output.txt" in the current directory. The format is as follows:

<ANSWER 1>
…
<ANSWER NQ>
  
where each answer is either TRUE if the corresponding query can be proved as true given the
Knowledge Base, or FALSE otherwise.


How to Run?
-----------
Needs Python 2.7 interpreter
> python FOL_inference_engine.py
