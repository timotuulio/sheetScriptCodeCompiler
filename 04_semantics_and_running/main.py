from semantics_common import visit_tree, SymbolData, SemData


import sys
import lexer
import syntax
parser = syntax.parser
import tree_print
import semantics_check

import re


def run_program(tree, semdata):
    # Initialize all variables to zero
    for symdata in semdata.symtbl.values():
        if symdata.symtype == 'var':
            symdata.value = 0
    eval_node(tree, semdata) # Do the actual execution

def eval_node(node, semdata):
    symtbl = semdata.symtbl
    nodetype = node.nodetype
    if nodetype == 'program':
        # Execute each assignment in program
        for i in node.children_funcs_vars:
            eval_node(i, semdata)
        # Execute each statement in program
        # The naming convention is bit sloppy here, but what's you gonna do
        for i in node.child_expr.children_statement_list:
            eval_node(i, semdata)
        return None
        """elif nodetype == 'number':
        # Return the value of the number as result
        return node.value
    elif nodetype == 'variable':
        # Return the value of the variable in symboldata as result
        return node.symdata.value
    elif nodetype == 'assign':
        # Execute the expression
        expr_value = eval_node(node.child_expr, semdata)
        # Change the value of the variable in symbol data
        node.symdata.value = expr_value
        # Print out the assignment
        print(node.value, "=", expr_value)
        return None"""
    elif nodetype == 'oper +':
        # Execute operand expressions
        left_value = eval_node(node.child_left, semdata)
        right_value = eval_node(node.child_right, semdata)
        # Calculate and return the result
        result = left_value + right_value
        return result
    elif nodetype == 'oper -':
        # Execute operand expressions
        left_value = eval_node(node.child_left, semdata)
        right_value = eval_node(node.child_right, semdata)
        # Calculate and return the result
        result = left_value - right_value
        return result
    elif nodetype == 'oper *':
        # Execute operand expressions
        left_value = eval_node(node.child_left, semdata)
        right_value = eval_node(node.child_right, semdata)
        # Calculate and return the result
        result = left_value * right_value
        return result
    elif nodetype == 'oper /':
        # Execute operand expressions
        left_value = eval_node(node.child_left, semdata)
        right_value = eval_node(node.child_right, semdata)
        # Calculate and return the result
        result = left_value / right_value
        return result
    elif nodetype == 'decimal number':
        value = node.value
        return float(value)
    elif nodetype == 'print scalar':
        if hasattr(node.child_name, "value"):
            value = node.child_name.value
        else:
            value = eval_node(node.child_name, semdata)
        print(value)
        return None
    elif nodetype == 'scalar definition' or nodetype == 'sheet definition':
        name = node.child_name.value
        if node.child_init.nodetype == 'decimal number':
            newVal = node.child_init.value
        elif node.child_init.nodetype[0:4] == 'oper':
            newVal = eval_node(node.child_init, semdata)
        else:
            return None
        semdata.symtbl[name].value = newVal
        return None
    elif nodetype == 'range definition':
        name = node.child_name.value
        newVal = eval_node(node.child_init, semdata)
        if newVal[0] == newVal[2]:
            r = re.compile("([a-zA-Z]+)([0-9]+)")
            cell1 = r.match(newVal[1])
            cell2 = r.match(newVal[3])
            chars = cell1.group(1) < cell2.group(1) or len(cell1.group(1)) < len(cell2.group(1))
            numbers = cell1.group(2) < cell2.group(2)
            if chars ^ numbers:
                semdata.symtbl[name].value = newVal
                return None
        return None
    elif nodetype == 'range expr':
        val1 = node.child_coord1.value[0]
        val2 = node.child_coord1.value[2]
        value1 = node.child_coord2.value[0]
        value2 = node.child_coord2.value[2]
        value = [val1, val2, value1, value2]
        return value
    else:
        print("Error, unknown node of type " + nodetype)
        return None


if __name__ == "__main__":
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file', help='filename to process')

    ns = arg_parser.parse_args()

    if ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        ast_tree = parser.parse(data, lexer=lexer.lexer, debug=False)

        semdata = SemData()
        semdata.in_function = None
        semantics_check.semantic_checks(ast_tree, semdata)
        tree_print.treeprint(ast_tree)
        print("Semantics ok.")
        run_program(ast_tree, semdata)
        semantics_check.print_symbol_table(semdata, "Symbol table")
        print("Program finished.")
