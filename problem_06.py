import numpy as np
from helpers import load_text


# FILE_PATH = "problem_06_example.txt"
FILE_PATH = "problem_06_data.txt"


def load_map(file_path: str) -> tuple[np.ndarray, np.ndarray, int]:
    init_world = np.array(
        [[ch for ch in line.strip()] for line in load_text(file_path)], "S1"
    )
    assert np.all(np.unique(init_world) == np.array("# . ^".split(), "S1"))

    num_world = np.zeros(init_world.shape, dtype=np.int64)
    num_world[init_world == b"#"] = 1

    guard_mask = np.zeros(init_world.shape, dtype=np.bool_)
    guard_chars = [b"^", b">", b"v", b"<"]
    for guard_char in guard_chars:
        guard_mask |= init_world == guard_char

    assert np.sum(guard_mask) == 1
    guard_direction = guard_chars.index(init_world[guard_mask])
    indices = np.indices(init_world.shape)
    guard_position = np.array(
        [indices[0][guard_mask][0], indices[1][guard_mask][0]], np.int64
    )

    return num_world, guard_position, guard_direction


def main():
    world, position, direction = load_map(FILE_PATH)

    nrows, ncols = world.shape

    def advance_position(pos: np.ndarray, dir_in: list[int]) -> bool:
        assert isinstance(dir_in, list)
        assert len(dir_in) == 1
        dir = dir_in[0]
        assert pos.size == 2

        def position_ahead(pos, dir):
            assert dir < 4
            deltas = np.array([[-1, 0], [0, 1], [1, 0], [0, -1]], dtype=np.int64)
            pos_ahead = pos + deltas[dir, :]

            # If position ahead is out-of-bounds, return None
            if np.any(pos_ahead < 0) | np.any(pos_ahead >= [nrows, ncols]):
                return None

            return pos_ahead

        # Mark current position
        world[pos[0], pos[1]] = -1

        # Check ahead
        for num_iter in range(5):
            assert num_iter != 4, "Surrounded by obstacles"

            # While obstacle ahead, turn
            if (pos_ahead := position_ahead(pos, dir)) is None:
                return False  # Out-of-bounds ahead

            # Turn if obstacle ahead
            obstacle_ahead = world[pos_ahead[0], pos_ahead[1]] > 0
            if obstacle_ahead:
                dir = (dir + 1) % 4
            else:
                break

        # Step forwards
        pos[:] = pos_ahead[:]
        dir_in[0] = dir
        return True

    max_iter = 10000
    direction = [direction]
    for n in range(max_iter + 1):
        assert n != max_iter
        if advance_position(position, direction) == False:
            break

    num_positions_visited = np.sum(-world[world < 0])
    print(f"{num_positions_visited=}")  # Answer: 5239


main()
