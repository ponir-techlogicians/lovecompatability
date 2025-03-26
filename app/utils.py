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