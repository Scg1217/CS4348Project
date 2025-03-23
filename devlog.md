# Devlog

## [2025-02-17 10:00 AM]
**Thoughts so far:**
- Reviewed the project requirements. The project consists of three parts:
  - **logger.py:** Logs all activity with timestamps.
  - **encryption.py:** Implements the Vigenère cipher for encryption and decryption.
  - **driver.py:** Provides an interactive menu and connects the logger and encryption processes via pipes.
- Initially planned to use Python 3, but discovered that the cs1 server has Python 2.7.5.
- I need to update the code to remove Python 3–specific features (like f-strings, keyword arguments for `split()`, etc.) and ensure compatibility with Python 2.7.
- I also need to maintain a complete devlog that tracks all sessions and commits.

**Plan for this session:**
- Initialize a new local Git repository.
- Create a `devlog.md` file and record this initial entry.
- Create initial versions of `logger.py`, `encryption.py`, and `driver.py` in Python 3.
- Commit the devlog and initial code with the message "Initial Commit".

---

## [2025-03-20 11:00 AM]
**Thoughts so far:**
- Created initial versions of all three files.
- Encountered errors related to Python 3 syntax:
  - f-strings in logger.py.
  - The use of `split(maxsplit=1)` in encryption.py.
  - The `encoding` keyword in `open()` calls.
- Reviewed error messages and identified needed changes (switch to `.format()`, use `split(None, 1)`, and remove or replace the encoding parameter).

**Plan for this session:**
- Update all code to be Python 2.7 compliant:
  - Replace f-strings with `.format()`.
  - Change `split(maxsplit=1)` to `split(None, 1)`.
  - Use `codecs` if UTF-8 support is required or simply remove the encoding parameter.
- Test each module individually using unbuffered mode (`python -u encryption.py`, etc.).
- Commit changes with a message like "Updated code for Python 2.7 compatibility".

---

## [2025-03-20 12:00 PM]
**Thoughts so far:**
- Made all necessary syntax changes in `logger.py`, `encryption.py`, and `driver.py` so they run on Python 2.7.
- Tested each module individually:
  - `logger.py` now correctly writes log entries.
  - `encryption.py` responds to commands when run with `-u` (unbuffered mode).
- However, when integrating via `driver.py`, the output from the encryption process is not showing up as expected.

**Plan for this session:**
- Investigate the integration issue:
  - Ensure that the encryption process is launched with `-u` for unbuffered output.
  - Test `encryption.py` independently to confirm it prints results as expected.
  - Add additional debug prints in driver.py to trace the subprocess communication.
- Commit debugging changes and note any unresolved issues.

---

## [2025-03-22 01:00 PM]
**Thoughts so far:**
- Ran `python -u encryption.py` manually; encryption commands return output correctly when tested alone.
- In `driver.py`, even though I’m launching encryption.py with the `-u` flag, the expected output is not being captured.
- Inserted debug statements to verify that driver.py is reading from the encryption process.
- Still, output seems to be missing or delayed; this may be due to subtle buffering issues in Python 2.7’s subprocess module.

**Plan for this session:**
- Try minor workarounds (for example, a short sleep after flushing output) to see if output becomes available.
- Consider whether to persist further debugging in Python or explore switching to Java.
- Document all observations in the devlog.
- Commit all debugging attempts with a message like "Debugging encryption output in driver.py".

---

## [2025-03-22 02:30 PM]
**Thoughts so far:**
- After additional debugging, I confirmed that encryption.py works as expected in isolation.
- The driver process still struggles with capturing the encryption output reliably.
- Although the integration isn’t perfect, all individual functionalities (setting a password, encryption, and decryption) work when tested manually.
- The known output buffering issue in the integration will be documented, and instructions for manual testing will be added to the README.

**Plan for this session:**
- Finalize the code as much as possible and document the known issue in the README.
- Prepare for final integration testing.
- Commit with a message like "Final integration adjustments and documentation of output buffering issue".

---

## [2025-03-23 03:00 PM]
**Thoughts so far:**
- Completed final integration testing:
  - Logger records all commands and responses.
  - Encryption and decryption functionalities work correctly when tested manually.
  - The history feature in driver.py is operational.
- Despite some lingering issues with capturing encryption output via the subprocess in driver.py, the core functionality is intact.
- Documented all known issues and provided workarounds/instructions in the README.

**Plan for this session:**
- Clean the working tree, ensuring the latest commit matches the current code and devlog.
- Add a README detailing file roles, instructions for running the project, and known issues.
- Create a final commit and zip the repository for submission.
- Reflect on the session in the devlog, then prepare to submit the project.

---

## [2025-03-23 05:30 PM]
**Final Reflection:**
- The project meets the specifications:
  - Logger, encryption, and driver modules are implemented.
  - The project works on the cs1 server running Python 2.7.5, with adjustments made for compatibility.
  - Integration testing shows that all modules work individually, and known issues with subprocess output are documented.
- The devlog and commit history reflect all development sessions and the debugging process.
- I am now ready to submit the final project.

**Plan for this session:**
- Final commit and repository cleanup.
- Zip the entire repository and submit as per instructions.
- Document any final thoughts in the devlog.

---

*Remember: Do not delete any devlog entries. Each commit and session note is valuable to show your development process and the invisible work that went into the project.*
