def heaps_permutations(activities):
    """
    Generates all permutations of the activities by using iterative version of B.R. Heap's algorithm
    """
    permutations = [activities.copy()]
    c = [0] * len(activities)

    i = 0
    while i < len(activities):
        if c[i] < i:
            if not (i & 1):  # checks if i is even
                activities = swap(activities, 0, i)
            else:
                activities = swap(activities, c[i], i)

            c[i] += 1
            i = 1

            permutations.append(activities.copy())
        else:
            c[i] = 0
            i += 1

    permutations.sort()
    return permutations


def swap(activities, i, j):
    tmp = activities[j]
    activities[j] = activities[i]
    activities[i] = tmp

    return activities


if __name__ == "__main__":
    arr = [1, 2, 3]
    res = heaps_permutations(arr)
    print(res)
    # permutations.sort()
