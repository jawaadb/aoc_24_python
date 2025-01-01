from helpers import load_text
import numpy as np

# FILE_PATH = "problem_12_example.txt"
FILE_PATH = "problem_12_data.txt"


def load_map(file_path) -> np.ndarray:
    return np.array([list(l.strip()) for l in load_text(file_path)], dtype="S1")


def main():
    grid = load_map(FILE_PATH)
    indices = np.indices(grid.shape)
    nrows, ncols = grid.shape

    def calc_cost(grid: np.ndarray):
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

        def measure(fill_mask: np.ndarray):
            area = np.sum(fill_mask)

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

            return area, perimeter

        parsed = np.zeros(grid.shape, dtype=np.bool_)

        cost = 0
        i = 0
        while ~np.all(parsed):
            i += 1
            print(f"{i}", end="\r")
            start_pos = np.array(
                [indices[0][~parsed][0], indices[1][~parsed][0]], dtype=np.int64
            )
            plant_type = grid[*start_pos]

            plant_area = grid == plant_type
            assert plant_area[*start_pos] == True

            region = np.zeros(grid.shape, dtype=np.bool_)
            flood_fill(start_pos, plant_area, region)

            area, perim = measure(region)
            cost += area * perim

            parsed |= region
        print("")

        return cost

    cost = calc_cost(grid)
    print(f"cost: {cost}")  # Answer: 1375574


main()
