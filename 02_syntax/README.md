
    What is syntax analysis and how is it related to other parts in compilation?
    Syntax analysis takes the tokens from the lexer and checks that they are in correct order. After an "int" -token comes variable name and after that an '=' sign followed by a number (or another variable).
    How is the syntactic structure of the language expressed in the PLY tool? I.e., what parts are needed in the code and how are they related to syntactic rules of the language?
    There are functions which compose of the rules of the language. The rules then define how and what tokens can be followed to which tokens and how the language must be expressed.
    Explain in English what the syntax of the following elements mean (i.e. how would you describe the syntax in textual form):
        Sheet variable definition
        A new sheet variable can be made by calling sheet and then giving a valid sheet-variable name. If you want to give a value to it, it can be given by giving an int multipiced by another int. Another way is to give an existing list of sheet rows.
        Function call
        Function is called by giving function name and brackets '[' and ']'. If arguments are needed, they are inside the brackets.
        Sheet variable definition with initialization list (“{…}”).
        A list is given. Inside the curly brackets are sheet rows which become elements of the sheet. The values are differantiatet from each other by commas. If however there is no comma, that means that the following element is placed on a new line.
    Answer the following based on the syntax definition:
        Is it possible to define a “nested” function, i.e. to define a new function inside another function? Why?
        It is not possible. In function definition there is 'formals' -elements and 'variable_definition' -elements which neither can define a new function.
        Is it syntactically possible to perform arithmetic with integers (1+2)? Why?
        Arithmetic can be performed with atoms and integers are not considered atoms. Only doubles can be used with calculations.
        Is it syntactically possible to initialize a range variable with a decimal value (range _rng = 2.0+3.0)? Why?
        Range expression can't take in arithmetic or double values so it is not possible.
        Are the following allowed by the syntax: xx--yy and --xx? Why?
        The first one is possible because yy can be negative and it can be subtrackted from another number. --xx however cannot, because it is not valid to have a number with a arithmetic symbol before it with nothing to calculate it with.
        Can comparisons appear in a sheet variable’s initialization list (sheet SS = { 1.0 < 2.0 })? Why?
        Only simple expressions can be inside those curly brackets. Comparisons are scalar expressions so it is not possible.
        How is it ensured that addition/subtraction are done after multiplication/division?
        They are made in different elements. Multiplication and division are terms whereas the other are simple expressions. This way the order of calculations can be ensured.
        In SheetScript, statements and definitions are not separated by semicolons (like in Java/C++) or line breaks (like in Python). How does the syntax known when one thing ends and another begins?
        It doesn't need to know when one thing ends and another begins. It just goes through the tokens and fits them inside the rules of the language. If there is ever a moment on abiguity on what the programmer wanted, it means that there is a syntax error.
    Please mention in the document if you didn’t implement functions (i.e. you are ok with passing with the minimum grade).
    I did implement functions.
    What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?
    The start was really hard and I didn't get much of it. But after having having spent some time with it and especially after watching the lecture where the assigment was explained more in depth it became more clear on what and how to do things. After really getting started with this it wasn't that hard anymore. Well not easy either but still... As for learning, well it all becomes more and more clearer and I even got some things from the lexical part too now that we actually used it more concretely.
