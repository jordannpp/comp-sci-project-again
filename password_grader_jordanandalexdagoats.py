"""
COP1500 PROJECT — PASSWORD GRADER
Authors: Jordan and Alex 

"""

import time
import random

# colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# animations
def type_text(text, delay=0.02):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def loading(text):
    print(text, end="")
    for i in range(5):
        print(".", end="", flush=True)
        time.sleep(0.2)
    print()

def progress_bar(percent):
    filled = int(percent / 5)
    bar = "█" * filled + "-" * (20 - filled)
    print(f"[{bar}] {percent}% strength\n")

# responses
friendly = [
    "Nice job! That’s a solid password!",
    "Good effort! Keep improving!",
    "Looks better than most people’s passwords!"
]

roasty = [
    "Its okay I guess bro.",
    "Even my toaster could guess that one.",
    "Bro really?"
]

professional = [
    "Password analysis complete. Improvement recommended.",
    "Password meets acceptable strength criteria.",
    "Password security: satisfactory."
]

# weak passwords
COMMON = ["password", "123456", "qwerty", "admin", "letmein"]

def score_length(pw):
    L = len(pw)
    if L == 0:
        return 0, "Empty password."
    elif L < 8:
        return 10, f"Length {L}: too short."
    elif L < 12:
        return 20, f"Length {L}: okay length."
    else:
        return 30, f"Length {L}: great length."

def score_variety(pw):
    lower = any(c.islower() for c in pw)
    upper = any(c.isupper() for c in pw)
    digit = any(c.isdigit() for c in pw)
    symbol = any(not c.isalnum() for c in pw)
    count = lower + upper + digit + symbol

    if count == 4:
        return 25, "Excellent character mix."
    elif count == 3:
        return 18, "Good mix, missing one type."
    elif count == 2:
        return 12, "Weak mix."
    else:
        return 6, "Very poor variety."

def score_common(pw):
    p = pw.lower()
    for word in COMMON:
        if word in p:
            return 2, f"Contains common pattern '{word}'."
    return 10, "No common words found."

def score_patterns(pw):
    notes = []
    score = 25
    for i in range(1, len(pw)):
        if pw[i] == pw[i - 1]:
            score -= 5
            notes.append("Repeated characters detected.")
            break
    if "123" in pw or "abc" in pw.lower():
        score -= 10
        notes.append("Sequence like '123' or 'abc' found.")
    if score < 0:
        score = 0
    reason = " | ".join(notes) if notes else "No weak patterns found."
    return score, reason

def score_unique(pw):
    unique = len(set(pw))
    ratio = unique / len(pw)
    pts = int(ratio * 10)
    return pts, "Character uniqueness evaluated."

# encryption stuff forr requierment
def encrypt_text(text, shift=3):
    encrypted = ""
    for ch in text:
        encrypted += chr((ord(ch) + shift) % 126)
    return encrypted

def decrypt_text(text, shift=3):
    decrypted = ""
    for ch in text:
        decrypted += chr((ord(ch) - shift) % 126)
    return decrypted

def generate_password():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    pw = "".join(random.choice(chars) for _ in range(12))
    print(GREEN + "\nGenerated password:" + RESET)
    print(pw)
    return pw

def save_history(pw, score):
    masked = "*" * len(pw)
    encrypted_pw = encrypt_text(masked)
    try:
        with open("password_history.txt", "a") as f:
            f.write(f"{encrypted_pw},{score}\n")
    except:
        print(RED + "Error saving history." + RESET)

def show_history():
    try:
        with open("password_history.txt", "r") as f:
            lines = f.readlines()
            print("\nPassword History:")
            for line in lines:
                enc, score = line.strip().split(",")
                print(f"{decrypt_text(enc)} | Score: {score}")
    except:
        print(YELLOW + "No history found." + RESET)

def show_report(pw, total, details, comments, mode):
    print("\nPassword Report")
    progress_bar(total)

    for k, v in details.items():
        print(f"{k}: {v} pts")

    print("\nAnalysis:")
    for c in comments:
        print("-", c)

    print("\nResponse:")
    if mode == "A":
        print(GREEN + random.choice(friendly) + RESET)
    elif mode == "B":
        print(RED + random.choice(roasty) + RESET)
    else:
        print(BLUE + random.choice(professional) + RESET)

def evaluate(pw):
    details = {}
    comments = []

    s, c = score_length(pw)
    details["Length"] = s
    comments.append(c)

    s, c = score_variety(pw)
    details["Variety"] = s
    comments.append(c)

    s, c = score_patterns(pw)
    details["Patterns"] = s
    comments.append(c)

    s, c = score_common(pw)
    details["Common"] = s
    comments.append(c)

    s, c = score_unique(pw)
    details["Unique"] = s
    comments.append(c)

    total = sum(details.values())
    if total > 100:
        total = 100
    return total, details, comments

def main():
    type_text(CYAN + "Welcome to the Password Grader!" + RESET)
    while True:
        print("\nMenu:")
        print("1 - Check a password")
        print("2 - Generate password")
        print("3 - View history")
        print("4 - Exit")

        choice = input("Enter choice: ")

        if choice == "4":
            type_text("Goodbye!")
            break
        elif choice == "1":
            print("\nChoose Mode:")
            print("A - Friendly")
            print("B - Roast")
            print("C - Professional")
            mode = input("Enter A/B/C: ").upper()
            pw = input("\nEnter password: ")
            loading("Analyzing password")
            total, details, comments = evaluate(pw)
            show_report(pw, total, details, comments, mode)
            save_history(pw, total)
        elif choice == "2":
            generate_password()
        elif choice == "3":
            show_history()
        else:
            print(RED + "Invalid choice, try again." + RESET)

main()