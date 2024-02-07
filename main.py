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

# print(code)

import re
def remove_comments(string, comment_pattern):
    comments = re.findall(comment_pattern, string)
    stripped_string = re.sub(comment_pattern, "", string)
    return stripped_string

import tokenize
import io

# test code
code = """A Score could be only \tshow 8"""

# Single-line and multi-line comments
comment_pattern = r"//(.*?)\n|\/\*[\s\S]*?\*\/"
clean_code = remove_comments(code, comment_pattern)
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
                
              print(f"{count:2}\t|\t{' ':10}\t|\t{token_name:10}")
              TOKEN_NAMES.append(token_name)
              count+=1
              break

            print(f"{count:<2}|  {lexeme:<10}\t|  {token_name:<10}")
            TOKEN_NAMES.append(token_name)
            count+=1
            break  # Stop after first match (if needed)

import re

def analyze_syntax(tokens, grammar_rules):
    missing_tokens = []
    misplaced_tokens = []
    correct_tokens = []
    grammar_index = []

    for statement in grammar_rules:
        grammar_index.clear()
        for token in tokens:
            if token in statement:
                correct_tokens.append(token)
                grammar_index.append(statement.index(token))
            if any(re.match(terminal, token) for terminal in statement if isinstance(terminal, str) and terminal.startswith("^")):
                correct_tokens.append(token) 
                grammar_index.append(statement.index(next(terminal for terminal in statement if re.match(terminal, token))))
            if token not in statement:
                misplaced_tokens.append(token)
                print("misplaced: "+token)
        break  
    for terminal in statement:
        if terminal not in tokens  and not any(re.match(terminal, token) for token in tokens):
            print(terminal)
            missing_tokens.append(terminal)
            
    

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
GRAMMAR_RULES = [["NW", "DT_MOD", "ID", "COULD_KW", "ONLY_KW", "BE_KW", LITERAL],
                 ["LET_KW", "ID", "BE_KW", r"^LIT_(STRING|INT|FLOAT|BOOL)$"]]

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






