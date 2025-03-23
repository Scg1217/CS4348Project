#!/usr/bin/env python3
import sys
from datetime import datetime

def main():
    # Ensure the log file name is provided as a command-line argument.
    if len(sys.argv) != 2:
        print("Usage: python logger.py <logfile>")
        sys.exit(1)
    log_filename = sys.argv[1]
    
    # Attempt to open the log file in append mode.
    try:
        log_file = open(log_filename, "a")
    except Exception as e:
        print(f"Error opening log file: {e}")
        sys.exit(1)
    
    try:
        # Read from standard input line by line.
        for line in sys.stdin:

            # Remove the trailing newline character.
            line = line.rstrip("\n")

            # If the line is "QUIT", break out of the loop and exit.
            if line.strip() == "QUIT":
                break
            # Skip processing if the line is empty.
            if not line.strip():
                continue
            # Split the line into two parts: the action and the message.
            parts = line.split(maxsplit=1)
            action = parts[0]
            message = parts[1] if len(parts) > 1 else ""

             # Create a timestamp in the format "YYYY-MM-DD HH:MM".
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Format the log entry.
            log_line = f"{timestamp} [{action}] {message}\n"
            log_file.write(log_line)
            log_file.flush()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Always close the log file.
        log_file.close()

if __name__ == "__main__":
    main()
