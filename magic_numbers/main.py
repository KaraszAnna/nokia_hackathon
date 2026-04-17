from pathlib import Path

def next_magic_num(num_str: str) -> str:
        n = len(num_str)
        
        if num_str == '9' * n:
            return '1' + '0' * (n - 1) + '1'

        half_len = (n + 1) // 2
        left_str = num_str[:half_len]
        
        for diff in (0, 1):
            new_left = str(int(left_str) + diff)
            
            if n % 2 == 0:
                poss = new_left + new_left[::-1]
            else:
                poss = new_left + new_left[:-1][::-1]
            
            if len(poss) == n and poss > num_str:
                return poss
            if len(poss) > n:
                return poss
        
        return '1' + '0' * (n - 1) + '1'


def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    for line in data.strip().splitlines():
        line = line.strip()
        if "^" in line:
            base, exp = line.split("^")
            n = int(base) ** int(exp)
        else:
            n = int(line)
            
        print(next_magic_num(str(n)))


if __name__ == "__main__":
    main()
