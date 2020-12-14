In addition to the code, the group submits a text document in either plain text (.txt), markdown (.md) or pdf (.pdf) format. It should document each semantic check / interpretation level you’ve done, explaining how it works. If you implemented any things of your own, explain them also in the document. Also tell what you thought about this assignment? What was difficult? What was easy? Did you learn anything useful?

Implemented in code:
Semantic checks: 
1. Variables and functions and subfunctions need to be defined before use and the names need to be unique.
- This is done before running the code when doing the semantic check to make the symbol table. If the user tries to add a variable with the same name that already exists, the program gives an error message and crashes. This works with functions and subroutines but they are not implemented later so using them will yield message: "Error, unknown node of type subroutine/function definition"

2. Range expression of style SS'A1 .. SS'A5 checks that both values refer to the same sheet and that the range is either vertical or horizontal.
- Both sheet-coordinates are secured in a table so that the values are easily accessed. The sheet variables are taken apart so that I have both the alphabetical and numerical values. The values of both sheets are compared; if there are more characters or if the character comparison (a < b) returns true, then there has been change in the rows. If the second number is greater than the first, there has been change in the columns. With xor-operator I check that only one of these has been changed. If so, the range definition is added to the symbol table. If not, the range expression gives the value of 0.


3. Each row in a sheet initialization has to have same number of columns.
- When defining a sheet a sheet init list can be given. In this case, I check the length of the first row in the sheet. Then with a for-loop I go through each of the rows and if they have different row length, the function stops and the sheet value is not change (meaning it stays as the default value of 0). If the rows are correctly done the sheet variable becomes a table with each row as a subtable.

Interpretation
4. Evaluating expressions with arithmetic expressions, decimal literals and print_scalar.
- Decimal numbers are interpreted as they are. The arithmetic calculations are done just by evaluating the two children nodes and doing the specific operation with their result. Print_scalar checks it the object to be printed has attribute "value" and if it is in the symbol table and prints that variables value. Else we evaluate the value of the node which interprets it if it is for example an arithmetic operation.

5. Scalar variables can be defined, assigned and read
- The assigned value is interpreted. If it is a decimal number it can be understood directly, a variable must be read from symbol table and arithmetic operation must be calculated. When we have the value, it is taken to the symbol table. When reading it we just find it from the symbol table and take its value.

Thoughts on assignment:
This phase of the assignment was considerably easier than the previous parts. The start was again difficult but this time just reading the example code made it more or less clear. Each of the parts of the assignment, single semantic and interpretation checks were quite short and I already had 3 or 4 done before I even realized it. But I definetly enjoyed finally getting to actually realize the code language we have been doing for so long. It feels weird to leave some parts of the code unfinished (you can make range variables but you can't do anything with them as an example). I almost want to carry on doing this thing longer, but I quess other things will have to take hold of my time now.