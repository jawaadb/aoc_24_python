import numpy as np
from helpers import load_text

# FILE_PATH = "problem_04_example.txt"
FILE_PATH = "problem_04_data.txt"

WORD_TO_FIND = "XMAS"


def main():
    word_to_find = np.array([letter for letter in WORD_TO_FIND], dtype="S1")
    word_len = word_to_find.size

    ch_array: np.ndarray = np.array(
        [[letter for letter in line.strip()] for line in load_text(FILE_PATH)],
        dtype="S1",
    )

    rel_indices_horz = np.vstack(
        [np.zeros((1, word_len), dtype=np.int64), np.arange(word_len).reshape(1, -1)]
    )

    rel_indices_diag = np.vstack([np.arange(word_len), np.arange(word_len)])

    def generate_rotations(rel_indices: np.ndarray) -> list[np.ndarray]:
        assert rel_indices.shape[0] == 2
        rot_matrix = np.array([[0, -1], [1, 0]], dtype=rel_indices.dtype)
        r1 = rel_indices.copy()
        r2 = rot_matrix @ r1
        r3 = rot_matrix @ r2
        r4 = rot_matrix @ r3
        return [r1, r2, r3, r4]

    rel_indices_list = generate_rotations(rel_indices_horz) + generate_rotations(
        rel_indices_diag
    )

    for ri in rel_indices_list:
        assert ri.dtype == rel_indices_list[0].dtype

    def check_word(coords: np.ndarray, rel_idx: np.ndarray) -> np.ndarray | None:
        assert coords.size == 2 and isinstance(coords, np.ndarray)
        assert rel_idx.shape[0] == 2 and isinstance(rel_idx, np.ndarray)
        coords = (
            coords.reshape(-1, 1) @ np.ones((1, rel_idx.shape[1]), dtype=coords.dtype)
            + rel_idx
        )

        # No match if out of bounds
        if np.any(coords.min(axis=1) < 0):
            return False
        if np.any(coords.max(axis=1) >= ch_array.shape):
            return False

        return np.all(
            np.array(
                [
                    ch_array[coords[0, idx], coords[1, idx]]
                    for idx in range(coords.shape[1])
                ]
            )
            == word_to_find
        )

    # locate all first letters
    first_letter_indices = np.arange(ch_array.size).reshape(ch_array.shape[0], -1)[
        ch_array == word_to_find[0]
    ]
    first_letter_coords = np.vstack(
        [
            first_letter_indices // ch_array.shape[0],
            first_letter_indices % ch_array.shape[1],
        ]
    )

    found_count = 0
    for candidate_idx in range(first_letter_coords.shape[1]):
        coord = first_letter_coords[:, candidate_idx]
        for ri in rel_indices_list:
            found = check_word(coord, ri)
            if found:
                found_count += 1

    print(f"{found_count=}")  # Answer: 2530


main()
