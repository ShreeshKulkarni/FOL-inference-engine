import re


def unify_var(var, x, subsList):
    '''Return a substitution between var and x.

    Args:
        var : a variable
        x : a variable, constant, or list (predicate)
        subsList : the substitution built so far
    '''

    # Cascade unification if a substitution already exists
    if subsList.get(var, False):
        return unify(subsList[var], x, subsList)
    elif subsList.get(x, False):
        return unify(var, subsList[x], subsList)

    # else add the new substitution to subsList
    else:
        subsList[var] = x
        return subsList


def unify(x, y, subsList):
    '''Make FOL expressions x and y look identical, if it is possible to do so.

    Args:
        x : a variable, constant, or list (predicate)
        y : a variable, constant, or list (predicate)
        subsList : the unifier / substitution built so far

    Returns:
        The final substitution (Most General Unifier) if one exists, "failure" otherwise.
    '''

    if subsList == "failure":
        return "failure"
    # When x and y are identical
    elif x == y:
        return subsList
    # When x is a variable
    elif isinstance(x, str) and x[0].islower():
        return unify_var(x, y, subsList)
    # When y is a variable
    elif isinstance(y, str) and y[0].islower():
        return unify_var(y, x, subsList)
    # When x and y are predicates, recurse over the corresponding arguments
    elif isinstance(x, list) and isinstance(y, list):
        return unify(x[1:], y[1:], unify(x[0], y[0], subsList))
    else:
        return "failure"


def forward_chain(que):
    '''Perform FOL Resolution (Proof by Refutation) using Forward Chaining.

    Args:
        que : a list [symbol, name, arg1, arg2, ..] - single-clause-sentence passed as query

    Returns:
        True if there is a contradiction in the KB, False otherwise.
    '''

    global working_unit_KB, working_poly_KB

    # Check for contradiction in working_unit_KB
    for unit in working_unit_KB:
        # Primary check - predicate name should be same, symbol should be different and number of args should be same
        if unit[1] == que[1] and unit[0] != que[0] and len(unit) == len(que):
            # Try to unify corresponding args of the query and unit clause
            subsList = unify(que[2:], unit[2:], {})

            # If cannot unify, try next unit clause
            if subsList == "failure":
                continue

            # Unification happened either var-var - {x/a, y/b} or var-const - {x/Art, y/Jon} or args were same - {}
            # This means contradiction is found
            return True

    # Check for contradiction in working_poly_KB
    for sent in working_poly_KB:
        # Resolve each predicate p with the query
        for p in range(len(sent)):
            if que[1] == sent[p][1] and que[0] != sent[p][0] and len(que) == len(sent[p]):
                # Perform unification as above
                subsList = unify(que[2:], sent[p][2:], {})
                if subsList == "failure":
                    continue

                if len(sent) == 1:
                    # Contradiction because sentences unified have only 1 clause each ex: ~A(John) and A(x)
                    return True

                # If subsList is empty - no substitution needed.
                # Resolution step: Compute the remainder of clauses in sent, excluding the unified clause
                if not subsList:
                    remainder = []
                    for pi in range(len(sent)):
                        # Exclude the unified clause
                        if pi != p:
                            temp = [e for e in sent[pi]]
                            remainder.append(temp)

                # SubsList exists
                else:
                    remainder = []

                    # Do substitution in the sentence unified with - then compute the remainder
                    for pi in range(len(sent)):
                        # Exclude the unified clause
                        if pi != p:
                            temp = [e for e in sent[pi]]
                            for arg in range(2, len(sent[pi])):
                                if subsList.get(sent[pi][arg], False):
                                    temp[arg] = subsList[sent[pi][arg]]
                            remainder.append(temp)

                # Add the remainder to KB
                if len(remainder) == 1:
                    existing = False
                    for unit in working_unit_KB:
                        # Check repetition
                        if unit == remainder[0]:
                            existing = True

                        # Optimization: check contradiction in working_unit_KB against single-clause-remainder
                        if unit[1] == remainder[0][1] and unit[0] != remainder[0][0] and len(unit) == len(remainder[0]):
                            if unit[2:] == remainder[0][2:]:
                                return True

                    if not existing:
                        working_unit_KB.append(remainder[0])

                else:
                    for existing_sent in working_poly_KB:
                        if existing_sent == remainder:
                            break
                    else:
                        working_poly_KB.append(remainder)

    # Tried all sentences in KB - no unification (= No contradiction)
    return False

# To hold working copy of the processed Knowledge Base
working_unit_KB = []
working_poly_KB = []

if __name__ == '__main__':
    unit_KB_FC = []         # To hold single clause sentences in the FOL Knowledge Base (KB)
    poly_KB_FC = []         # To hold multiple clause sentences in the KB
    queries = []            # To hold NQ number of queries
    result = []             # To hold NQ number of results to queries - "TRUE" / "FALSE"

    with open('input.txt', 'r') as f:
        NQ = int(f.readline().strip())
        for _ in range(NQ):
            line = f.readline().strip()
            # Extract name of query function
            name = re.search('^.*(?=\()', line)
            name = name.group().strip()

            # Extract the arguments
            match = re.search('(?<=\().*(?=\))', line)
            args = match.group().split(',')

            # Store each query in the format: [symbol, name, arg1, arg2, ..]
            if name[0] == '~':
                queries.append(['~'] + [name[1:]] + [arg.strip() for arg in args])
            else:
                queries.append(['+'] + [name] + [arg.strip() for arg in args])

        NS = int(f.readline().strip())               # number of sentences in the KB
        for _ in range(NS):
            # List of predicates in the sentence
            preds = f.readline().strip().split('|')

            # Preprocess and store predicates in each sentence in the format [symbol, name, arg1, arg2, ..] as above
            temp = []            # temp list to hold processed clauses in each sentence
            for pred_i in preds:
                pred_i = pred_i.strip()
                name = re.search('^.*(?=\()', pred_i)
                name = name.group().strip()
                match = re.search('(?<=\().*(?=\))', pred_i)
                args = match.group().split(',')

                if name[0] == '~':
                    pred_i = ['~'] + [name[1:].strip()] + [arg.strip() for arg in args]
                else:
                    pred_i = ['+'] + [name.strip()] + [arg.strip() for arg in args]

                temp.append(pred_i)

            # Classify sentences as sentences with single clause and multiple clauses
            if len(temp) == 1:
                unit_KB_FC.append(temp[0])
            else:
                poly_KB_FC.append(temp)

    global working_unit_KB, working_poly_KB
    for query in queries:
        # Negate the query
        if query[0] == '~':
            query[0] = '+'
        else:
            query[0] = '~'

        # Make fresh copy of KB for each new query
        working_unit_KB = [x for x in unit_KB_FC]
        working_poly_KB = [x for x in poly_KB_FC]

        # Add the negated query to KB
        working_unit_KB = [query] + working_unit_KB

        # Perform Forward Chaining with each unit clause sentence against all sentences in working_poly_KB
        for unit in working_unit_KB:
            if forward_chain(unit):
                # contradiction found - query can be inferred from given KB
                result.append('TRUE')
                break
        else:
            result.append('FALSE')

    # Write out the output
    with open("output.txt", 'w') as f:
        for truth in result:
            f.write(truth + '\n')
