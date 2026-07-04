import importlib


def check_dependency(package_name: str) -> tuple[bool, str]:
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, "__version__", "unknown")
        return True, str(version)
    except ImportError:
        return False, ""


def main() -> None:
    print("\nLOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")

    pandas_ok, pandas_version = check_dependency("pandas")
    numpy_ok, numpy_version = check_dependency("numpy")
    matplotlib_ok, matplotlib_version = check_dependency("matplotlib")
    # requests_ok, requests_version = check_dependency("requests")

    if pandas_ok:
        print(f"[OK] pandas ({pandas_version}) - Data manipulation ready")
    else:
        print("[MISSING] pandas - install with pip or Poetry")

    if numpy_ok:
        print(f"[OK] numpy ({numpy_version}) - Numerical computation ready")
    else:
        print("[MISSING] numpy - install with pip or Poetry")
    """
    if requests_ok:
        print(f"[OK] requests ({requests_version}) - Network access ready")
    else:
        print("[MISSING] requests - optional, only needed for APIs")
    """
    if matplotlib_ok:
        print(f"[OK] matplotlib ({matplotlib_version}) - Visualization ready")
    else:
        print("[MISSING] matplotlib - install with pip or Poetry")

    print()

    if not (pandas_ok and numpy_ok and matplotlib_ok):
        print("Missing dependencies detected.")
        print("Install them using:")
        print("pip install -r requirements.txt")
        print("python3 loading.py")
        print("or")
        print("poetry install --no-root")
        print("poetry run python loading.py")
        return

    import numpy as np  # type: ignore
    import pandas as pd  # type: ignore
    import matplotlib.pyplot as plt  # type: ignore

    print("Analyzing Matrix data...")
    data = np.random.randint(0, 100, size=1000)
    print("Processing 1000 data points...")

    df = pd.DataFrame({"matrix_values": data})
    summary = df["matrix_values"].describe()
    print("Summary statistics:")
    print(summary)

    print("Generating visualization...")
    plt.figure(figsize=(8, 4))
    plt.hist(df["matrix_values"], bins=20, color="green", alpha=0.7)
    plt.title("Matrix Data Distribution")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("matrix_analysis.png")

    print()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")
    """print()
    print("Installed package versions:")
    print(f"pandas: {pandas_version}")
    print(f"numpy: {numpy_version}")
    print(f"matplotlib: {matplotlib_version}")
    if requests_ok:
        print(f"requests: {requests_version}")
    print()"""


if __name__ == "__main__":
    main()
