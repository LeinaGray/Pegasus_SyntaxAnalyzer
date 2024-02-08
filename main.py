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

def analyze_syntax(tokens, grammar_rules):
    missing_tokens = []
    misplaced_tokens = []
    correct_tokens = []
    grammar_index = []

    statements = split_tokens_into_statements(tokens)
    
    for statement in statements:
        matched_rules = []
        print("\n") 
        for rule in grammar_rules:
            matching_tokens = 0
            grammar_index.clear()    

            for token in tokens:
                if token in rule:
                    correct_tokens.append(token)
                    grammar_index.append(rule.index(token))
                    matching_tokens += 1
                elif any(re.match(terminal, token) for terminal in rule if isinstance(terminal, str) and terminal.startswith("^")):
                    correct_tokens.append(token) 
                    grammar_index.append(rule.index(next(terminal for terminal in rule if re.match(terminal, token))))
                    matching_tokens += 1
                elif token not in rule and not matched_rules:
                    misplaced_tokens.append(token)
                    
            if matching_tokens >= len(statement):
                matched_rules.append(rule)
                break  
        if matched_rules:
            print(f"Statement: {statement} matches rules: {matched_rules}")
            # Compare statement with tokens in matched_rules
            for token in statement:
                if token not in correct_tokens:
                    missing_tokens.append(token)
            
            # Add your further processing logic here
        else:
            print(f"Statement: {statement} doesn't match any rule")
        for terminal in rule:
            if terminal not in tokens  and not any(re.match(terminal, token) for token in tokens):
                missing_tokens.append(terminal)
        print("Missing tokens:", missing_tokens)
        print("Misplaced tokens:", misplaced_tokens)

          
    

        # for terminal in statement:
            # if isinstance(terminal, list):  # Handle nested arrays
            #     missing_nonterminals = analyze_syntax(tokens, terminal)
            #     if missing_nonterminals is not True:
            #         missing_tokens.extend(missing_nonterminals)
            # if isinstance(terminal, str) and terminal.startswith("^"):  # Check for regex patterns
            #     regex = re.compile(terminal[1:])
            #     found_match = False
            #     for sub_item in tokens:
            #         if regex.match(sub_item):
            #             found_match = True
            #             break
            #     if not found_match:
            #         missing_tokens.append(terminal)
            # if terminal not in tokens:
            #     print(terminal)
            #     missing_tokens.append(terminal)
                
        

    # for terminal in grammar_rules:
    #     # if isinstance(terminal, list):  # Handle nested arrays
    #     #     missing_nonterminals = has_all_items(tokens, terminal)
    #     #     if missing_nonterminals is not True:
    #     #         missing_tokens.extend(missing_nonterminals)
    #     if isinstance(terminal, str) and terminal.startswith("^"):  # Check for regex patterns
    #         regex = re.compile(terminal[1:])
    #         found_match = False
    #         for sub_item in tokens:
    #             if regex.match(sub_item):
    #                 found_match = True
    #                 break
    #         if not found_match:
    #             missing_tokens.append(terminal)
    #     elif terminal not in tokens:
    #         missing_tokens.append(terminal)
        
                    
    print(grammar_index)
    return missing_tokens
# , grammar_index

LITERAL = r"^LIT_(STRING|INT|FLOAT|BOOL)$"
LIST = r"LITERAL"
GRAMMAR_RULES = [["NW", "DT_MOD", "ID", "COULD_KW", "ONLY_KW", "BE_KW", LITERAL, "DELIM_NEWLINE"],
                 ["LET_KW", "ID", "BE_KW", LITERAL, "DELIM_NEWLINE"]]

missing_items = analyze_syntax(TOKEN_NAMES, GRAMMAR_RULES)
# print(token_index)
# if not missing_items:
#     print("correct syntax")
# else:
#     print("You are missing the following keywords")
#     for item in missing_items:
#         print("\t" + item)

# def find_insertion_index(unsorted_list):
#     """
#     Finds the index where an item should be inserted in an unsorted list to maintain sorted order.

#     Args:
#         unsorted_list: A list of unsorted elements.

#     Returns:
#         The index where the item should be inserted.
#     """

#     if len(unsorted_list) <= 1:
#         return 0

#     for i in range(1, len(unsorted_list)):
#         if unsorted_list[i] < unsorted_list[i - 1]:
#             return i

#     # If the item is larger than all elements, return the end of the list
#     return len(unsorted_list)

# insertion_index = find_insertion_index(token_index)
# print(f"{GRAMMAR_RULES[insertion_index]} must be inserted after {lexemes[insertion_index]}")






