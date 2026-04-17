from pathlib import Path
import json
import re
import sys

ADAPTER_SPLIT = re.compile(r'\n(?=[a-zA-Z])')
IPV4_CLEANUP = re.compile(r'\(.*?\)')

FIELD_MAP = {
    "description": "description",
    "physical address": "physical_address",
    "dhcp enabled": "dhcp_enabled",
    "ipv4 address": "ipv4_address",
    "subnet mask": "subnet_mask",
    "default gateway": "default_gateway",
    "dns servers": "dns_servers",
}


def parse_ipconfig_file(file_path):
    with open(file_path, 'r', encoding='utf-16') as f:
        content = f.read()

    adapter_sections = ADAPTER_SPLIT.split(content)

    parsed_adapters = []

    for section in adapter_sections:
        if "adapter" not in section.lower():
            continue

        lines = section.strip().split('\n')
        adapter = {
            "adapter_name": lines[0].strip(':'),
            "description": "",
            "physical_address": "",
            "dhcp_enabled": "",
            "ipv4_address": "",
            "subnet_mask": "",
            "default_gateway": "",
            "dns_servers": []
        }

        prev_field = ""
        for line in lines[1:]:
            if ". ." not in line:
                stripped = line.strip()
                if not stripped:
                    continue
                if prev_field == "dns_servers":
                    adapter["dns_servers"].append(stripped)
                elif prev_field == "default_gateway":
                    adapter["default_gateway"] += ", " + stripped
                continue

            raw_key, raw_value = line.split(":", 1)
            normalized_key = raw_key.strip().replace(".", "").lower()
            value = raw_value.strip()

            matched_field = ""
            for keyword, field_name in FIELD_MAP.items():
                if keyword in normalized_key:
                    matched_field = field_name
                    break

            if not matched_field:
                continue

            prev_field = matched_field

            if matched_field == "dns_servers":
                if value:
                    adapter["dns_servers"].append(value)
            elif matched_field == "ipv4_address":
                adapter["ipv4_address"] = IPV4_CLEANUP.sub('', value).strip()
            else:
                adapter[matched_field] = value

        parsed_adapters.append(adapter)

    return parsed_adapters


def main():
    input_files = sorted(Path(".").glob("parser_input*.txt"))
    all_results = []

    for file_path in input_files:
        adapters = parse_ipconfig_file(str(file_path))
        all_results.append({
            "file_name": file_path.name,
            "adapters": adapters
        })

    sys.stdout.write(json.dumps(all_results, indent=2, ensure_ascii=False))
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()