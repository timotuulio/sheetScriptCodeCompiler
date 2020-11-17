from ply import yacc
import lexer
import tree_print

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = lexer.tokens

class Node:
  def __init__(self, typestr):
    self.nodetype = typestr

# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors
def p_program1(p):
    '''program : statement_list'''
    print('-------------------')
    p[0] = Node("program")
    p[0].children_assigns = [ p[1] ]
    #p[0].child_expr = p[1]
    #if (len(p) > 2):
    #    p[0].child_rest = p[2]

def p_program2(p):
    '''program : function_or_variable_definition program'''
    p[0] = p[2]
    p[0].children_assigns.append(p[1])

def p_function_or_variable_definition1(p):
    '''function_or_variable_definition : variable_definition
                                       | function_definition
                                       | subroutine_definition'''
    p[0] = p[1]

def p_variable_definition(p):
    '''variable_definition : sheet_definition
                           | range_definition
                           | scalar_definition'''
    p[0] = p[1]

def p_sheet_definition(p):
    '''sheet_definition : SHEET SHEET_IDENT sheet_init
                        | SHEET SHEET_IDENT'''
    print('variable definition(', p[2], ': Sheet)')
    p[0] = Node('sheet definition')
    p[0].value = p[2]
    if (len(p) > 2):
        p[0].child_expr = p[3]

def p_sheet_init(p):
    '''sheet_init : EQ INT_LITERAL MULT INT_LITERAL
                  | EQ sheet_init_list'''
    p[0] = Node('sheet init')
    #p[0].value = p[0]
    if (len(p) > 3):
        p[0].value = p[3]
    else:
        p[0].child_expr = p[2]

def p_sheet_init_list(p):
    '''sheet_init_list : LCURLY sheet_row sheet_init_list2'''
    p[0] = Node('sheet init list')
    p[0].value = p[0]
    p[0].child_left = p[2]
    p[0].child_right = p[3]

def p_sheet_init_list2(p):
    '''sheet_init_list2 : sheet_row sheet_init_list2
                        | RCURLY'''
    #Onko tähän järkee laittaa kahta sheet init listiä, olisko mahollista saada sitä kaikkee yhteen?
    p[0] = Node('sheet init list2')
    if(len(p) > 1):
        p[0].child_expr = p[1]

def p_sheet_row(p):
    '''sheet_row : simple_expr
                 | simple_expr COMMA sheet_row'''
    p[0] = Node('sheet row')
    #p[0].value = p[0]
    if (len(p) > 2):
        p[0].child_left = p[1]
        p[0].child_right = p[3]
    else:
        p[0].child_expr = p[1]


def p_range_definition(p):
    '''range_definition : RANGE RANGE_IDENT
                        | RANGE RANGE_IDENT EQ range_expr'''
    print('variable definition(', p[2], ': Range)')
    p[0] = Node('range definition')
    if (len(p) > 3):
        p[0].value = p[2]
    else:
        p[0].value = p[2]
        p[0].child_expr = p[4]

