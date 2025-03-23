#!/usr/bin/env python
import sys
import datetime
import codecs

def main():
    if len(sys.argv) < 2:
        print("Usage: python logger.py <log_filename>")
        sys.exit(1)

    log_filename = sys.argv[1]

    # Open the log file in append mode
    with codecs.open(log_filename, 'a', 'utf8') as log_file:
        while True:
            line = sys.stdin.readline()
            if not line:
                # If stdin is closed or pipe is broken, exit
                break

            line = line.strip()
            if line == "QUIT":
                # When we see "QUIT", we stop logging and exit
                break

            # Split the first token (ACTION) from the rest (MESSAGE)
            parts = line.split(None, 1)
            if len(parts) == 1:
                action, message = parts[0], ""
            else:
                action, message = parts[0], parts[1]

            # Make a timestamp string in "YYYY-MM-DD HH:MM" format
            now = datetime.datetime.now()
            time_str = now.strftime("%Y-%m-%d %H:%M")

            # Write out the log entry: 2025-03-02 11:32 [START] Logging Started.
            log_entry = "{} [{}] {}\n".format(time_str, action, message)
            log_file.write(log_entry)
            log_file.flush()

if __name__ == "__main__":
    main()
