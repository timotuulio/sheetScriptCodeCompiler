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
    p[0] = Node("program")
    p[0].children_funcs_vars = [ ]
    p[0].child_expr = p[1]

def p_program2(p):
    '''program : function_or_variable_definition program'''
    p[0] = p[2]
    p[0].children_funcs_vars.insert(0, p[1])

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
    p[0] = Node('sheet definition')
    p[0].child_name = Node('SHEET_IDENT')
    p[0].child_name.value = p[2]
    if (len(p) > 3):
        p[0].child_init = p[3]
    else:
        p[0].child_init = Node('NONE')

def p_sheet_init(p):
    '''sheet_init : EQ INT_LITERAL MULT INT_LITERAL
                  | EQ sheet_init_list'''
    if (len(p) > 3):
        p[0] = Node('sheet init')
        p[0].value = [p[2], p[4]]
    else:
        p[0] = p[2]

def p_sheet_init_list(p):
    '''sheet_init_list : LCURLY sheet_init_list2'''
    p[0] = p[2]

def p_sheet_init_list2a(p):
    '''sheet_init_list2 : sheet_row sheet_init_list2'''
    p[0] = p[2]
    p[0].children_row.insert(0, p[1])

def p_sheet_init_list2b(p):
    '''sheet_init_list2 : sheet_row sheet_init_list3'''
    p[0] = Node("Sheet_init_list")
    p[0].children_row = [ p[1] ]

def p_sheet_init_list3(p):
    '''sheet_init_list3 : RCURLY'''

def p_sheet_row(p):
    '''sheet_row : simple_expr
                 | simple_expr COMMA sheet_row'''
    p[0] = Node('sheet row')
    if (len(p) > 2):
        p[0] = p[3]
        p[0].children_column.insert(0, p[1])
    else:
        p[0].children_column = [ p[1] ]

def p_range_definition(p):
    '''range_definition : RANGE RANGE_IDENT
                        | RANGE RANGE_IDENT EQ range_expr'''
    p[0] = Node('range definition')
    p[0].value = p[2]
    p[0].child_name = Node('RANGE_IDENT')
    p[0].child_name.value = p[2]
    if (len(p) > 3):
        p[0].child_init = p[4]
    else:
        p[0].child_init = Node('NONE')

