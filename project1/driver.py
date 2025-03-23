#!/usr/bin/env python2
"""
driver.py

This interactive driver program coordinates the logger and encryption programs.
It spawns both as subprocesses and communicates with them via pipes.

Features:
- Provides an interactive menu to set the encryption password, encrypt or decrypt strings,
  view the history, and quit.
- Sends user commands to the encryption program and logs commands/responses via the logger.
- Maintains a session history of non-sensitive strings.

Usage: python driver.py <logfile>
"""
from __future__ import print_function
import subprocess
import sys

def is_valid_string(s):
    # Check that the string contains only letters.
    return s.isalpha()

def log_message(logger_proc, action, message):
    """
    Sends a log message to the logger process.
    The message is formatted as: ACTION MESSAGE.
    """
    try:
        logger_proc.stdin.write("{} {}\n".format(action.upper(), message))
        logger_proc.stdin.flush()
    except Exception as e:
        print("Logging error: {}".format(e))

def choose_from_history(history, prompt):
    """
    Displays history entries and allows the user to select one.
    Returns the selected string or None if the user chooses to enter a new string.
    """
    if not history:
        return None
    print("History:")
    for idx, item in enumerate(history, start=1):
        print("{}. {}".format(idx, item))
    print("0. Enter a new string")
    while True:
        choice = raw_input(prompt).strip()  # Use raw_input for Python 2.
        if choice.isdigit():
            choice_num = int(choice)
            if choice_num == 0:
                return None
            elif 1 <= choice_num <= len(history):
                return history[choice_num - 1]
        print("Invalid selection. Please try again.")

