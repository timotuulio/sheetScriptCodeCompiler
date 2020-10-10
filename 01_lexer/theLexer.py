import ply.lex as lex
import sys as sys

reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'sheet' : 'SHEET',
    'scalar' : 'SCALAR',
    'range' : 'RANGE',
    'do' : 'DO',
    'done' : 'DONE',
    'is' : 'IS',
    'for' : 'FOR',
    'endif' : 'ENDIF',
    'function' : 'FUNCTION',
    'subroutine' : 'SUBROUTINE',
    'return' : 'RETURN',
    'end' : 'END',
    'print_sheet' : 'PRINT_SHEET',
    'print_scalar' : 'PRINT_SCALAR',
    'print_range' : 'PRINT_RANGE'
 }

# List of token names.   This is always required
tokens = list(reserved.values()) + [
    'ASSIGN',
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'EQ',
    'NOTEQ',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',

    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'LCURLY',
    'RCURLY',

    'COMMA',
    'DOTDOT',
    'SQUOTE',
    'COLON',
    'DOLLAR',
    'NUMBER_SIGN',
    'IDENT',
    'INFO_STRING',
    'COORDINATE_IDENT',
    'DECIMAL_LITERAL',
    'INT_LITERAL',
    'RANGE_IDENT',
    'SHEET_IDENT',
    'FUNC_IDENT'
]

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_EQ = r'='
t_NOTEQ = r'!='
t_LT = r'<'
t_LTEQ = r'<='
t_GT = r'>'
t_GTEQ = r'>='

t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r','
t_DOTDOT = r'\.\.'
t_SQUOTE = r"'"
t_COLON = r':'
t_DOLLAR = r'\$'
t_NUMBER_SIGN = r'\#'
#t_EXLAMATION_MARK = r'!'

def t_comment(t):
    r'\.\.\..*\.\.\.'
    pass

def t_RANGE_IDENT(t):
    r'_[a-zA-Z_\d]+'
    return t

def t_DECIMAL_LITERAL(t):
    r'-?\d+\.\d'
    t.type = reserved.get(t.value, 'DECIMAL_LITERAL')
    return t

def t_INT_LITERAL(t):
    r'-?\d+'
    t.type = reserved.get(t.value, 'INT_LITERAL')
    return t

def t_INFO_STRING(t):
    r'!.*!'
    t.type = reserved.get(t.value, 'INFO_STRING')
    return t

def t_COORDINATE_IDENT(t):
    r'[A-Z]{1,2}\d{1,3}'
    t.type = reserved.get(t.value, 'COORDINATE_IDENT')
    return t

def t_FUNC_IDENT(t):
    r'[A-Z][a-z0-9]+'
    t.type = reserved.get(t.value, 'FUNC_IDENT')
    return t

def t_SHEET_IDENT(t):
    r'[A-Z]+'
    return t

def t_IDENT(t):
    r'[a-z][a-zA-Z_0-9]+'
    t.type = reserved.get(t.value, 'IDENT')  # Check for reserved words
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s' on line " % t.value[0], t.lexer.lineno)
    sys.exit()

# Build the lexer
lexer = lex.lex()

# Test it out
with open('text.txt', 'r', encoding='utf-8') as INFILE:
    data3 = INFILE.read()

data2 = '''
3 + 4 * 10 ) [ ] }
  + -20 *2 { :=
  , ' : $ # = != < <= > >= ..
  end if while then endif end 
  48 /*print_range
   2222*/ if
    50000 ... testei asd 23 ...
  38 !merkkijono! mottonen Metri
  A110 AS1
  12.3
  if
'''

#-f text.txt
#-h
#--who
if __name__ == '__main__':
    import argparse, codecs
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')

    ns = parser.parse_args()
    if ns.who == True:
        print('415428 Timo Tuulio')
    elif ns.file is None:
        parser.print_help()
    else:
        # using codecs to make sure we process unicode
        # Also give the lexer some input
        with codecs.open(ns.file, 'r', encoding='utf-8') as INFILE:
            data = INFILE.read()
        lexer.input(data)
        # Tokenize
        while True:
            tok = lexer.token()
            if not tok:
                break  # No more input
            print(tok)
