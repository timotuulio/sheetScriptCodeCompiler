    1. What is lexical analysis and how is it related to other parts in compilation?
    - Lexial analysis is when the code is taken and the "text" (variables, numbers, etc) are interpreted as tokens. This way each single tokens real meaning or functionality is easier later to interpret as we already have the code read as tokens. It would be impossible to try to understand the meaning of some line without knowing if for example the '=' is part of the variable name or not.
    
    2. How is the lexical structure of the language expressed in the PLY tool? I.e., what parts are needed in the code and how are they related to lexical rules of the language?
    - You need to give the lexer what different tokens there can be in the code that it is given. In my file there are both reserved words which are simply "if there is this word, then it means it is this token", and also those that have more precise definitions. The more precise definitions need their own functions which tell exactly what in the token can be for it to be token type X. Other than that, well the lexer needs to be started or builded and errorhandling is good to have too so as to know what to do if there is a word that doesn't fit in any token.
    
    3. Explain how the following are recognized and handled in your code:
        a) Keywords
        - There is a list of reserved words which are recognized if they come up in the code.
        b) Comments
        - If the analyzer finds three '.' it ignores everything until it reches the other three '.'
        c) Whitespace between tokens
        - Whitespace is ignore with t.ignore
        d) Operators & delimiters (<-, parenthesis, etc.)
        - They are marked as simple tokens so the lexer can do its stuff with them
        e) Desimal literals
        - First is an optional '-'-sign, then at least one number, then a point ja lastly a single number
        f) String literals
        - Strings are recognized and compared to different functions I have made. For example an Sheet identification is a string with only big letters.
        g) Function names
        - If a string starts with a big letter and is followed by at least one small letter/number, then it is a function
    
    4. How can the lexer distinguish between the following lexical elements:
        a) Function name identifiers & variable name identifiers
        - Function names start with a big letter and variable with a small letter.
        b) Keywords & variable name identifiers
        - Keywords are considered first, so if the word is a keyword, it can't be a variable name.
        e) Operators > (greater than) & >= (greator or equal)
        - The lexam checks first the longer tokens and only after that it checks the single character tokens. So if there is an '=' after >, then it is "greater or equal".
        f) Info string literals & variables names
        - Info sting literals start with an '!' so if the lexer sees one of those, it just reads the code until it finds another and everything in between goes to the info literal.
        g) Comments & other code
        - If the lexer sees the three points, it reads everything as comment until it reads another three points.
        h)Integer literals & a decimal literals
        - Decimal literal is looked for first so if the lexer sees a number which is followed by a point and a single number, then we have a decimal literal and not an integer.
    
    5. Did you implement any extras? If so explain them (what and how)
    - Multiline comment works having given it the choice of being .* or \n with an extra parameter ? so that it is lazy and stops commenting on the first triple dot it encounters.
    
    6. What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?
    - It took me quite a while to understand how and what and why is everything going on with the lexical analysis and especially how does the code work. But after I undestood it the rest of the project wasn't all that difficult. It was nice to get my hand on the code as during the course that hasn't really happened. And something useful... Well, this part (and I assume the rest of them too) really does help understand how does these things called programming languages work and do their job.
