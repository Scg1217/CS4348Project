#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
encryption.py

This program implements encryption and decryption using the Vigenère cipher.
It reads commands from standard input and outputs responses for each command.

Supported commands:
- PASS (or PASSKEY): Sets the encryption key.
- ENCRYPT: Encrypts a given plaintext using the current key.
- DECRYPT: Decrypts a given ciphertext using the current key.
- QUIT: Exits the program.

The cipher operates on uppercase letters only. Non-letter characters are not processed.
"""

import sys

def vigenere_encrypt(plaintext, key):
    """
    Encrypts plaintext using the Vigenère cipher with the given key.
    Both plaintext and key should be uppercase strings containing only letters.
    """
    ciphertext = []
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            p = ord(char) - ord('A')
            k = ord(key[i % key_length]) - ord('A')
            c = (p + k) % 26
            ciphertext.append(chr(c + ord('A')))
        else:
            ciphertext.append(char)
    return "".join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    """
    Decrypts ciphertext using the Vigenère cipher with the given key.
    Both ciphertext and key should be uppercase strings containing only letters.
    """
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
    current_key = None  # Initially, no encryption key is set.
    
    # Process each command received from standard input.
    while True:
        line = sys.stdin.readline()
	if not line:
            break
        # Split the line into the command and its argument.
        line = line.rstrip("\n")
	if not line:
	    continue
	parts = line.split(None, 1)
        command = parts[0].upper()
        argument = parts[1] if len(parts) > 1 else ""
        
        if command == "QUIT":
            break
        
        elif command in ["PASS", "PASSKEY"]:
            # Set the encryption key.
            if not argument.isalpha():
                print("ERROR Invalid passkey. Must contain only letters.")
                sys.stdout.flush()
            else:
                current_key = argument.upper()
                print("RESULT")
                sys.stdout.flush()
        
        elif command == "ENCRYPT":
            # Ensure a key is set before encrypting.
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
                    print("RESULT {}".format(encrypted_text))
                    sys.stdout.flush()
        
        elif command == "DECRYPT":
            # Ensure a key is set before decrypting.
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
                    print("RESULT {}".format(decrypted_text))
                    sys.stdout.flush()
        
        else:
            # For any unrecognized command.
            print("ERROR Unknown command")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
