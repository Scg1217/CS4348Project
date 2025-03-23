#!/usr/bin/env python3
import subprocess
import sys

def is_valid_string(s):
    # Checks if the string contains only letters.
    return s.isalpha()

def log_message(logger_proc, action, message):
    """
    Sends a log message to the logger process.
    The action is the type of log (e.g., CMD, RESULT, ERROR) and the message contains details.
    """
    try:
        logger_proc.stdin.write(f"{action.upper()} {message}\n")
        logger_proc.stdin.flush()
    except Exception as e:
        print(f"Logging error: {e}")

def choose_from_history(history, prompt):
    """
    Display the history list with numbers and let the user choose one.
    Returns the selected string or None if the user opts to enter a new string.
    """
    if not history:
        return None
    print("History:")
    for idx, item in enumerate(history, start=1):
        print(f"{idx}. {item}")
    print("0. Enter a new string")
    while True:
        choice = input(prompt).strip()
        if choice.isdigit():
            choice_num = int(choice)
            if choice_num == 0:
                return None
            elif 1 <= choice_num <= len(history):
                return history[choice_num - 1]
        print("Invalid selection. Please try again.")

def main():
    # Ensure the log file name is provided as a command-line argument.
    if len(sys.argv) != 2:
        print("Usage: python driver.py <logfile>")
        sys.exit(1)
    log_filename = sys.argv[1]
    
    # Start the logger process.
    try:
        logger_proc = subprocess.Popen(
            [sys.executable, "logger.py", log_filename],
            stdin=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        print(f"Failed to start logger: {e}")
        sys.exit(1)
    
    # Start the encryption program.
    try:
        enc_proc = subprocess.Popen(
            [sys.executable, "encryptor.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        print(f"Failed to start encryption program: {e}")
        sys.exit(1)
    
    # Log the start of the driver.
    log_message(logger_proc, "START", "Driver program started")
    
    history = []  # Holds all strings entered or returned during this run.
    
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
        cmd = input("Enter command: ").strip().lower()
        
        if cmd == "password":
            log_message(logger_proc, "CMD", "password command invoked")
            use_history = input("Use a string from history? (y/n): ").strip().lower()
            selected = None
            if use_history == 'y':
                selected = choose_from_history(history, "Select a number from history (or 0 to enter new): ")
            if selected is None:
                pwd = input("Enter new password (letters only): ").strip()
                if not is_valid_string(pwd):
                    print("Error: Password must contain only letters.")
                    log_message(logger_proc, "ERROR", "Invalid password entered")
                    continue
                pwd = pwd.upper()
            else:
                pwd = selected.upper()
            
            # Send the PASS command (passwords are not logged in clear text).
            try:
                enc_proc.stdin.write(f"PASS {pwd}\n")
                enc_proc.stdin.flush()
                log_message(logger_proc, "PASS", "Password set (value hidden)")
                response = enc_proc.stdout.readline().strip()
                print(response)
                log_message(logger_proc, "RESULT", f"Password command response: {response}")
            except Exception as e:
                print(f"Error communicating with encryption program: {e}")
                log_message(logger_proc, "ERROR", f"Encryption program communication error: {e}")
                
        elif cmd == "encrypt":
            # Log the encrypt command invocation.
            log_message(logger_proc, "CMD", "encrypt command invoked")

            # Ask the user whether to use a string from history or enter a new plaintext.
            use_history = input("Use a string from history? (y/n): ").strip().lower()
            selected = None
            if use_history == 'y':
                selected = choose_from_history(history, "Select a number from history (or 0 to enter new): ")
            if selected is None:
                # Prompt for a new plaintext string.
                plaintext = input("Enter string to encrypt (letters only): ").strip()
                if not is_valid_string(plaintext):
                    print("Error: Input must contain only letters.")
                    log_message(logger_proc, "ERROR", "Invalid input for encryption")
                    continue
                plaintext = plaintext.upper()
                history.append(plaintext)
            else:
                plaintext = selected.upper()

            # Send the ENCRYPT command to the encryption process.
            try:
                enc_proc.stdin.write(f"ENCRYPT {plaintext}\n")
                enc_proc.stdin.flush()
                response = enc_proc.stdout.readline().strip()
                print(response)
                log_message(logger_proc, "RESULT", f"Encrypt command response: {response}")
                # If encryption succeeded, add the result to the history.
                if response.startswith("RESULT"):
                    parts = response.split(maxsplit=1)
                    if len(parts) == 2:
                        encrypted_text = parts[1]
                        history.append(encrypted_text)
            except Exception as e:
                print(f"Error communicating with encryption program: {e}")
                log_message(logger_proc, "ERROR", f"Encryption program communication error: {e}")
                
        elif cmd == "decrypt":
            # Log the decrypt command invocation.
            log_message(logger_proc, "CMD", "decrypt command invoked")

            # Ask the user whether to use a string from history or enter a new ciphertext.
            use_history = input("Use a string from history? (y/n): ").strip().lower()
            selected = None
            if use_history == 'y':
                selected = choose_from_history(history, "Select a number from history (or 0 to enter new): ")
            if selected is None:
                # Prompt for a new ciphertext string.
                ciphertext = input("Enter string to decrypt (letters only): ").strip()
                if not is_valid_string(ciphertext):
                    print("Error: Input must contain only letters.")
                    log_message(logger_proc, "ERROR", "Invalid input for decryption")
                    continue
                ciphertext = ciphertext.upper()
                history.append(ciphertext)
            else:
                ciphertext = selected.upper()

            # Send the DECRYPT command to the encryption process.
            try:
                enc_proc.stdin.write(f"DECRYPT {ciphertext}\n")
                enc_proc.stdin.flush()
                response = enc_proc.stdout.readline().strip()
                print(response)
                log_message(logger_proc, "RESULT", f"Decrypt command response: {response}")
                # If decryption succeeded, add the result to the history.
                if response.startswith("RESULT"):
                    parts = response.split(maxsplit=1)
                    if len(parts) == 2:
                        decrypted_text = parts[1]
                        history.append(decrypted_text)
            except Exception as e:
                print(f"Error communicating with encryption program: {e}")
                log_message(logger_proc, "ERROR", f"Encryption program communication error: {e}")
                
        elif cmd == "history":
            # Log that the history command was invoked.
            log_message(logger_proc, "CMD", "history command invoked")
            if history:
                print("History:")
                for idx, item in enumerate(history, start=1):
                    print(f"{idx}. {item}")
            else:
                print("History is empty.")
            log_message(logger_proc, "RESULT", "Displayed history")
            
        elif cmd == "quit":
            # Log the quit command.
            log_message(logger_proc, "CMD", "quit command invoked")
            # Send QUIT to encryption and logger programs.
            try:
                enc_proc.stdin.write("QUIT\n")
                enc_proc.stdin.flush()
            except Exception as e:
                print(f"Error sending QUIT to encryption program: {e}")
                log_message(logger_proc, "ERROR", f"Error sending QUIT to encryption program: {e}")
            try:
                logger_proc.stdin.write("QUIT\n")
                logger_proc.stdin.flush()
            except Exception as e:
                print(f"Error sending QUIT to logger: {e}")
            log_message(logger_proc, "EXIT", "Driver program exiting")
            break
        else:
            # Handle invalid commands.
            print("Invalid command. Please try again.")
            log_message(logger_proc, "ERROR", f"Invalid command entered: {cmd}")
            
    # Wait for the child processes to finish.
    enc_proc.wait()
    logger_proc.wait()
    print("Driver program terminated.")

if __name__ == "__main__":
    main()