def p_range_expr(p):
    '''range_expr : RANGE_IDENT
                  | RANGE cell_ref DOTDOT cell_ref
                  | LSQUARE function_call RSQUARE
                  | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''
    p[0] = Node('range expr')
    if(len(p) == 2):
        p[0].value = p[1]
    elif (len(p) == 4):
        p[0].child_expr = p[2]
    elif(len(p) == 5):
        p[0].child_coord1 = p[2]
        p[0].child_coord2 = p[4]
    else:
        p[0].value = [ p[3], p[5] ]
        p[0].child_expr = p[1]

def p_range_list(p):
    '''range_list : range_expr
                  | range_list COMMA range_expr'''
    if (len(p) == 2):
        p[0] = Node('range list')
        p[0].children_range_list = [ p[1] ]
    else:
        p[0] = p[1]
        #Täs on jotain outoo, näin se tulostaa noi ranget oikeeseen järjestykseen
        # mutta järki sanoo että se tekis ton näin väärinpäin... Kattoo
        # jos tää aiheuttaa ongelmia myöhemmin :/
        p[0].children_range_list.insert(len(p[0].children_range_list), p[3])

def p_scalar_definition(p):
    '''scalar_definition : SCALAR IDENT
                         | SCALAR IDENT EQ scalar_expr'''
    p[0] = Node('scalar definition')
    p[0].child_name = Node('IDENT')
    p[0].child_name.value = p[2]
    if (len(p) > 3):
        p[0].child_init = p[4]
    else:
        p[0].child_init = Node('NONE')

def p_scalar_expr(p):
    '''scalar_expr : simple_expr
                   | scalar_expr EQ simple_expr
                   | scalar_expr NOTEQ simple_expr
                   | scalar_expr LT simple_expr
                   | scalar_expr LTEQ simple_expr
                   | scalar_expr GT simple_expr
                   | scalar_expr GTEQ simple_expr'''
    if(len(p) > 2):
        p[0] = Node('oper ' + p[2])
        p[0].child_left = p[1]
        p[0].child_right = p[3]
    else:
        p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''
    if (len(p) == 2):
        p[0] = Node("Statement list")
        p[0].children_statement_list = [ p[1] ]
    else:
        p[0] = p[2]
        p[0].children_statement_list.insert(0, p[1])

def p_statement(p):
    '''statement : statement1
                 | statement2'''
    p[0] = p[1]

def p_statement1a(p):
    '''statement1 : IF scalar_expr THEN statement_list ELSE statement_list ENDIF
                  | IF scalar_expr THEN statement_list ENDIF
                  | WHILE scalar_expr DO statement_list DONE
                  | FOR range_list DO statement_list DONE
                  | RETURN scalar_expr
                  | RETURN range_expr'''
    p[0] = Node('statement')
    if (len(p) == 3):
        p[0].child_return = p[2]
    elif(len(p) == 4):
        p[0].value = p[1]
        p[0].child_infostring = Node('infostring')
        p[0].child_infostring.value = p[2]
        p[0].child_print = p[3]
    elif(len(p) == 6):
        p[0].value = p[1]
        p[0].child_loop = p[2]
        p[0].child_do = p[4]
    else:
        p[0].value = p[1]
        p[0].child_condition = p[2]
        p[0].child_then = p[4]
        p[0].child_else = p[6]

def p_statement1b(p):
    '''statement1 : PRINT_SHEET SHEET_IDENT
                  | PRINT_SHEET INFO_STRING SHEET_IDENT'''
    p[0] = Node('print sheet')
    if (len(p) == 3):
        p[0].child_name = Node(p[2])
    else:
        p[0].child_infostring = Node('infostring')
        p[0].child_infostring.value = p[2]
        p[0].child_name = Node(p[3])

def p_statement1c(p):
    '''statement1 : PRINT_RANGE INFO_STRING range_expr
                  | PRINT_RANGE range_expr'''
    p[0] = Node('print range')
    if (len(p) == 3):
        p[0].child_name = p[2]
    else:
        p[0].child_infostring = Node('infostring')
        p[0].child_infostring.value = p[2]
        p[0].child_name = p[3]

def p_statement1d(p):
    '''statement1 : PRINT_SCALAR INFO_STRING scalar_expr
                  | PRINT_SCALAR scalar_expr'''
    p[0] = Node('print scalar')
    if (len(p) == 3):
        p[0].child_name = p[2]
    else:
        p[0].child_infostring = Node('infostring')
        p[0].child_infostring.value = p[2]
        p[0].child_name = p[3]

def p_statement2(p):
    '''statement2 : subroutine_call
                  | assignment'''
    p[0] = p[1]

def p_cell_ref(p):
    '''cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR
                | DOLLAR COLON RANGE_IDENT'''
    p[0] = Node('cell ref')
    if (len(p) == 2):
        p[0].value = 'NONE'
    else:
        p[0].value = [ p[1], p[2], p[3] ]

def p_simple_expr(p):
    '''simple_expr : term
                   | simple_expr MINUS term
                   | simple_expr PLUS term'''
    if (len(p) > 2):
        p[0] = Node('oper ' + p[2])
        p[0].child_left = p[1]
        p[0].child_right = p[3]
    else:
        p[0] = p[1]

def p_term(p):
    '''term : factor
            | term MULT factor
            | term DIV factor'''
    if (len(p) > 2):
        p[0] = Node('oper ' + p[2])
        p[0].child_left = p[1]
        p[0].child_right = p[3]
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : atom
              | MINUS atom'''
    if (len(p) > 2):
        #Pitäisköhän toi muuttaa factorin sijaan joksikin "minus" tjm
        #tai siis miks toi factor toimii hyvin, vaik ton pitäis tehä uus lapsisolmu?
        p[0] = Node('factor')
        p[0].value = p[1]
        p[0].child_expr = p[2]
    else:
        p[0] = p[1]

def p_atom(p):
    '''atom : atom2
            | atom3'''
    p[0] = p[1]

def p_atom2a(p):
    '''atom2 : DECIMAL_LITERAL'''
    p[0] = Node('decimal number')
    p[0].value = p[1]

def p_atom2b(p):
    '''atom2 : IDENT'''
    p[0] = Node('IDENT')
    p[0].value = p[1]

def p_atom3(p):
    '''atom3 : function_call
             | cell_ref
             | NUMBER_SIGN range_expr
             | LPAREN scalar_expr RPAREN'''
    if (len(p) > 2):
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_assignment(p):
    '''assignment : assignment2
                  | assignment3'''
    p[0] = p[1]

def p_assignment2a(p):
    '''assignment2 : IDENT ASSIGN scalar_expr'''
    p[0] = Node('scalar assign')
    p[0].child_name = Node('ASSIDENT')
    p[0].child_name.value = p[1]
    p[0].child_assign_value = p[3]

def p_assignment2b(p):
    '''assignment2 : SHEET_IDENT ASSIGN SHEET_IDENT'''
    p[0] = Node('sheet assign')
    p[0].child_name = Node(p[1])
    p[0].child_assign_value = Node(p[3])

