Run the main file with argument for the sheetscript-filename. There are two examples for sheetscript added in project (animals.ss and subFuncDef.ss).
For example:
$ python main.py -f "animals.ss"

The code prints out the syntax tree, then prints out any print clauses there is written in the code that is compiled. Lastly all the variables in the variable table are printed out.

This part of the project is where a sheetscript-file (fileName.ss) is read, compiled and ran. The program first recognizes the tokens, "words" that the file has, then checks that there are no syntax errors. A syntax tree is printed which shows how the code is constructed. Finally a semantic check is made and the code is run.

The code is not fully completed and only the following semantic checks and interpretations have been implemented:

- Variables, functions and subfunctions need to be defined before use and the names need to be unique. Otherwise an error will occur.

- Range expression of style SS'A1 .. SS'A5 checks that both values refer to the same sheet and that the range is either vertical or horizontal. (This means that expressions like "SS2'A1 .. SS1'A5" or "SS'A1 .. SS'B5" result in an error)

- Each row in a sheet initialization has to have same number of columns.

- Expressions with arithmetic expressions, decimal literals and print_scalar are evaluated.

- Scalar variables can be defined, assigned and read
