import re
import tokenize
import io
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_comments(string, comment_pattern):
    comments = re.findall(comment_pattern, string)
    stripped_string = re.sub(comment_pattern, "", string)
    return stripped_string

def browse_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Pegasus Text", "*.pg")])
    if file_path:
        messagebox.showinfo("Analysis Complete", "Lexical analysis completed successfully!")
        return get_file(file_path)
        
    else:
        messagebox.showwarning("Invalid File", "Please select a valid Pegasus file.")

def get_file(file_path):
    try:

        with open(file_path, 'r') as content:
            return content.read()
    
    except FileNotFoundError:
        print("File not found!")
        return ""
            



# Single-line and multi-line comments
comment_pattern = r"//(.*?)\n|\/\*[\s\S]*?\*\/"
clean_code = remove_comments(browse_file(), comment_pattern)
print(clean_code + "\n")
tokens = tokenize.generate_tokens(io.StringIO(clean_code).readline)
lexemes = [token.string for token in tokens]

token_pattern_dict = {
    r'^\d+$': "LIT_INT",
    r'^"(?:\\.|[^"\\])*"$': "LIT_STRING",
    r'^\d+.\d+$': "LIT_FLOAT",
    r"^[Tt]rue$|^[Ff]alse$": "LIT_BOOL",
    r"^[Nn]ull$": "LIT_NULL",
    r"'([^'\\]|\\.)'": "LIT_CHAR",
    r"^[Aa]$|^[Aa]n$|^[Tt]he$": "NW",
    "could": "COULD_KW",
    "only": "ONLY_KW",
    r"^[Ll]et": "LET_KW",
    r"^be$": "BE_KW",
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

TOKEN_NAMES = []
print(f"{'':<2}|  {'lexeme':<10}\t|  {'token_name':<10}")
print("--------------------------------------")
count = 0
for lexeme in lexemes:
    
    for pattern, token_name in token_pattern_dict.items():
        if re.match(pattern, lexeme):
            if lexeme == "\n":
                
              print(f"{count:<2}|  {'--':<10}\t|  {token_name:<10}")
              TOKEN_NAMES.append(token_name)
              count+=1
              break

            print(f"{count:<2}|  {lexeme:<10}\t|  {token_name:<10}")
            TOKEN_NAMES.append(token_name)
            count+=1
            break  # Stop after first match (if needed)

def split_tokens_into_statements(tokens):
    statements = []
    current_statement = []

    for token in tokens:
        if token == "DELIM_NEWLINE":
            statements.append(current_statement)
            current_statement = []
        else:
            current_statement.append(token)

    # Add the last statement if it doesn't end with a newline
    if current_statement:
        statements.append(current_statement)

    return statements
