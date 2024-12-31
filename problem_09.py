import numpy as np
from helpers import load_text


# FILE_PATH = "problem_09_example.txt"
FILE_PATH = "problem_09_data.txt"


def main():
    diskmap = load_text(FILE_PATH)[0].strip()

    def unpack_diskmap(diskmap: str) -> np.ndarray:
        diskmap: np.ndarray = np.array([int(n) for n in diskmap], np.int64)
        blockmap = np.full(np.sum(diskmap), -1, np.int64)

        pos, blockid, is_data = 0, 0, False
        for n in diskmap:
            is_data = not is_data
            if is_data:
                blockmap[pos : (pos + n)] = blockid
                blockid += 1
            pos += n

        return blockmap

    blockmap = unpack_diskmap(diskmap)
    indices = np.indices(blockmap.shape)[0]

    def move_file(file_id: int, blockmap: np.ndarray) -> bool:
        file_mask = blockmap == file_id
        file_sz = np.sum(file_mask)

        # find free space start indices
        indices_free = indices[blockmap == -1]
        indices_free_start = indices_free[np.hstack([0, np.diff(indices_free)]) != 1]

        # find free space sizes
        data_diff = np.diff(np.hstack([indices[blockmap != -1], blockmap.size]))
        free_sz = data_diff[data_diff != 1] - 1

        # locate first free space big enough
        free_spaces = np.vstack([indices_free_start, free_sz])

        sufficient_free_spaces = free_spaces[:, free_spaces[1, :] >= file_sz]
        if sufficient_free_spaces.shape[1] == 0:
            return False

        idx_dst = sufficient_free_spaces[0, 0]
        idx_src = indices[file_mask][0]

        if idx_dst >= idx_src:
            return False

        blockmap[idx_dst : idx_dst + file_sz] = blockmap[idx_src : idx_src + file_sz]
        blockmap[idx_src : idx_src + file_sz] = -1

        return True

    def calc_checksum(blockmap: np.ndarray) -> int:
        mask = blockmap != -1
        return np.sum(indices[mask] * blockmap[mask])

    for file_id in range(blockmap.max(), 0, -1):
        print(f"{file_id:6d}", end="\r")
        move_file(file_id, blockmap)
    print("")

    checksum = calc_checksum(blockmap)
    print(f"{checksum=}")  # Answer: 6183632723350


main()
