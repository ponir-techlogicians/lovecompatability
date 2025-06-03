# Stroke dictionary for each letter
stroke_dict = {
    'A': 3, 'B': 3, 'C': 1, 'D': 2, 'E': 3, 'F': 2, 'G': 2, 'H': 3,
    'I': 1, 'J': 2, 'K': 3, 'L': 2, 'M': 4, 'N': 3, 'O': 1, 'P': 2,
    'Q': 2, 'R': 3, 'S': 4, 'T': 2, 'U': 3, 'V': 2, 'W': 4, 'X': 2,
    'Y': 3, 'Z': 3
}


def get_strokes_for_word(word: str) -> list:
    """Convert a word into a list of stroke counts for each letter."""
    return [stroke_dict[ch] for ch in word.upper() if ch in stroke_dict]


def interleave_tokens(name1: str, name2: str) -> list:
    """Interleave words from two names, filling missing words with '0'."""
    tokens1 = name1.split()
    tokens2 = name2.split()

    max_len = max(len(tokens1), len(tokens2))
    merged_tokens = []

    for i in range(max_len):
        merged_tokens.append(tokens1[i] if i < len(tokens1) else "0")
        merged_tokens.append(tokens2[i] if i < len(tokens2) else "0")

    return merged_tokens


def adjacency_sum(arr: list) -> list:
    """Reduce the list by summing adjacent numbers until two digits remain."""
    while len(arr) > 2:
        arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
    return arr

def adjacency_sum_steps(arr: list) -> list:
    """Return a list of each step taken during adjacency summing until two digits remain."""
    steps = [arr[:]]  # Store the initial array
    while len(arr) > 2:
        arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
        steps.append(arr[:])
    return steps

def adjacency_sum_steps_fixed(arr: list, total_steps: int = 5) -> list:
    """Return a fixed number of adjacency sum steps (default 5).
    If the result reaches two digits early, repeat the last step."""
    steps = [arr[:]]  # Start with the initial array

    while len(steps) < total_steps:
        if len(arr) <= 2:
            # Repeat the last step if already reduced
            steps.append(arr[:])
        else:
            arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
            steps.append(arr[:])
    return steps


def get_name_compatibility_with_steps(name1: str, name2: str) -> tuple:
    """Calculate compatibility score and return 5 adjacency sum steps."""
    merged_tokens = interleave_tokens(name1, name2)
    stroke_list = [stroke for token in merged_tokens for stroke in get_strokes_for_word(token)]
    steps = adjacency_sum_steps_fixed(stroke_list, total_steps=5)
    final_score = int("".join(map(str, steps[-1])))  # From the last step
    return final_score, steps



def get_name_compatibility(name1: str, name2: str) -> int:
    """Calculate the compatibility score between two names."""
    merged_tokens = interleave_tokens(name1, name2)
    stroke_list = [stroke for token in merged_tokens for stroke in get_strokes_for_word(token)]
    final_two = adjacency_sum(stroke_list)
    return int("".join(map(str, final_two)))


def split_names(name1, name2):
    words1 = name1.split()  # Split name1 into words
    words2 = name2.split()  # Split name2 into words

    merged = []
    max_len = max(len(words1), len(words2))

    # Merge names in an alternating pattern
    for i in range(max_len):
        if i < len(words1):
            merged.append(words1[i])
        if i < len(words2):
            merged.append(words2[i])

    # Ensure the final list has exactly 6 elements, filling with "_"
    while len(merged) < 6:
        merged.append("_")

    return merged[:6]  # Return exactly 6 elements


def get_total_stroke(word: str) -> int:
    """Return the total stroke count for a word."""
    return sum(stroke_dict.get(ch, 0) for ch in word.upper())


def split_names_into_6(name1: str, name2: str) -> list:
    """Split both names and interleave up to 3 parts each to get 6 tokens."""
    parts1 = name1.split()
    parts2 = name2.split()

    merged = []
    for i in range(3):
        if i < len(parts1):
            merged.append(parts1[i])
        else:
            merged.append("_")
        if i < len(parts2):
            merged.append(parts2[i])
        else:
            merged.append("_")
    return merged

def split_names_into_4(name1: str, name2: str) -> list:
    """Split both names and interleave up to 3 parts each to get 6 tokens."""
    parts1 = name1.split()
    parts2 = name2.split()

    merged = []
    for i in range(2):
        if i < len(parts1):
            merged.append(parts1[i])
        else:
            merged.append("_")
        if i < len(parts2):
            merged.append(parts2[i])
        else:
            merged.append("_")
    return merged


def get_number_of_split(name1: str, name2: str) -> int:
    """Return the number of times the names are split into 6 tokens."""
    parts1 = name1.split()
    parts2 = name2.split()
    merged = []
    for i in range(3):
        if i < len(parts1):
            merged.append(parts1[i])
        if i < len(parts2):
            merged.append(parts2[i])

    return merged

def adjacency_sum_steps_fixed_5(arr: list) -> list:
    """Return 5 steps of adjacency summing (even if 2 elements reached early)."""
    steps = [arr[:]]
    while len(steps) < 5:
        if len(arr) <= 2:
            steps.append(arr[:])
        else:
            arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
            steps.append(arr[:])
    return steps

def adjacency_sum_steps_fixed_3(arr: list) -> list:
    """Return 5 steps of adjacency summing (even if 2 elements reached early)."""
    steps = [arr[:]]
    while len(steps) < 3:
        if len(arr) <= 2:
            steps.append(arr[:])
        else:
            arr = [(arr[i] + arr[i + 1]) % 10 for i in range(len(arr) - 1)]
            steps.append(arr[:])
    return steps

def get_name_compatibility_with_5steps(name1: str, name2: str) -> tuple:
    """Get compatibility score with 5 steps starting from 6 tokens."""
    splits = get_number_of_split(name1, name2)
    if len(splits) > 4:
        six_parts = split_names_into_6(name1, name2)
        initial_strokes = [get_total_stroke(word) for word in six_parts]
        steps = adjacency_sum_steps_fixed_5(initial_strokes)
        final_score = int("".join(map(str, steps[-1])))
        return final_score, steps
    else:
        four_parts = split_names_into_4(name1, name2)
        initial_strokes = [get_total_stroke(word) for word in four_parts]
        steps = adjacency_sum_steps_fixed_3(initial_strokes)
        final_score = int("".join(map(str, steps[-1])))
        return final_score, steps
