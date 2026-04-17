from pathlib import Path
from datetime import datetime
import math


def calc_fee_per_hour(total_minutes):
    if total_minutes <= 0:
        return 0

    full_days = total_minutes // 1440
    remaining = total_minutes % 1440

    fee = full_days * 10000

    if remaining <= 30:
        return fee

    billable = remaining - 30
    day_fee = 0

    if billable <= 180:
        day_fee = math.ceil(billable / 60) * 300
    else:
        day_fee = 3 * 300 + math.ceil((billable - 180) / 60) * 500

    fee += min(day_fee, 10000)

    return fee


def calc_fee_per_minute(total_minutes):
    if total_minutes <= 0:
        return 0

    full_days = total_minutes // 1440
    remaining = total_minutes % 1440

    fee = full_days * 10000.0

    if remaining <= 30:
        return int(fee)

    billable = remaining - 30
    day_fee = 0.0

    if billable <= 180:
        day_fee = billable * 5
    else:
        day_fee = 180 * 5 + (billable - 180) * (500 / 60)

    fee += min(day_fee, 10000)

    return round(fee)


def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    lines = data.strip().splitlines()

    results = []
    for line in lines[2:]:
        parts = [p.strip() for p in line.split('\t') if p.strip()]
        if len(parts) < 3:
            continue

        plate = parts[0]

        try:
            entry = datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S")
            exit_time = datetime.strptime(parts[2], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            results.append(f"{plate}\tHibás dátumformátum")
            continue

        total_minutes = math.ceil((exit_time - entry).total_seconds() / 60)

        if total_minutes < 0:
            results.append(f"{plate}\tHibás: kilépés korábbi, mint belépés")
            continue

        hourly = calc_fee_per_hour(total_minutes)
        per_min = calc_fee_per_minute(total_minutes)

        results.append(f"{plate}\t{hourly} Ft\t{per_min} Ft")

    output = "\n".join(results)
    print(output)
    Path("output.txt").write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
