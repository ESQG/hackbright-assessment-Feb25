def string_compare(s1, s2):
    """Given two strings, figure out if they are exactly the same (without using ==).

    Put runtime here:
    -----------------
    [   O(n)            ]

    Checking the length of each string is O(1) in Python, because apparently the length
    is cached as an attribute.  In a non language-specific context, I would call it O(n) 
    to find the length of a string.  Either way though, to ensure that two strings of the
    same length are not the same, we iterate through them together, which costs O(n) runtime.

    """

    if len(s1) != len(s2):
        return False

    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False

    return True


def has_exotic_animals(animals):
    """Determine whether a list of animals contains exotic animals.

    Put runtime here:
    -----------------
    [  O(n) assuming list, not set ]

    Platpypus???  Not platypus?  I suppose that's more exotic.

    This function would have an O(1) runtime if given animals as a set
    (or equivalently a dictionary, when checking for keys).  However in
    the given case, when animals is a list, the "in" statement must be checked
    by iterating through the list once, making it an O(n) runtime cost.

    """

    if "hippo" in animals or "platpypus" in animals:
        return True
    else:
        return False


def sum_zero_1(numbers):
    """Find pairs of integers that sum to zero.

    Put runtime here:
    -----------------
    [        O(n)     ]

    As in the hint, to make a set from an iterable, the runtime is O(n),
    because I believe the algorithm iterates through and adds each non-redundant
    element to the hash table (if it checks redundancy that's set lookup, which is O(1)).

    The for loop iterates through the new set s, an O(n) operation.  During each step,
    the lookup in s has O(1) cost, as does appending [-x, x] to the list result.  Thus
    the overal cost is still O(n * constant) = O(n).
    """

    result = []

    # Hint: the following line, "s = set(numbers)", is O(n) ---
    # we'll learn exactly why later
    s = set(numbers)

    for x in s:
        if -x in s:
            result.append([-x, x])

    return result


def sum_zero_2(numbers):
    """Find pairs of integers that sum to zero.

    Put runtime here:
    -----------------
    [ O(n**2): quadratic ]

    Whether numbers is a list or any other iterable (including a set),
    the algorithm loops through it to look at x, and for each x,
    loops through numbers again to look at y.  This nested for loop,
    which compares every pair (x, y) in the product of numbers with itself
    (as in Cartesian product),
    imposes a cost of O(n^2).  The conditional if x == -y and appending (x, y)
    both cost O(1), so the total runtime cost is quadratic.

    """

    result = []

    for x in numbers:
        for y in numbers:
            if x == -y:
                result.append((x, y))
    return result


def sum_zero_3(numbers):
    """Find pairs of integers that sum to zero.

    This version gets rid of duplicates (it won't add (1, -1) if (-1, 1) already there.

    Put runtime here:
    -----------------
    [  O(n**4) , quartic at worst-- but generic case cubic ]

    Here we have a nested for loop as above, with a quadratic runtime cost, but in each step
    of the inner for loop, we have a list lookup in result.  To determine the full runtime, we
    need to check if the length of result is constant, proportional to that of numbers, or larger.

    This is trickier than it might seem, because the algorithm below does not get rid of duplicates.
    It does not check if (x, y) is already in result, only if (y, x) is.  Thus, using n to mean
    the length of numbers, we must consider how the length of results grows.  In the event that
    every single pair (x, y) were appended to the list, the length of results would grow quadratically
    in numbers, so the lookup "(y, x) not in result" has O(n**2) cost where n is the length of numbers.

    Indeed I was able to construct a scenario where the length of the results list is 1/4 n**2.
    For example, if the list is [1]*k + [-1]* k, so n = 2k, then len(results) = k**2.  Thus we have
    a quartic runtime.

    After emailing Henry about this, he says I should consider a generic list instead of the example above.
    I am still concerned that the presence of duplicates could make results grow quadratically; however,
    in most cases this will not come up, in particular, if a and -a appear in a long list, and a appears
    again after -a, then both pairs (a, -a) and (-a, a) will be added during the first outer iteration.
    And many pairs of numbers in a generic case won't add to results at all; so by claiming that on average
    results grows linearly in n, we get a cubic runtime.  But I think this is inexact, so I'm leaving my 
    quartic claim above.

    Henry also said that for the future, the algorithm will also check if (x, y) not in results.
    In that case, the length of results grows linearly in n, including as the algorithm runs, because each 
    element of numbers can be added to a pair in results at most once.  The two lookups (x, y) not in results
    and (y, x) not in results will then both be O(n).  Therefore the total runtime is cubic: O(n**3).



    """

    result = []

    for x in numbers:
        for y in numbers:
            if x == -y and (y, x) not in result:
                result.append((x, y))
    return result


def test_runtime_3(lengths):
    """Takes a list of lengths, and runs sum_zero_3 on a contrived bad-case example.
    Each example is length twice the entry on the list of lengths.

    Unfortunately this runs VERY slowly.  I tried it where lengths = [10, 20, 40, 80, 160, 320].
    I wish I had left off the 320.

    My results, which I forgot to store but then copied to a variable times, were:

    {10: 0.0004220008850097656,
    20: 0.004470109939575195,
    40: 0.06383395195007324,
    80: 0.8547639846801758,
    160: 13.675019979476929,
    320: 279.8374078273773}

    times[20]/times[10] = 10.59
    times[40]/times[20] = 14.28
    times[80]/times[40] = 13.39
    times[160]/times[80] = 16.00
    times[320]/times[160] = 20.46

    I'm satisfied with my proof-by-worst-example above but I ran these just to see.
    """

    import time
    results = {}
    for k in lengths:
        numbers = [1]*k + [-1]*k

        start = time.time()
        r = sum_zero_3(numbers)
        end = time.time()

        results[k] = end - start

    return results