#!/usr/bin/env python3
import sys

def vigenere_encrypt(plaintext, key):
    ciphertext = [] # List to accumulate encrypted characters.
    key_length = len(key)

    # Process each character in the plaintext.
    for i, char in enumerate(plaintext):
        if char.isalpha():
            # Convert character and corresponding key character to a 0-25 range.
            p = ord(char) - ord('A')
            k = ord(key[i % key_length]) - ord('A')
            # Compute the encrypted character using modulo 26 arithmetic.
            c = (p + k) % 26
            ciphertext.append(chr(c + ord('A')))
        else:
            ciphertext.append(char)  # If non-letter 
    return "".join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    plaintext = [] # List to accumulate decrypted characters.
    key_length = len(key)
    # Process each character in the ciphertext.
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            c = ord(char) - ord('A')
            k = ord(key[i % key_length]) - ord('A')
            # Compute the decrypted character using modulo arithmetic.
            p = (c - k + 26) % 26
            plaintext.append(chr(p + ord('A')))
        else:
            plaintext.append(char)
    return "".join(plaintext)

def main():
    current_key = None # Initialize the encryption key as None.

    # Continuously read commands from standard input.
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue # Skip empty lines.

        # Split the line into command and argument.
        parts = line.split(maxsplit=1)
        command = parts[0].upper()
        argument = parts[1] if len(parts) > 1 else ""
        
        if command == "QUIT":
            break
        elif command in ["PASS", "PASSKEY"]:
            # Set the current passkey.
            if not argument.isalpha():
                print("ERROR Invalid passkey. Must contain only letters.")
                sys.stdout.flush()
            else:
                current_key = argument.upper()
                print("RESULT")
                sys.stdout.flush()
        elif command == "ENCRYPT":
            # Check if the encryption key is set.
            if current_key is None:
                print("ERROR Password not set")
                sys.stdout.flush()
            else:
                # Validate that the argument contains only letters.
                if not argument.isalpha():
                    print("ERROR Input must contain only letters")
                    sys.stdout.flush()
                else:
                    plaintext = argument.upper()
                    encrypted_text = vigenere_encrypt(plaintext, current_key)
                    print(f"RESULT {encrypted_text}")
                    sys.stdout.flush()
        elif command == "DECRYPT":
            if current_key is None:
                print("ERROR Password not set")
                sys.stdout.flush()
            else:
                if not argument.isalpha():
                    print("ERROR Input must contain only letters")
                    sys.stdout.flush()
                else:
                    ciphertext = argument.upper()
                    decrypted_text = vigenere_decrypt(ciphertext, current_key)
                    print(f"RESULT {decrypted_text}")
                    sys.stdout.flush()
        else:
            # Handle unknown commands.
            print("ERROR Unknown command")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
