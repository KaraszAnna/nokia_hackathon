from pathlib import Path

def next_magic_num(self, num: str) -> str:
        n = len(num)
        
        if all(c == '9' for c in num):
            return str(int(num) + 2)

        half_len = (n + 1) // 2
        left_str = num[:half_len]
        
        possible = []
                
        for diff in [0, 1]:
            new_left = str(int(left_str) + diff)
            
            if n % 2 == 0:
                poss = new_left + new_left[::-1]
            else:
                poss = new_left + new_left[:-1][::-1]
            
            possible.append(poss)
            
        valid = [p for p in possible if int(p) > int(num)]
        return min(valid, key=int)


def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    for line in data.strip().splitlines():
        line = line.strip()
        if "^" in line:
            base, exp = line.split("^")
            n = int(base) ** int(exp)
        else:
            n = int(line)
            
        print(next_magic_num(None, str(n)))


if __name__ == "__main__":
    main()
