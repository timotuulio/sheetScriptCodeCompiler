#!/usr/bin/env python3
#

from semantics_common import visit_tree, SymbolData, SemData


# Define semantic check functions


# Collect variables to the symbol table
def add_vars(node, semdata):
    nodetype = node.nodetype
    if (nodetype == 'assign' or nodetype == 'scalar definition'
        or nodetype == 'range definition' or nodetype == 'sheet definition'):
        var_name = node.child_name.value
        if var_name in semdata.symtbl:
            # Variable is already in the symbol table
            return "Error, redefined variable '" + var_name + "'"; # + "' on line " + str(node.lineno)
        else:
            # Add variable to symbol table
            symdata = SymbolData('var', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata  # Add a link to the symbol data to AST node for execution

    elif (nodetype == 'function definition'):
        var_name = node.child_name.value
        if var_name in semdata.symtbl:
            # Variable is already in the symbol table
            return "Error, redefined function '" + var_name + "'"; # + "' on line " + str(node.lineno)
        else:
            # Add variable to symbol table
            symdata = SymbolData('func', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata  # Add a link to the symbol data to AST node for execution
    elif (nodetype == 'subroutine definition'):
        var_name = node.child_name.value
        if var_name in semdata.symtbl:
            # Variable is already in the symbol table
            return "Error, redefined subroutine '" + var_name + "'"; # + "' on line " + str(node.lineno)
        else:
            # Add variable to symbol table
            symdata = SymbolData('subr', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata  # Add a link to the symbol data to AST node for execution

# Check variable use, add link to symbol data
def check_vars(node, semdata):
    nodetype = node.nodetype
    if nodetype == 'variable':
        var_name = node.value
        if not (var_name in semdata.symtbl):
            # Variable is not in the symbol table
            return "Error, undefined variable '" + var_name + "' on line " + str(node.lineno)
        else:
            # Add symbol data link to variable's AST node (for execution)
            node.symdata = semdata.symtbl[var_name]



# Stupid check, make sure all numbers are < 10
def check_literals(node, semdata):
    nodetype = node.nodetype
    if nodetype == 'number':
        if node.value >= 10:
            return "Number " + str(node.value) + " on line " + str(node.lineno) + " too large!"
    else:
        return None

# Another stupid check, only allow less than 3 nested + operations
def check_plus_level_before(node, semdata):
    nodetype = node.nodetype
    if nodetype == 'oper +':
        # We are entering a plus node, increase level
        semdata.plus_level = semdata.plus_level + 1
        if semdata.plus_level > 3:
            return "Error, more than 3 nested plus operations, line " + str(node.lineno)
        else:
            return None


# Another stupid check, only allow less than 4 nested + operations
def check_plus_level_after(node, semdata):
    nodetype = node.nodetype
    if nodetype == 'oper +':
        # We are leaving the plus node, decrease level
        semdata.plus_level = semdata.plus_level - 1
    else:
        return None


# Simple symbol table printer for debugging
def print_symbol_table(semdata, title):
    '''Print the symbol table in semantic data

       Parameters:
       semdata: A SemData data structure containing semantic data
       title: String printed at the beginning
  '''
    print(title)
    for name, data in semdata.symtbl.items():
        print(name, ":")
        for attr, value in vars(data).items():
            printvalue = value
            if hasattr(value, "nodetype"):  # If the value seems to be a ASTnode
                printvalue = value.nodetype
                if hasattr(value, "lineno"):
                    printvalue = printvalue + ", line " + str(value.lineno)
            print("  ", attr, "=", printvalue)


def semantic_checks(tree, semdata):
    '''run all semantic checks'''
    # Initialize 'oper +' level count to 0
    semdata.plus_level = 0
    # Gather information
    visit_tree(tree, add_vars, None, semdata)
    visit_tree(tree, check_vars, None, semdata)
    # Check stupid things
    visit_tree(tree, check_literals, None, semdata)
    visit_tree(tree, check_plus_level_before, check_plus_level_after, semdata)
