def get_permutations(sequence):
    if len(sequence) <= 1:
        return [sequence]
    first = sequence[0]
    rest_perms = get_permutations(sequence[1:])
    result = []
    for perm in rest_perms:
        for i in range(len(perm) + 1):
            result.append(perm[:i] + first + perm[i:])
    return result
