from helpers import load_text
import numpy as np

FILE_PATH = "problem_12_data.txt"


def load_map(file_path) -> np.ndarray:
    return np.array([list(l.strip()) for l in load_text(file_path)], dtype="S1")


def load_part2_examples() -> np.ndarray:
    fp = "problem_12_example2.txt"

    txt = "".join([l for l in load_text(fp)])
    chunks = txt.split("\n\n")

    examples: list[tuple[int, np.ndarray]] = []
    for chunk in chunks:
        lines = chunk.strip().split("\n")
        answer = int(lines[0])
        grid = np.array([list(l) for l in lines[1:]], "S1")
        examples.append((answer, grid))

    return examples


def main():
    def calc_cost(grid: np.ndarray, print_debug=False):
        if print_debug:
            print("debug")

        indices = np.indices(grid.shape)
        nrows, ncols = grid.shape

        def flood_fill(
            fill_pt: np.ndarray, fill_mask: np.ndarray, res_buff: np.ndarray
        ):
            dirs = np.array(
                [[0, 1], [1, 0], [0, -1], [-1, 0]], dtype=np.int64
            ).transpose()

            # fill point
            res_buff[*fill_pt] = True

            # adjacent points
            adj_pts = dirs.copy()
            adj_pts[0, :] += fill_pt[0]
            adj_pts[1, :] += fill_pt[1]

            # points within bounds
            mask = (
                (adj_pts[0, :] >= 0)
                & (adj_pts[1, :] >= 0)
                & (adj_pts[0, :] < nrows)
                & (adj_pts[1, :] < ncols)
            )
            if ~np.any(mask):
                return
            adj_pts = adj_pts[:, mask]

            # points within canvas and not already filled
            mask = (fill_mask & ~res_buff)[adj_pts[0, :], adj_pts[1, :]]
            if ~np.any(mask):
                return
            adj_pts = adj_pts[:, mask]

            # fill pts
            for ipt in range(adj_pts.shape[1]):
                flood_fill(adj_pts[:, ipt], fill_mask, res_buff)

        def measure_area(fill_mask: np.ndarray):
            return np.sum(fill_mask)

        def measure_perimeter(fill_mask: np.ndarray):
            dirs = np.array(
                [[0, 1], [1, 0], [0, -1], [-1, 0]], dtype=np.int64
            ).transpose()

            perimeter = 0
            pts = np.vstack([indices[0][fill_mask], indices[1][fill_mask]])
            for ipt in range(pts.shape[1]):
                pt = pts[:, ipt]
                adj_pts = dirs.copy()
                adj_pts[0, :] += pt[0]
                adj_pts[1, :] += pt[1]

                mask = (
                    (adj_pts[0, :] >= 0)
                    & (adj_pts[1, :] >= 0)
                    & (adj_pts[0, :] < nrows)
                    & (adj_pts[1, :] < ncols)
                )
                perim_wall = np.sum(~mask)
                adj_pts = adj_pts[:, mask]

                mask = fill_mask[adj_pts[0, :], adj_pts[1, :]]
                perim_fence = np.sum(~mask)

                perimeter += perim_wall + perim_fence

            return perimeter

        def count_sides(fill_mask: np.ndarray):
            pts = np.vstack([indices[0][fill_mask], indices[1][fill_mask]])
            pt_tl = np.array([pts[0, :].min(), pts[1, :].min()], np.int64)
            pt_br = np.array([pts[0, :].max(), pts[1, :].max()], np.int64) + [1, 1]
            sz = pt_br - pt_tl + [2, 2]

            crop = np.zeros(sz, dtype=np.bool)
            img = fill_mask[pt_tl[0] : pt_br[0], pt_tl[1] : pt_br[1]]
            crop[1 : sz[0] - 1, 1 : sz[1] - 1] = img

            def count_verts(arr: np.ndarray) -> int:
                if print_debug:
                    print(np.diff(np.int64(arr), axis=1))

                hdiff_pos = np.int64(np.diff(np.int64(arr), axis=1) == 1)
                hdiff_neg = np.int64(np.diff(np.int64(arr), axis=1) == -1)
                count = 0
                for icol in range(hdiff_pos.shape[1]):
                    count += np.sum(np.diff(np.hstack([0, hdiff_pos[:, icol], 0])) == 1)
                for icol in range(hdiff_neg.shape[1]):
                    count += np.sum(np.diff(np.hstack([0, hdiff_neg[:, icol], 0])) == 1)
                return count

            return count_verts(crop) + count_verts(crop.transpose())

        parsed = np.zeros(grid.shape, dtype=np.bool_)
        cost_A, cost_B = 0, 0
        i = 0
        while ~np.all(parsed):
            i += 1
            start_pos = np.array(
                [indices[0][~parsed][0], indices[1][~parsed][0]], dtype=np.int64
            )
            plant_type = grid[*start_pos]

            plant_area = grid == plant_type
            assert plant_area[*start_pos] == True

            region = np.zeros(grid.shape, dtype=np.bool_)
            flood_fill(start_pos, plant_area, region)

            area, sides, perimeter = (
                measure_area(region),
                count_sides(region),
                measure_perimeter(region),
            )
            if print_debug:
                print(f"A:{area}, S:{sides}")
            sub_cost_A = area * perimeter
            sub_cost_B = area * sides
            cost_A += sub_cost_A
            cost_B += sub_cost_B

            parsed |= region

        return cost_A, cost_B

    # Tests
    all_correct = True
    for iex, (answer, grid) in enumerate(load_part2_examples()):
        print(f"[E.g. {iex}]")
        calculated_answer = calc_cost(grid)[1]
        is_correct = answer == calculated_answer
        print(f"  {answer=}, {'correct' if is_correct else str(calculated_answer)}")
        all_correct &= is_correct
    if not all_correct:
        print("\nFAIL\n")
        return
    else:
        print("")

    # Results
    costA, costB = calc_cost(load_map(FILE_PATH))
    print(f"{costA=}")
    print(f"{costB=}")  # Answer: 830566


main()