def main():
    # Check that exactly one command-line argument (log file name) is provided.
    if len(sys.argv) != 2:
        print("Usage: python driver.py <logfile>")
        sys.exit(1)
    log_filename = sys.argv[1]
    
    # Start the logger process.
    try:
        logger_proc = subprocess.Popen(
            [sys.executable, "logger.py", log_filename],
            stdin=subprocess.PIPE,
            universal_newlines=True  # For text mode in Python 2.
        )
    except Exception as e:
        print("Failed to start logger: {}".format(e))
        sys.exit(1)
    
    # Start the encryption process.
    try:
        enc_proc = subprocess.Popen(
            [sys.executable,"-u", "encryption.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
	    bufsize=1,
            universal_newlines=True  # For text mode.
        )
    except Exception as e:
        print("Failed to start encryption program: {}".format(e))
        sys.exit(1)
    
    # Log the start of the driver program.
    log_message(logger_proc, "START", "Driver program started")
    
    history = []  # To maintain session history.
    
    menu = """
Commands:
  password - Set encryption password
  encrypt  - Encrypt a string
  decrypt  - Decrypt a string
  history  - Show history
  quit     - Exit the program
"""
    while True:
        print(menu)
        cmd = raw_input("Enter command: ").strip().lower()
        
        if cmd == "password":
            log_message(logger_proc, "CMD", "password command invoked")
            use_history = raw_input("Use a string from history? (y/n): ").strip().lower()
            selected = None
            if use_history == 'y':
                selected = choose_from_history(history, "Select a number from history (or 0 to enter new): ")
            if selected is None:
                pwd = raw_input("Enter new password (letters only): ").strip()
                if not is_valid_string(pwd):
                    print("Error: Password must contain only letters.")
                    log_message(logger_proc, "ERROR", "Invalid password entered")
                    continue
                pwd = pwd.upper()
            else:
                pwd = selected.upper()
            
            try:
                enc_proc.stdin.write("PASS {}\n".format(pwd))
                enc_proc.stdin.flush()
                log_message(logger_proc, "PASS", "Password set (value hidden)")
                response = enc_proc.stdout.readline().strip()
                print(response)
                log_message(logger_proc, "RESULT", "Password command response: {}".format(response))
            except Exception as e:
                print("Error communicating with encryption program: {}".format(e))
                log_message(logger_proc, "ERROR", "Encryption program communication error: {}".format(e))
                
        elif cmd == "encrypt":
            log_message(logger_proc, "CMD", "encrypt command invoked")
            use_history = raw_input("Use a string from history? (y/n): ").strip().lower()
            selected = None
            if use_history == 'y':
                selected = choose_from_history(history, "Select a number from history (or 0 to enter new): ")
            if selected is None:
                plaintext = raw_input("Enter string to encrypt (letters only): ").strip()
                if not is_valid_string(plaintext):
                    print("Error: Input must contain only letters.")
                    log_message(logger_proc, "ERROR", "Invalid input for encryption")
                    continue
                plaintext = plaintext.upper()
                history.append(plaintext)
            else:
                plaintext = selected.upper()
            try:
                enc_proc.stdin.write("ENCRYPT {}\n".format(plaintext))
                enc_proc.stdin.flush()
                response = enc_proc.stdout.readline().strip()
                print(response)
                log_message(logger_proc, "RESULT", "Encrypt command response: {}".format(response))
                if response.startswith("RESULT"):
                    parts = response.split(None, 1)
                    if len(parts) == 2:
                        encrypted_text = parts[1]
                        history.append(encrypted_text)
            except Exception as e:
                print("Error communicating with encryption program: {}".format(e))
                log_message(logger_proc, "ERROR", "Encryption program communication error: {}".format(e))
                
        elif cmd == "decrypt":
            log_message(logger_proc, "CMD", "decrypt command invoked")
            use_history = raw_input("Use a string from history? (y/n): ").strip().lower()
            selected = None
            if use_history == 'y':
                selected = choose_from_history(history, "Select a number from history (or 0 to enter new): ")
            if selected is None:
                ciphertext = raw_input("Enter string to decrypt (letters only): ").strip()
                if not is_valid_string(ciphertext):
                    print("Error: Input must contain only letters.")
                    log_message(logger_proc, "ERROR", "Invalid input for decryption")
                    continue
                ciphertext = ciphertext.upper()
                history.append(ciphertext)
            else:
                ciphertext = selected.upper()
            try:
                enc_proc.stdin.write("DECRYPT {}\n".format(ciphertext))
                enc_proc.stdin.flush()
                response = enc_proc.stdout.readline().strip()
                print(response)
                log_message(logger_proc, "RESULT", "Decrypt command response: {}".format(response))
                if response.startswith("RESULT"):
                    parts = response.split(None, 1)
                    if len(parts) == 2:
                        decrypted_text = parts[1]
                        history.append(decrypted_text)
            except Exception as e:
                print("Error communicating with encryption program: {}".format(e))
                log_message(logger_proc, "ERROR", "Encryption program communication error: {}".format(e))
                
        elif cmd == "history":
            log_message(logger_proc, "CMD", "history command invoked")
            if history:
                print("History:")
                for idx, item in enumerate(history, start=1):
                    print("{}. {}".format(idx, item))
            else:
                print("History is empty.")
            log_message(logger_proc, "RESULT", "Displayed history")
            
        elif cmd == "quit":
            log_message(logger_proc, "CMD", "quit command invoked")
            try:
                enc_proc.stdin.write("QUIT\n")
                enc_proc.stdin.flush()
            except Exception as e:
                print("Error sending QUIT to encryption program: {}".format(e))
                log_message(logger_proc, "ERROR", "Error sending QUIT to encryption program: {}".format(e))
            try:
                logger_proc.stdin.write("QUIT\n")
                logger_proc.stdin.flush()
            except Exception as e:
                print("Error sending QUIT to logger: {}".format(e))
            log_message(logger_proc, "EXIT", "Driver program exiting")
            break
        else:
            print("Invalid command. Please try again.")
            log_message(logger_proc, "ERROR", "Invalid command entered: {}".format(cmd))
            
    # Wait for both child processes to finish.
    enc_proc.wait()
    logger_proc.wait()
    print("Driver program terminated.")

if __name__ == "__main__":
    main()
