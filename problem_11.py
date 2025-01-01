from helpers import load_text


if False:
    FILE_PATH = "problem_11_example.txt"
else:
    FILE_PATH = "problem_11_data.txt"


def main():
    stones = list(map(int, load_text(FILE_PATH)[0].strip().split()))

    def blink():
        idx = 0
        while idx < len(stones):
            if stones[idx] == 0:
                stones[idx] = 1
            elif len(digits := str(stones[idx])) % 2 == 0:
                left = int(digits[0 : len(digits) // 2])
                right = int(digits[len(digits) // 2 :])
                stones[idx] = left
                idx += 1
                stones.insert(idx, right)
            else:
                stones[idx] *= 2024

            idx += 1

    print(f'Init: {" ".join(map(str, stones))}')
    num_blinks = 25
    for i in range(num_blinks):
        print(f"{i+1}/{num_blinks}", end="\r")
        blink()
    print("")

    print(f"{len(stones)} stones after {num_blinks} blinks.")
    # Answer: 217812


main()
