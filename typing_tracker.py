"""
Typing and Accuracy Tracker
---------------------------
A small command-line program that:
  1. shows a practice passage,
  2. times how long you take to type it,
  3. calculates your words per minute (WPM) and accuracy,
  4. lists the words you got wrong,
  5. saves every attempt to results.csv so you can track improvement.

Run it with:   python typing_tracker.py
Needs only Python 3 (no extra packages).
"""

import csv
import difflib
import os
import random
import time
from datetime import datetime

RESULTS_FILE = "results.csv"

# Practice passages (each one is a single line, so pressing Enter ends the test).
PASSAGES = [
    "A good transcriptionist listens carefully and types every word exactly as it is spoken.",
    "Accuracy matters more than speed, because a single wrong word can change the meaning of a sentence.",
    "Regular practice helps the fingers remember the keyboard, and the mind stay calm under deadlines.",
    "Every recording carries a real voice, and it deserves to be written down faithfully and with care.",
    "Punctuation, spelling and formatting turn a rough draft into a clean and professional document.",
]


def analyse(reference, typed, seconds):
    """Compare typed text with the reference.

    Returns (wpm, accuracy, mistakes) where
      wpm      = words per minute, using the standard rule of 5 characters = 1 word
      accuracy = percentage of reference words typed correctly
      mistakes = list of (expected_word, typed_word) pairs that did not match
    """
    minutes = max(seconds, 1) / 60  # avoid dividing by zero
    wpm = (len(typed) / 5) / minutes

    ref_words = reference.split()
    typed_words = typed.split()

    # SequenceMatcher lines up the two word lists and tells us where they differ.
    matcher = difflib.SequenceMatcher(None, ref_words, typed_words)
    correct = 0
    mistakes = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            correct += i2 - i1
        else:
            expected = " ".join(ref_words[i1:i2]) or "(nothing)"
            got = " ".join(typed_words[j1:j2]) or "(missing)"
            mistakes.append((expected, got))

    accuracy = 100 * correct / len(ref_words) if ref_words else 0
    return wpm, accuracy, mistakes


def save_result(wpm, accuracy):
    """Append one attempt to results.csv (creates the file with a header the first time)."""
    new_file = not os.path.exists(RESULTS_FILE)
    with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["date", "wpm", "accuracy"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), f"{wpm:.1f}", f"{accuracy:.1f}"])


def load_results():
    """Read all saved attempts as a list of (date, wpm, accuracy)."""
    if not os.path.exists(RESULTS_FILE):
        return []
    with open(RESULTS_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [(r["date"], float(r["wpm"]), float(r["accuracy"])) for r in rows]


def run_test():
    """Run one typing test from start to finish."""
    passage = random.choice(PASSAGES)
    print("\nType the line below exactly as shown, then press Enter.\n")
    print(passage + "\n")
    input("Press Enter when you are ready to start...")

    start = time.time()
    typed = input("> ")
    seconds = time.time() - start

    wpm, accuracy, mistakes = analyse(passage, typed.strip(), seconds)

    print(f"\nTime     : {seconds:.1f} seconds")
    print(f"Speed    : {wpm:.1f} WPM")
    print(f"Accuracy : {accuracy:.1f}%")
    if mistakes:
        print("Mistakes :")
        for expected, got in mistakes:
            print(f"  expected '{expected}'  ->  you typed '{got}'")
    else:
        print("Perfect! No mistakes.")

    save_result(wpm, accuracy)


def show_history():
    """Print the last five attempts plus your average and best scores."""
    results = load_results()
    if not results:
        print("\nNo attempts saved yet. Take a test first!")
        return

    print("\nLast 5 attempts:")
    for date, wpm, accuracy in results[-5:]:
        print(f"  {date}   {wpm:5.1f} WPM   {accuracy:5.1f}%")

    avg_wpm = sum(r[1] for r in results) / len(results)
    avg_acc = sum(r[2] for r in results) / len(results)
    best_wpm = max(r[1] for r in results)
    print(f"\nAttempts: {len(results)}")
    print(f"Average : {avg_wpm:.1f} WPM at {avg_acc:.1f}% accuracy")
    print(f"Best    : {best_wpm:.1f} WPM")


def main():
    print("=== Typing and Accuracy Tracker ===")
    while True:
        print("\n1) Take a typing test")
        print("2) See my progress")
        print("3) Quit")
        choice = input("Choose 1, 2 or 3: ").strip()
        if choice == "1":
            run_test()
        elif choice == "2":
            show_history()
        elif choice == "3":
            print("Keep practising. See you next time!")
            break
        else:
            print("Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
