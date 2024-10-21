MORSE = {
    ".-": "a",
    "-...": "b",
    "-.-.": "c",
    "-..": "d",
    ".": "e",
    "..-.": "f",
    "--.": "g",
    "....": "h",
    "..": "i",
    ".---": "j",
    "-.-": "k",
    ".-..": "l",
    "--": "m",
    "-.": "n",
    "---": "o",
    ".--.": "p",
    "--.-": "q",
    ".-.": "r",
    "...": "s",
    "-": "t",
    "..-": "u",
    "...-": "v",
    ".--": "w",
    "-..-": "x",
    "-.--": "y",
    "--..": "z",
}


def read_file():
    input_file = open("input.txt", "r")
    output_file = open("output.txt", "w")

    for line in input_file.readlines():
        symbols = line.split(" ")
        decrypted_symbols = []
        space_count = 0
        for symbol in symbols:
            if symbol:
                decrypted_symbols.append(MORSE[symbol])
            else:
                if space_count:
                    continue
                else:
                    decrypted_symbols.append(" ")
                space_count += 1
        decrypted_line = "".join(decrypted_symbols)
        output_file.write(decrypted_line + "\n")

    input_file.close()
    output_file.close()


def main():
    read_file()


if __name__ == "__main__":
    main()
