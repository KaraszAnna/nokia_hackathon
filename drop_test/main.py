from pathlib import Path

def min_num_of_drops(devs, max_height):
    reach = [0] * (devs + 1)
    tries = 0
    
    while reach[devs] < max_height:
        tries += 1
        for i in range(devs, 0, -1):
            reach[i] = reach[i] + reach[i-1] + 1
            
    return tries

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    print(data, end="")


if __name__ == "__main__":
    main()
