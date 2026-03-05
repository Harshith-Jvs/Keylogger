import re

INPUT_FILE = "keylogs.txt"
OUTPUT_FILE = "cleaned_keylogs.txt"

def apply_key_logic(text, token):
    if token == "[BKSP]":
        if text:
            text.pop()

    elif token == "[ENTER]":
        text.append("\n")

    elif token == "[TAB]":
        text.append("\t")

    elif token == "[SPACE]":
        text.append(" ")

    elif token == "[ESC]":
        pass  # ignore

    else:
        text.append(token)

    return text


def process_line(line, buffer):
    tokens = re.findall(r'\[[A-Z]+\]|.', line)

    for token in tokens:
        buffer = apply_key_logic(buffer, token)

    return buffer


def clean_log():

    output = []
    buffer = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:

        for line in f:
            line = line.rstrip("\n")

            # detect app headers
            if line.startswith("[") and "App:" in line:
                if buffer:
                    output.append("".join(buffer))
                    buffer = []

                output.append("\n\n" + line + "\n")
                continue

            buffer = process_line(line, buffer)

    if buffer:
        output.append("".join(buffer))

    return "".join(output)


def main():

    cleaned = clean_log()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print("Cleaned file written to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()