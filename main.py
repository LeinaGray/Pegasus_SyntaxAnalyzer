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
    r'^\d+$': "INT",
    r'^"(?:\\.|[^"\\])*"$': "STRING",
    r'^\d+.\d+$': "FLOAT",
    r"^[Tt]rue$|^[Ff]alse$": "BOOL",
    r"^[Nn]ull$": "NULL",
    r"'([^'\\]|\\.)'": "CHAR",
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

def fix_unsorted_array(arr):
  """
  Checks if an array is in order and prints the index of where an element should be deleted and inserted.

  Args:
      arr: The unsorted array.

  Returns:
      None
  """
  sorted_arr = sorted(arr)
  for i, item in enumerate(arr):
    if item != sorted_arr[i]:
      # Find the correct position for the item
      correct_index = sorted_arr.index(item)
      print(f"delete {item} in index {i}")
      print(f"insert at index {correct_index}")
      break

def has_all_items(tokens, grammar_rules):
    missing_tokens = []
    grammar_index = []
    for terminal in grammar_rules:
        # if isinstance(terminal, list):  # Handle nested arrays
        #     missing_nonterminals = has_all_items(tokens, terminal)
        #     if missing_nonterminals is not True:
        #         missing_tokens.extend(missing_nonterminals)
        if isinstance(terminal, str) and terminal.startswith("^"):  # Check for regex patterns
            regex = re.compile(terminal[1:])
            found_match = False
            for sub_item in tokens:
                if regex.match(sub_item):
                    found_match = True
                    break
            if not found_match:
                missing_tokens.append(terminal)
        elif terminal not in tokens:
            missing_tokens.append(terminal)

    for token in tokens:
        for terminal in grammar_rules:
            if terminal == token:
                grammar_index.append(grammar_rules.index(token))

    return missing_tokens, grammar_index

