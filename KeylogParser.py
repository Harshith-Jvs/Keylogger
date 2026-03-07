import re

INPUT_FILE = "keylogs.txt"
OUTPUT_FILE = "cleaned_keylogs.txt"


def decode_line(raw_line):
    try:
        return raw_line.decode("utf-8")
    except UnicodeDecodeError:
        return raw_line.decode("cp1252")


def apply_key_logic(text, token):

    if token in ("[BKSP]", "[DEL]"):
        if text:
            text.pop()

    elif token == "[ENTER]":
        text.append("\n")

    elif token == "[TAB]":
        text.append("\t")

    elif token == "[SPACE]":
        text.append(" ")

    elif token in ("[ESC]", "[SHIFT]", "[CTRL]", "[ALT]",
                   "[LEFT]", "[RIGHT]", "[UP]", "[DOWN]"):
        pass
    else:
        text.append(token)

    return text


def process_line(line, buffer):

    tokens = re.findall(r'\[[^\]]+\]|.', line)

    for token in tokens:
        buffer = apply_key_logic(buffer, token)

    return buffer


def parse_header(line):

    match = re.search(r"\[(.*?)\]", line)
    app_match = re.search(r"App:\s*(.*)", line)

    date = ""
    time = ""

    if match:
        parts = match.group(1).split()
        if len(parts) == 2:
            date, time = parts

    app = app_match.group(1) if app_match else ""

    return date, time, app


def clean_log():

    output = []
    buffer = []
    first_log = True

    with open(INPUT_FILE, "rb") as f:

        for raw_line in f:

            line = decode_line(raw_line).strip()

            if line.startswith("[") and "App:" in line:

                # Close previous log
                if not first_log:
                    output.append("".join(buffer).rstrip())
                    output.append("\n\n")
                    buffer = []

                first_log = False

                date, time, app = parse_header(line)

                output.append("-------- LOG --------\n")
                output.append(f"Date : {date}\n")
                output.append(f"Time : {time}\n")
                output.append(f"App  : {app}\n")
                output.append("Keys : \n")

                continue

            buffer = process_line(line, buffer)

    # close last log
    output.append("".join(buffer).rstrip())
    output.append("\n\n")

    return "".join(output)


def main():

    cleaned = clean_log()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print("Cleaned file written to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
