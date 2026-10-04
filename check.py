import pandas as pd

files = [
    "datasets/temperature.csv",
    "datasets/air_quality.csv"
]

for file in files:

    print("\n" + "="*80)
    print(file)

    # Show first 200 raw bytes
    with open(file, "rb") as f:
        raw = f.read(200)

    print(raw)