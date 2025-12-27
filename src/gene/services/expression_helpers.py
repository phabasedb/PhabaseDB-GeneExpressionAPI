# Function to safely convert a value to float, returning 0.0 on failure
def safe_float(value) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
