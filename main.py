import sys

KEYWORDS = set("""SELECT FROM WHERE INSERT INTO VALUES CREATE TABLE UPDATE SET DELETE
AND OR NOT IS NULL INTEGER TEXT BEGIN COMMIT ROLLBACK ORDER BY LIMIT OFFSET
COUNT SUM AVG MIN MAX ASC DESC INDEX ON""".split())

# The token kinds, spelled exactly as they are printed.
KEYWORD, IDENTIFIER, NUMBER, STRING, OPERATOR, SYMBOL = (
    "KEYWORD", "IDENTIFIER", "NUMBER", "STRING", "OPERATOR", "SYMBOL")


def is_alpha(c):
    return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_"


def is_digit(c):
    return "0" <= c <= "9"

def tokenize(line):
    """Split one line of SQL into tokens.

    Returns (tokens, error). tokens is a list of (kind, text); error is None on success or the
    message that follows "ERR " when the line cannot be tokenized.
    """
    toks = []
    i, n = 0, len(line)
    while i < n:
        c = line[i]
        if c in " \t\r":
            i += 1
        elif c in "(),;":
            toks.append((SYMBOL, c))
            i += 1
        else:
            # TODO: comments (-- to end of line), 'strings' and "quoted identifiers" with a doubled
            # quote as an escape, numbers (and the malformed ones), words (keyword or identifier),
            # and operators (two-character ones first). Anything else is an error.
            return None, "unexpected character: " + c
    return toks, None

def main():
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        toks, err = tokenize(line)
        if err:
            print("ERR " + err)
            continue
        for kind, text in toks:
            print(kind + " " + text)
        print("END")


main()
