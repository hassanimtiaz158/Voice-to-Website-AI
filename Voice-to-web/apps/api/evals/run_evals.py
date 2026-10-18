import json
from pathlib import Path


def main():
    cases = json.loads((Path(__file__).parent / "datasets" / "example.json").read_text())
    print(f"loaded {len(cases)} eval cases. TODO: run graph per case and score.")


if __name__ == "__main__":
    main()