def p_range_expr(p):
    '''range_expr : RANGE_IDENT
                  | RANGE cell_ref DOTDOT cell_ref
                  | LSQUARE function_call RSQUARE
                  | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''
    p[0] = Node('range expr')
    #TODO Tänne tarttee jotain höttöö paljon, et mikä on mitenkäkin
    p[0].value = p[1]

def p_range_list(p):
    '''range_list : range_expr
                  | range_expr COMMA range_list'''
    p[0] = Node('range list')
    p[0].value = p[0]
    if (len(p) > 1):
        p[0].child_left = p[1]
        p[0].child_right = p[3]
    else:
        p[0].child_expr = p[1]

def p_scalar_definition(p):
    '''scalar_definition : SCALAR IDENT
                         | SCALAR IDENT EQ scalar_expr'''
    print('variable definition(', p[2], ': Scalar)')
    p[0] = Node('scalar definition')
    p[0].value = p[2]
    if (len(p) > 2):
        p[0].child_expr = p[4]

def p_scalar_expr(p):
    '''scalar_expr : simple_expr scalar_expr2'''
    print('scalar_expr')
    p[0] = Node('scalar expr')
    #p[0].value = p[0]
    p[0].child_left = p[1]
    p[0].child_right = p[2]


def p_scalar_expr2(p):
    '''scalar_expr2 : empty
                    | scalar_expr2 scalar_expr3'''
    if (len(p) > 2):
        p[0] = Node('scalar expr 2')
        p[0].child_left = p[1]
        p[0].child_right = p[2]

def p_scalar_expr3(p):
    '''scalar_expr3 : EQ simple_expr
                    | NOTEQ simple_expr
                    | LT simple_expr
                    | LTEQ simple_expr
                    | GT simple_expr
                    | GTEQ simple_expr'''
    p[0] = Node("oper " + p[1])
    p[0].value = p[1]
    p[0].child_expr = p[2]


def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''
    p[0] = Node('Statement list')
    if (len(p) > 2):
        p[0].child_left = p[1]
        p[0].child_right = p[2]
    else:
        p[0].child_expr = p[1]


def p_statement(p):
    '''statement : statement1
                 | statement2'''
    p[0] = p[1]

def p_statement1(p):
    '''statement1 : PRINT_SHEET INFO_STRING SHEET_IDENT
                  | PRINT_SHEET SHEET_IDENT
                  | PRINT_RANGE INFO_STRING range_expr
                  | PRINT_RANGE range_expr
                  | PRINT_SCALAR INFO_STRING scalar_expr
                  | PRINT_SCALAR scalar_expr
                  | IF scalar_expr THEN statement_list ELSE statement_list ENDIF
                  | IF scalar_expr THEN statement_list ENDIF
                  | WHILE scalar_expr DO statement_list DONE
                  | FOR range_list DO statement_list DONE
                  | RETURN scalar_expr
                  | RETURN range_expr'''
    print('statement: ', p[1])

def p_statement2(p):
    '''statement2 : subroutine_call
                  | assignment'''

def p_cell_ref(p):
    '''cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR
                | DOLLAR COLON RANGE_IDENT'''
    p[0] = Node('cell ref')
    #Tää pitää muuttaa viel, ja kattoo et mitä toi ny oikeen ottaa tonne
    p[0].value = p[1]

def p_simple_expr(p):
    '''simple_expr : term simple_expr2'''
    p[0] = Node('simple expr')
    p[0].child_left = p[1]
    p[0].child_right = p[2]

def p_simple_expr2(p):
    '''simple_expr2 : empty
                    | PLUS term simple_expr2
                    | MINUS term simple_expr2'''
    if (len(p) > 2):
        p[0] = Node('simple expr')
        p[0].value = p[1]
        p[0].child_left = p[2]
        p[0].child_right = p[3]

def p_term(p):
    '''term : factor term2'''
    print('term')
    p[0] = Node('term')
    p[0].child_left = p[1]
    p[0].child_right = p[2]

def p_term2(p):
    '''term2 : empty
             | MULT factor term2
             | DIV factor term2'''
    if (len(p) > 2):
        p[0] = Node('term')
        p[0].value = p[1]
        p[0].child_left = p[2]
        p[0].child_right = p[3]

def p_factor(p):
    '''factor : atom
              | MINUS atom'''
    print('factor')
    p[0] = Node('factor')
    if (len(p) > 2):
        p[0].child_expr = p[2]
    else:
        p[0].child_expr = p[1]

def p_atom(p):
    '''atom : atom2
            | atom3'''
    p[0] = p[1]

def p_atom2(p):
    '''atom2 : IDENT
             | DECIMAL_LITERAL'''
    print('atom: ', p[1])
    p[0] = Node('atom')
    p[0].value = p[1]

def p_atom3(p):
    '''atom3 : function_call
             | cell_ref
             | NUMBER_SIGN range_expr
             | LPAREN scalar_expr RPAREN'''
    print('atom')

def p_assignment(p):
    '''assignment : assignment2
                  | assignment3'''

def p_assignment2(p):
    '''assignment2 : IDENT ASSIGN scalar_expr
                   | RANGE_IDENT ASSIGN range_expr
                   | SHEET_IDENT ASSIGN SHEET_IDENT'''
    print('assignment: ', p[1])

def p_assignment3(p):
    '''assignment3 : cell_ref ASSIGN scalar_expr'''

def p_function_definition(p):
    '''function_definition : FUNCTION FUNC_IDENT LSQUARE function_definition2
                           | FUNCTION FUNC_IDENT LSQUARE formals function_definition2'''
    print('function definition: ', p[2])

def p_function_definition2(p):
    '''function_definition2 : RSQUARE RETURN SCALAR IS function_definition3
                            | RSQUARE RETURN RANGE IS function_definition3'''

def p_function_definition3(p):
    '''function_definition3 : function_definition4
                            | variable_definition function_definition3'''

def p_function_definition4(p):
    '''function_definition4 : statement_list END'''
    print('function definition: ', p[1])

def p_formals(p):
    '''formals : formal_arg
               | formal_arg COMMA formals'''

def p_formal_arg(p):
    '''formal_arg : IDENT COLON SCALAR
                  | RANGE_IDENT COLON RANGE
                  | SHEET_IDENT COLON SHEET'''
    print('formal arguments: ', p[1])

def p_function_call(p):
    '''function_call : FUNC_IDENT LSQUARE RSQUARE
                     | FUNC_IDENT LSQUARE arguments RSQUARE'''
    print('function call: ', p[1])

def p_subroutine_definition(p):
    '''subroutine_definition : SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS subroutine_definition2
                             | SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS subroutine_definition2'''
    print('subroutine definition: ', p[2])

def p_subroutine_definition2(p):
    '''subroutine_definition2 : subroutine_definition3
                              | variable_definition subroutine_definition2'''

def p_subroutine_definition3(p):
    '''subroutine_definition3 : statement_list END'''

def p_subroutine_call(p):
    '''subroutine_call : FUNC_IDENT LSQUARE RSQUARE
                       | FUNC_IDENT LSQUARE arguments RSQUARE'''
    print('subroutine call: ', p[1])

def p_arguments(p):
    '''arguments : arg_expr
                 | arg_expr COMMA arguments'''

def p_arg_expr(p):
    '''arg_expr : SHEET_IDENT
                | range_expr
                | scalar_expr'''

def p_empty(p):
    'empty :'
    pass

# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print( 'syntax error @', p )
    raise SystemExit

parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()

    outformat="unicode"
    if ns.treetype:
      outformat = ns.treetype

    if ns.who == True:
        # identify who wrote this
        print( '88888 Ahto Simakuutio' )
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)
        # Pretty print the resulting tree
        tree_print.treeprint(result, outformat)
