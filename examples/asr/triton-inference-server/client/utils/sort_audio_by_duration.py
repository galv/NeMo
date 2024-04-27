import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(description="sort audio manifest by duration")
    parser.add_argument(
        "--manifest",
        type=str,
        required=True,
        help="manifest file",
    )
    parser.add_argument(
        "--output_manifest",
        type=str,
        required=True,
        help="output manifest file",
    )
    parser.add_argument(
        "--descending",
        action="store_true",
        required=False,
        default=False,
        help="sort by descending order",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    duration_lines = []
    total_duration = 0
    with open(args.manifest, "r") as f:
        for line in f:
            item = json.loads(line.strip())
            duration = float(item["duration"])
            duration_lines.append((duration, line))  
            total_duration += duration          
    print(f"Total duration: {total_duration:.2f} seconds")
    lines = sorted(duration_lines, key=lambda x: x[0], reverse=args.descending)
    with open(args.output_manifest, "w") as f:
        for line in lines:
            f.write(line[1])


if __name__ == "__main__":
    main()
    