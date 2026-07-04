import os
import sys
import site


def is_virtual_environment() -> bool:
    return sys.prefix != sys.base_prefix


def get_python_path() -> str:
    return sys.executable


def get_environment_name() -> str:
    if not is_virtual_environment():
        return "None detected"

    return os.path.basename(sys.prefix)


def get_environment_path() -> str:
    return sys.prefix


def get_package_path() -> str:
    paths = site.getsitepackages()
    if paths:
        return paths[0]
    return site.getusersitepackages()


def get_short_python_path() -> str:
    full_path = sys.executable  # /opt/pyenv/versions/3.13.1/bin/python3
    parts = full_path.split(os.sep)

    if len(parts) > 3:
        return f"{parts[1]}/{parts[-2]}/{parts[-1]}"
    return full_path


def print_outside_matrix() -> None:
    print()
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {get_short_python_path()}")
    print(f"Virtual Environment: {get_environment_name()}")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows")
    print()
    print("Then run this program again.")


def print_inside_matrix() -> None:
    print()
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {get_python_path()}")
    print(f"Virtual Environment: {get_environment_name()}")
    print(f"Environment Path: {get_environment_path()}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(get_package_path())


def main() -> None:
    if is_virtual_environment():
        print_inside_matrix()
    else:
        print_outside_matrix()


if __name__ == "__main__":
    main()
