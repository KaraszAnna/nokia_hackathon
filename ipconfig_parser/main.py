from pathlib import Path

import json
import re

ADAPTER_SPLIT_PATTERN = re.compile(r'\n(?=[a-zA-Z])')

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
    with open(file_path, 'r', encoding='cp850') as f:
        content = f.read()

    adapter_sections = ADAPTER_SPLIT_PATTERN.split(content)

    parsed_adapters = []

    for section in adapter_sections:
        section_lower = section.lower()
        if "adapter" not in section_lower:
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
            if ":" not in line:
                if prev_field == "dns_servers" and line.strip():
                    adapter["dns_servers"].append(line.strip())
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
                adapter["ipv4_address"] = value.replace("(Preferred)", "").strip()
            else:
                adapter[matched_field] = value

        parsed_adapters.append(adapter)

    return parsed_adapters


def main():
    input_files = sorted(Path(".").glob("*.txt"))

    for file_path in input_files:
        adapters = parse_ipconfig_file(str(file_path))
        print(json.dumps({"file_name": file_path.name, "adapters": adapters}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()