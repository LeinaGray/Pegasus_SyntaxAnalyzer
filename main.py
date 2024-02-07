code = """//single-line comments are not recognized as tokens
/* multi-line comments 
  are also not recognized
*/
//BUG: NEWLINES AFTER COMMENTS ARE RECOGNIZED AS TOKEN
//separate string literals with commas with or without spaces
A score be could only be "d","d", "h" "h"
//separate integer literals with commas with or without spaces
A score could only be 1,2, 3
//invalid identifier
Let score 123d
//function declaration with tabs
def function
    print the word
//separate operators with or without spaces
Let score x be 3+3 3 + 3 =
//separate float literals
3.12
//BUG: STRING LITERAL WITH SPACES NOT DETECTED
"hello d"
"""

print(code)

import re
def remove_comments(string, comment_pattern):
    comments = re.findall(comment_pattern, string)
    stripped_string = re.sub(comment_pattern, "", string)
    return stripped_string

import tokenize
import io

# Single-line and multi-line comments
comment_pattern = r"//(.*?)\n|\/\*[\s\S]*?\*\/"
clean_code = remove_comments(code, comment_pattern)
print(clean_code)
tokens = tokenize.generate_tokens(io.StringIO(clean_code).readline)
lexemes = [token.string for token in tokens]

token_pattern_dict = {
    r'^\d+$': "LIT_INT",
    r'^"(?:\\.|[^"\\])*"$': "LIT_STRING",
    r'^\d+.\d+$': "LIT_FLOAT",
    r"^[Tt]rue$|^[Ff]alse$": "LIT_BOOL",
    r"^[Nn]ull$": "LIT_NULL",
    r"'([^'\\]|\\.)'": "LIT_CHAR",
    r"^[Aa]$|^[Aa]n$|^[Tt]he$": "NOISE",
    "could": "COULD_KW",
    "only": "ONLY_KW",
    r"^[Ll]et": "LET_KW",
    r"^be$": "ASSIGN_KW",
    "of": "REL_OF",
    "is": "REL_IS",
    r"^(this|each|it|was)$": "PTR",
    r"^(Remember|Shorten|Represent)$": "NAME_CONV", 
    r"^mean$": "KW_CONV",
    r"^(to|as|in)$": "PREP", 
    r"^one$": "QUANT",
    r"^always$": "CONST",
    r"^(discrete|continuous|order|boolean)$": "DT_MOD",
    r"^(show|ask|read|write|open|close|change|spell|count)$": "ACTION",  
    r"^(if|then|else|while)$": "CONJ", 
    r"^union$": "UNION",
    r"^(\+|-|\*|\/|%)$": "ARITH_OP",
    r"^[<>]=?|!=": "REL_OP",
    r"^(&&|\|\||!)$": "LOGICAL_OP", 
    r"^,$": "DELIM_COMMA",
    r"^\t$": "DELIM_TAB",
    r"^\n$": "DELIM_NEWLINE",
    r"^[a-zA-Z_][a-zA-Z0-9_]*$": "ID",
}
print(f"{'LEXEME':10}\t|\t{'TOKEN_NAME'}")
print("--------------------------------------")
for lexeme in lexemes:
    for pattern, token_name in token_pattern_dict.items():
        if re.match(pattern, lexeme):
            if lexeme == "\n":
              print(f"/{'n':10}\t|\t{token_name}")
              break

            print(f"{lexeme:10}\t|\t{token_name}")
            break  # Stop after first match (if needed)
        
        

grammar = ["A", "score"]





