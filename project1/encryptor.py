#!/usr/bin/env python3
import sys

def vigenere_encrypt(plaintext, key):
    # Assumes plaintext and key are uppercase and contain only letters.
    ciphertext = []
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            p = ord(char) - ord('A')
            k = ord(key[i % key_length]) - ord('A')
            c = (p + k) % 26
            ciphertext.append(chr(c + ord('A')))
        else:
            ciphertext.append(char)  # Although input is assumed valid.
    return "".join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    plaintext = []
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            c = ord(char) - ord('A')
            k = ord(key[i % key_length]) - ord('A')
            p = (c - k + 26) % 26
            plaintext.append(chr(p + ord('A')))
        else:
            plaintext.append(char)
    return "".join(plaintext)

def main():
    current_key = None
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue
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
            if current_key is None:
                print("ERROR Password not set")
                sys.stdout.flush()
            else:
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
            print("ERROR Unknown command")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
