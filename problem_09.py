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
    sz_free = np.sum(blockmap == -1)
    indices = np.indices(blockmap.shape)[0]

    def has_gaps(blockmap: np.ndarray) -> bool:
        return np.any(blockmap[-sz_free:] != -1)

    def defrag(blockmap: np.ndarray):
        idx_dst = indices[blockmap == -1][0]
        idx_src = indices[blockmap != -1][-1]
        blockmap[idx_dst], blockmap[idx_src] = blockmap[idx_src], blockmap[idx_dst]

    def calc_checksum(blockmap: np.ndarray) -> int:
        mask = blockmap != -1
        return np.sum(indices[mask] * blockmap[mask])

    def disp(blockmap: np.ndarray):
        print("".join([str(i) if i != -1 else "." for i in blockmap]))

    while has_gaps(blockmap):
        defrag(blockmap)

    checksum = calc_checksum(blockmap)
    print(f"{checksum=}")  # Answer: 6154342787400


main()
