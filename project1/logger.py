#!/usr/bin/env python3
import sys
from datetime import datetime

def main():
    if len(sys.argv) != 2:
        print("Usage: python logger.py <logfile>")
        sys.exit(1)
    log_filename = sys.argv[1]
    
    try:
        log_file = open(log_filename, "a")
    except Exception as e:
        print(f"Error opening log file: {e}")
        sys.exit(1)
    
    try:
        for line in sys.stdin:
            line = line.rstrip("\n")
            if line.strip() == "QUIT":
                break
            if not line.strip():
                continue
            # The first sequence of non-whitespace characters is the action.
            parts = line.split(maxsplit=1)
            action = parts[0]
            message = parts[1] if len(parts) > 1 else ""
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            log_line = f"{timestamp} [{action}] {message}\n"
            log_file.write(log_line)
            log_file.flush()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        log_file.close()

if __name__ == "__main__":
    main()