def p_assignment2c(p):
    '''assignment2 : RANGE_IDENT ASSIGN range_expr'''
    p[0] = Node('range assign')
    p[0].child_name = Node(p[1])
    p[0].child_assign_value = p[3]

def p_assignment3(p):
    '''assignment3 : cell_ref ASSIGN scalar_expr'''
    p[0] = Node('cell assign')
    p[0].child_left = p[1]
    p[0].child_right = p[3]

def p_function_definition(p):
    '''function_definition : FUNCTION FUNC_IDENT LSQUARE function_definition2
                           | FUNCTION FUNC_IDENT LSQUARE formals function_definition2'''
    p[0] = Node('function definition')
    p[0].child_name = Node('FUNC_IDENT')
    p[0].child_name.value = p[2]
    if(len(p) == 5):
        p[0].child_expr = p[4]
    else:
        p[0].child_formals = p[4]
        p[0].child_content = p[5]

def p_function_definition2(p):
    '''function_definition2 : RSQUARE RETURN SCALAR IS function_definition3
                            | RSQUARE RETURN RANGE IS function_definition3'''
    p[0] = p[5]

def p_function_definition3(p):
    '''function_definition3 : function_definition4
                            | variable_definition function_definition3'''
    if (len(p) == 2):
        p[0] = Node("function variables")
        p[0].children_function_variable = [ ]
        p[0].child_statement_list = p[1]
    else:
        p[0] = p[2]
        p[0].children_function_variable.insert(0, p[1])

def p_function_definition4(p):
    '''function_definition4 : statement_list END'''
    p[0] = p[1]

def p_formals(p):
    '''formals : formal_arg
               | formal_arg COMMA formals'''
    if (len(p) == 2):
        p[0] = Node("Formals")
        p[0].children_formal_list = [ p[1] ]
    else:
        p[0] = p[3]
        p[0].children_formal_list.insert(0, p[1])

def p_formal_arg1(p):
    '''formal_arg : IDENT COLON SCALAR'''
    p[0] = Node('IDENT')
    p[0].value = p[1]

def p_formal_arg2(p):
    '''formal_arg : RANGE_IDENT COLON RANGE'''
    p[0] = Node('RANGE_IDENT')
    p[0].value = p[1]

def p_formal_arg3(p):
    '''formal_arg : SHEET_IDENT COLON SHEET'''
    p[0] = Node('SHEET_IDENT')
    p[0].value = p[1]

def p_function_call(p):
    '''function_call : FUNC_IDENT LSQUARE RSQUARE
                     | FUNC_IDENT LSQUARE arguments RSQUARE'''
    p[0] = Node('function call')
    p[0].child_name = Node(p[1])
    if(len(p) > 4):
        p[0].child_expr = p[3]

def p_subroutine_definition(p):
    '''subroutine_definition : SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS subroutine_definition2
                             | SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS subroutine_definition2'''
    p[0] = Node('subroutine definition')
    p[0].child_name = Node('SUBROUT_IDENT')
    p[0].child_name.value = p[2]
    #p[0].child_name = Node(p[2])
    if(len(p) == 7):
        p[0].child_content = p[6]
    else:
        p[0].child_formals = p[4]
        p[0].child_content = p[7]

def p_subroutine_definition2(p):
    '''subroutine_definition2 : subroutine_definition3
                              | variable_definition subroutine_definition2'''
    if (len(p) == 2):
        p[0] = Node("subroutine variables")
        p[0].children_subroutine_variable = []
        p[0].child_statements = p[1]
    else:
        p[0] = p[2]
        p[0].children_subroutine_variable.insert(0, p[1])

def p_subroutine_definition3(p):
    '''subroutine_definition3 : statement_list END'''
    p[0] = p[1]

def p_subroutine_call(p):
    '''subroutine_call : FUNC_IDENT LSQUARE RSQUARE
                       | FUNC_IDENT LSQUARE arguments RSQUARE'''
    p[0] = Node('subroutine call')
    p[0].child_name = Node(p[1])
    if(len(p) > 4):
        p[0].child_arguments = p[3]

def p_arguments(p):
    '''arguments : arg_expr
                 | arg_expr COMMA arguments'''
    if (len(p) == 2):
        p[0] = Node("arguments")
        p[0].children_argument_list = [ p[1] ]
    else:
        p[0] = p[3]
        p[0].children_argument_list.insert(0, p[1])

def p_arg_expra(p):
    '''arg_expr : range_expr
                | scalar_expr'''
    p[0] = p[1]

def p_arg_exprb(p):
    '''arg_expr : SHEET_IDENT'''
    p[0] = Node('sheet ident')
    p[0].value = p[1]

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
        print( '415428 Timo Tuulio' )
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)
        # Pretty print the resulting tree
        tree_print.treeprint(result, outformat)