GRAMMAR_RULES = [["NW", "ID", "COULD_KW", "ONLY_KW", "BE_KW", r"^LIT_(STRING|INT|FLOAT|BOOL)$"],
                 ['DT_DECLARATION*', 'IDENT_DECLARATION*', 'STMT+'],
                 ['DEC_STMT', 'INPUT_STMT', 'OUT_STMT', 'ASS_STMT', 'COND_STMT', 'REL_STMT', 'CONV_STMT'],
                 ['CONDITION'],
                 ['EXPRESSION'],
                 ['ARITH_EXP', 'REL_EXP', 'LOG_EXP'],
                 ['IDENTIFIER', 'ARITH_OP', 'IDENTIFIER', 'LITERALS', 'ARITH_OP', 'LITERALS', 'IDENTIFIER', 'ARITH_OP', 'LITERALS', 'LITERALS', 'ARITH_OP', 'IDENTIFIER'],
                 ['IDENTIFIER', 'REL_OP', 'IDENTIFIER', 'ARITH_EXP', 'REL_OP', 'ARITH_EXP'],
                 ['REL_EXP', 'LOG_OP', 'REL_EXP', 'NOT_OP', 'IDENTIFIER', 'NOT_OP', 'REL_EXP'],
                 ['COMMENT'],
                 ['ML_C', 'SNGL_C'],
                 ['/*ASCII_SEQUENCE*/'],
                 ['//ASCII_SEQUENCE'],
                 ['IDENTIFIER', ',', 'IDENTIFIERS'],
                 ['STARTING_CHAR', 'STARTING_CHAR', 'SUBSEQUENT_CHARS'],
                 ['ALPHABET', 'UNDERSCORE'],
                 ['SUBSEQUENT_CHAR', 'SUBSEQUENT_CHAR', 'SUBSEQUENT_CHAR'],
                 ['ALPHABET', 'DIGITS', 'UNDERSCORE'],
                 ['_'],
                 ['RESERVE_WORDS', 'ARITH_OP', 'REL_OP', 'LOG_OP'],
                 ['LET_KW', 'COULD_KW', 'ONLY_KW', 'BE_KW', 'REL_OF', 'REL_IS', 'PTR', 'NAME_CONV', 'KW_CONV', 'PREP', 'QUANT', 'CONST', 'DT_MOD', 'OUT_KW', 'CONJ', 'FOR_KW', 'INPUT_KW', 'IF_KW', 'ELIF_KW', 'ELSE_KW'],
                 ['Let', 'let'],
                 ['Could', 'could'],
                 ['Only', 'only'],
                 ['Be', 'be'],
                 ['Of', 'of'],
                 ['Is', 'is'],
                 ['This', 'this', 'Each', 'each', 'It', 'it', 'Was', 'was'],
                 ['For', 'for'],
                 ['Remember', 'remember', 'Shorten', 'shorten', 'Represent', 'represent'],
                 ['Mean', 'mean'],
                 ['To', 'to', 'As', 'as', 'In', 'in'],
                 ['One', 'one'],
                 ['Always', 'always'],
                 ['Discrete', 'discrete', 'Continuous', 'continuous', 'Order', 'order', 'Boolean', 'boolean'],
                 ['Show', 'show', 'Read', 'read', 'Write', 'write', 'Open', 'open', 'Close', 'close', 'Change', 'change', 'Spell', 'spell', 'Count', 'count'],
                 ['Ask', 'ask'],
                 ['If', 'if'],
                 ['Then', 'then'],
                 ['Else', 'else'],
                 ['VALUE'],
                 ['LITERALS', 'IDENTIFIER', 'PTR', 'REL_VALUE'],
                 ['IDENTIFIER', 'REL_OF', 'STRING_LIT'],
                 ['LITERAL', 'LITERAL', ',', 'LITERALS'],
                 ['INT_LIT', 'FLT_LIT', 'BOOL_LIT', 'CHAR_LIT', 'STR_LIT', 'NULL_LIT'],
                 ['DIGIT', 'DIGITS'],
                 ['DIGITS', '.', 'DIGITS'],
                 ['true', 'false'],
                 ["ASCII", "ESCAPE_SEQUENCE"],
                 ['ASCII_SEQUENCE', 'ASCII_SEQUENCE', 'ESCAPE_SEQUENCE', 'ASCII_SEQUENCE'],
                 ['+', '_', '/', '*', '%'],
                 ['<', '>', '<=', '>=', '==', '!='],
                 ['&&', '||'],
                 ['!'],
                 ['+', '-', '*', '/', '=', '<', '>', '!', '@', '#', '$', '%', '^', '&', '(', ')', '_', '{', '}', '[', ']', '|', '\\', ':', ';', '?', '~'],
                 ['ALPHABET', 'DIGITS', 'SYMBOLS'],
                 ['ASCII', 'ASCII', 'ASCII_SEQUENCE', 'ASCII', 'ASCII_SEQUENCE'],
                 ['ALPHABET', 'DIGITS'],
                 ['LC', 'UC'],
                 ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
                 ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
                 ['DIGIT', 'DIGIT', 'DIGITS'],
                 ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                 ["'", '"', '\\', '\\t', '\\b', '\\n', '\\r', '\\f', '\\v', '\\a', '?', '\\0'],
                 ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '}', '~']]

DEC_STMT = [r"^(NW)?$", "ID", "COULD_KW", "ONLY_KW", "BE_KW", "STRING"] #TODO: ALLOW GRAMMAR RULES ABOVE, FIX LITERALS REGEX(?)

missing_items, token_index = has_all_items(TOKEN_NAMES, DEC_STMT)
print(token_index)
if not missing_items:
    print("correct syntax")
else:
    print("You are missing the following keywords")
    for item in missing_items:
        print("\t" + item)

def find_insertion_index(unsorted_list):
    """
    Finds the index where an item should be inserted in an unsorted list to maintain sorted order.

    Args:
        unsorted_list: A list of unsorted elements.

    Returns:
        The index where the item should be inserted.
    """

    if len(unsorted_list) <= 1:
        return 0

    for i in range(1, len(unsorted_list)):
        if unsorted_list[i] < unsorted_list[i - 1]:
            return i

    # If the item is larger than all elements, return the end of the list
    return len(unsorted_list)

insertion_index = find_insertion_index(token_index)
print(f"{DEC_STMT[insertion_index]} must be inserted after {lexemes[insertion_index]}") #TODO: ERROR AT NEW LINES, NEED PROPER ERROR HANDLING