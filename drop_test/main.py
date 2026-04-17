from pathlib import Path

def min_num_of_drops(devs, max_height):
    if devs == 0 or max_height == 0:
        return 0

    min_tries, max_tries = 1, max_height

    while min_tries < max_tries:
        guess = (min_tries + max_tries) // 2
        covered = 0
        binomial = 1
        for k in range(1, devs + 1):
            binomial = binomial * (guess - k + 1) // k
            covered += binomial
            if covered >= max_height:
                break
        if covered >= max_height:
            max_tries = guess
        else:
            min_tries = guess + 1

    return min_tries

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    for line in data.strip().splitlines():
        devs, height = line.split(",")
        print(min_num_of_drops(int(devs.strip()), int(height.strip())))


if __name__ == "__main__":
    main()
