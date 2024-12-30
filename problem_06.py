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

    return init_world, num_world, guard_position, guard_direction


def main():
    ch_world, world, position, direction = load_map(FILE_PATH)

    nrows, ncols = world.shape

    def advance_position(pos: np.ndarray, dir_in: list[int], world: np.ndarray) -> bool:
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
        if dir == 0:  # up
            i_col_obstacles = np.arange(world.shape[0])[world[:, pos[1]] > 0]
            i_col_obstacles: np.ndarray = i_col_obstacles[i_col_obstacles < pos[0]]
            if i_col_obstacles.size == 0:
                world[0 : pos[0], pos[1]] = -1
                return False
            i_next_obs = i_col_obstacles[-1]
            world[pos[0] : i_next_obs : -1, pos[1]] = -1
            pos[0] = i_next_obs + 1
        elif dir == 2:  # down
            i_col_obstacles = np.arange(world.shape[0])[world[:, pos[1]] > 0]
            i_col_obstacles: np.ndarray = i_col_obstacles[i_col_obstacles > pos[0]]
            if i_col_obstacles.size == 0:
                world[pos[0] :, pos[1]] = -1
                return False
            i_next_obs = i_col_obstacles[0]
            world[pos[0] : i_next_obs, pos[1]] = -1
            pos[0] = i_next_obs - 1
        elif dir == 1:  # right
            i_row_obstacles = np.arange(world.shape[1])[world[pos[0], :] > 0]
            i_row_obstacles: np.ndarray = i_row_obstacles[i_row_obstacles > pos[1]]
            if i_row_obstacles.size == 0:
                world[pos[0] :, pos[1]] = -1
                return False
            i_next_obs = i_row_obstacles[0]
            world[pos[0], pos[1] : i_next_obs] = -1
            pos[1] = i_next_obs - 1
        elif dir == 3:  # left
            i_row_obstacles = np.arange(world.shape[1])[world[pos[0], :] > 0]
            i_row_obstacles: np.ndarray = i_row_obstacles[i_row_obstacles < pos[1]]
            if i_row_obstacles.size == 0:
                world[pos[0], 0 : pos[1]] = -1
                return False
            i_next_obs = i_row_obstacles[-1]
            world[pos[0], pos[1] : i_next_obs : -1] = -1
            pos[1] = i_next_obs + 1
        else:
            assert False

        dir_in[0] = dir
        return True

    def simulate_guard_path(
        init_pos: np.ndarray, init_dir: int, world: np.ndarray
    ) -> str:
        max_iter = 10000
        history_buffer = np.full((max_iter, 3), -1, dtype=np.int64)
        position = init_pos.copy()
        direction = [init_dir]

        for n in range(max_iter + 1):
            if n == max_iter:
                return "max_iter"

            history_buffer[n, 0:2] = position
            history_buffer[n, 2] = direction[0]

            if advance_position(position, direction, world) == False:
                return "out_of_bounds"

            posdir = np.hstack([position, direction[0]], dtype=np.int64)

            history = history_buffer[history_buffer[:, 0] != -1, :]
            if np.any(
                (history[:, 0] == posdir[0])
                & (history[:, 1] == posdir[1])
                & (history[:, 2] == posdir[2]),
            ):
                return "loop"

    init_world = world.copy()
    simulate_guard_path(position, direction, init_world)
    mask_space = init_world == -1

    print(f"{np.sum(mask_space)=}")

    indices = np.indices(ch_world.shape)
    candidate_obstacles = np.vstack(
        [indices[0][mask_space], indices[1][mask_space]]
    ).transpose()

    outcomes: list[str] = []
    for iobs in range(candidate_obstacles.shape[0]):
        print(
            f"{iobs+1}/{candidate_obstacles.shape[0]} ({(iobs+1)/candidate_obstacles.shape[0]:.1%})",
            end="\r",
        )
        candidate_obs = candidate_obstacles[iobs, :]
        this_world = world.copy()
        this_world[candidate_obs[0], candidate_obs[1]] = 1
        result = simulate_guard_path(position, direction, this_world)
        outcomes.append(result)
    print("")

    outcomes = np.array(outcomes)
    for oc in np.unique(outcomes):
        print(f"{oc}: {np.sum(outcomes==oc)}")

    # Answer: 1753 loops


main()
