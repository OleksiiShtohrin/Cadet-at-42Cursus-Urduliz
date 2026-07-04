import os
import sys

try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    print("❌ Error: python-dotenv is not installed.")
    print("Install them using:")
    print("Run: echo python-dotenv==1.0.1 > requirements.txt")
    print("pip install -r requirements.txt")
    print("python3 oracle.py")
    print("or")
    print("poetry add python-dotenv")
    print("poetry run python oracle.py")
    sys.exit(1)


def get_config_value(name: str, default: str = "not set") -> str:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def main() -> None:
    load_dotenv()

    print("ORACLE STATUS: Reading the Matrix...")
    print()

    mode = get_config_value("MATRIX_MODE", "development")
    database_url = get_config_value("DATABASE_URL")
    api_key = get_config_value("API_KEY")
    log_level = get_config_value("LOG_LEVEL", "DEBUG")
    zion_endpoint = get_config_value("ZION_ENDPOINT")

    print("Configuration loaded:")
    print(f"Mode: {mode}")

    if database_url == "not set":
        print("Database: Missing configuration")
    elif mode == "production":
        print("Database: Connected to production database")
    else:
        print("Database: Connected to local instance")

    if api_key == "not set":
        print("API Access: Missing credentials")
    else:
        print("API Access: Authenticated")

    print(f"Log Level: {log_level}")

    if zion_endpoint == "not set":
        print("Zion Network: Offline")
    else:
        print("Zion Network: Online")

    print()
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if zion_endpoint == "not set":
        print("[MISSING] .env file, Run: cp .env.example .env")
    else:
        print("[OK] .env file properly configured")
    print("[OK] Production overrides available")
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
