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
import tokenize
import io
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_comments(string, comment_pattern):
    comments = re.findall(comment_pattern, string)
    stripped_string = re.sub(comment_pattern, "", string)
    return stripped_string

import tokenize
import io

# test code
code = """A Score could only be show\nA score could only be 8"""
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
                
              print(f"{count:<2}|  {'--':<10}\t|  {token_name:<10}")
              TOKEN_NAMES.append(token_name)
              count+=1
              break

            print(f"{count:<2}|  {lexeme:<10}\t|  {token_name:<10}")
            TOKEN_NAMES.append(token_name)
            count+=1
            break  # Stop after first match (if needed)

import re

def split_tokens_into_statements(tokens, delim):
    statements = []
    current_statement = []

    for token in tokens:
        if token == delim:
            statements.append(current_statement)
            current_statement = []
        else:
            current_statement.append(token)

    # Add the last statement if it doesn't end with a newline
    if current_statement:
        statements.append(current_statement)

    return statements

def analyze_syntax(lexemes, token_pattern_dict, tokens, grammar_rules):
    
    code = split_tokens_into_statements(lexemes, "\n")
    statements = split_tokens_into_statements(tokens, "DELIM_NEWLINE")
    
    for statement in statements:
                
        misplaced_tokens = []
        misplaced_indices = []
        missing_tokens = []
        missing_indices = []
        grammar_index = []

        correct_tokens = []
        matched_rules = []
        

        print("") 
        for rule in grammar_rules:
            correct_tokens.clear()
            missing_tokens.clear()
            missing_indices.clear()
            misplaced_indices.clear()
            misplaced_tokens.clear()
            grammar_index.clear()    

            num_matched_tokens = 0
            num_unmatched_tokens = 0

            # COUNT NUMBER OF MATCHED TOKENS BETWEEN STATEMENT AND RULE
            for token in statement:
                if token in rule:
                    num_matched_tokens += 1
                elif any(re.match(terminal, token) for terminal in rule if isinstance(terminal, str) and terminal.startswith("^")):
                    num_matched_tokens += 1
                else:
                    num_unmatched_tokens += 1
            
            # IF THERE ARE MORE MATCHES THAN UNMATCHED 
            # THEN STATEMENT MATCHES RULES
            isMatched = False
            if num_matched_tokens > num_unmatched_tokens:
                # print("matches ", rule)
                isMatched = True
            
            # STORE MATCHED RULE
            matched_rule = []
            if isMatched == True:
                for token in rule:
                    matched_rule.append(token)
            
            
            if isMatched == True:
                # CHECK IF THERE ARE MISPLACED TOKENS
                for token in statement:
                    token_has_regex = False
                    for word in matched_rule:
                        if token == word:
                            correct_tokens.append(token)
                        elif isinstance(word, str) and word.startswith("^"):
                            if re.match(word, token):
                                correct_tokens.append(token)
                                token_has_regex = True  
                    if token not in matched_rule and not token_has_regex:
                        misplaced_tokens.append(token)
                        misplaced_indices.append(statement.index(token))
                        # if len(misplaced_tokens) > 0:
                        #     print("Misplaced Tokens"+ token)
                
                # print("Correct Tokens", correct_tokens)
                # print("Misplaced Tokens", misplaced_tokens)

                 # CHECK FOR MISSING TOKENS
                for word in matched_rule:
                    if word not in statement and not any(re.match(token, word) for token in statement):
                        missing_tokens.append(word)
                        missing_indices.append(matched_rule.index(word))
                        # print("Missing keyword "+ word)
                
                # CHECK FOR ORDER OF TOKENS
                for token in statement:
                    token_has_regex = False
                    for word in matched_rule:
                        if token == word:
                            index = matched_rule.index(token)
                            grammar_index.append(index)
                        elif isinstance(word, str) and word.startswith("^"):
                            if re.match(word, token):
                                index = rule.index(next(terminal for terminal in rule if re.match(terminal, token)))
                                grammar_index.append(index)
                                token_has_regex = True
                    if token not in matched_rule and not token_has_regex:
                        grammar_index.append(404)
                
                if grammar_index:
                    unsorted_index = []
                    for i in range(len(grammar_index) - 1):
                        if grammar_index[i] > grammar_index[i + 1]:
                            unsorted_index.append(i)

                    # print(grammar_index)
                    # print(unsorted_index)
                
                import colorama
                colorama.init()
                
                print(colorama.Fore.RED + "Invalid Syntax:" + colorama.Style.RESET_ALL)
                print("\t", end="")
                spaces = []
                i=0
                for lexeme in lexemes:
                    if lexeme == "\n":
                        break
                    for missing in missing_indices:
                        if missing == i:
                            x = sum(len(word) for word in lexemes[:i+1]) + i
                            spaces.append(x)
                            print(colorama.Fore.RED + "_" + colorama.Style.RESET_ALL, end=" ")
                            break
                    for misplaced in misplaced_indices:
                        if misplaced == i:
                            x = sum(len(word) for word in lexemes[:i+1]) + i
                            spaces.append(x)
                            print(colorama.Fore.RED + lexeme + colorama.Style.RESET_ALL, end=" ")
                            break  # Exit the loop after highlighting a misplaced lexeme
                    
                    else:
                        print(lexeme, end = " ")
                    i+=1
                print("")
                for missing in missing_tokens:
                    for space in spaces:
                        print("\t" + " " * space + colorama.Fore.RED +"^ Missing " + f"{missing}" +  colorama.Style.RESET_ALL)
                
                # print(grammar_index)
                break
                






        #     for token in tokens:
        #         if token in rule:
        #             correct_tokens.append(token)
        #             grammar_index.append(rule.index(token))
        #         elif any(re.match(terminal, token) for terminal in rule if isinstance(terminal, str) and terminal.startswith("^")):
        #             correct_tokens.append(token) 
        #             grammar_index.append(rule.index(next(terminal for terminal in rule if re.match(terminal, token))))
        #         else:
        #             misplaced_indices.append(statement.index(token))
        #             misplaced_tokens.append(token)

        #     if len(correct_tokens) >= len(misplaced_tokens):
        #         print(len(correct_tokens))
        #         print(len(misplaced_tokens))
        #         matched_rules.append(rule)
        #         break  
        # for terminal in rule:
        #     if terminal not in tokens  and not any(re.match(terminal, token) for token in tokens):
        #         missing_tokens.append(terminal)
        #         missing_indices.append(rule.index(terminal))
        # if matched_rules:
        #     print(f"Statement: {statement} matches rules: {matched_rules}")
            
        # else:
        #     print(f"Statement: {statement} doesn't match any rule")
        
        
        
        
        # print("Missing indices: ", missing_indices)
        # print("Missing tokens:", missing_tokens)
        # print("Misplaced indices: ", misplaced_indices)
        # print("Misplaced tokens:", misplaced_tokens)
        # print("Correct tokens:", correct_tokens)
        # colorama.deinit()

          
    

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
        
                    
    # print(grammar_index)
    return missing_tokens
# , grammar_index

LITERAL = r"^LIT_(STRING|INT|FLOAT|BOOL)$"
LIST = r"LITERAL"
GRAMMAR_RULES = [
                 ["LET_KW", "ID", "BE_KW", LITERAL, "DELIM_NEWLINE"],
                 ["NW", "DT_MOD", "ID", "COULD_KW", "ONLY_KW", "BE_KW", LITERAL, "DELIM_NEWLINE"],
                 ["NAME_CONV", "ID", "PREP" , "ID"],
                 ["ACTION", r"^(PTR|ID)"],
                 ["ACTION", LITERAL],
                 ["ID", "REL_OP", LITERAL, "ARITH_OP", LITERAL]]

missing_items = analyze_syntax(lexemes, token_pattern_dict, TOKEN_NAMES, GRAMMAR_RULES)
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






