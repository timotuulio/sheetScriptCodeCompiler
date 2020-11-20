
    What is an (abstract) syntax tree and how is it related to other parts in compilation?
    - Abstract syntax tree is a tree made with nodes that are tokens from the file that was read. They are pushed to the tree in logical order so that it is (at least somewhat) intuitive to read. Easiest example is a calculation 2 + 4 that has a node '+' with two child nodes '2' and '4'. Later on, by using this tree, it is possible to actually use the language and get the answer to this calculation. 
    
    How is the syntax tree generated using the PLY tool? I.e., what things are needed in the code and how are they related to syntactic rules of the language and the tree?
    - With PLY tool there is this variable p, which is the tokens or something. When the code is read from a file, we make a nodes out of this p, give it name and sometimes a value, and then give it children. And as the file is being read the tree is being made at the same time.
    
    Explain in English what kind of tree is formed in your code from the following syntactic elements:
        Variable definitions
        - Variable (and function) definitions go into a list at the start of reading the file. The tree represents these trees very simply. "Assigns[X]: variable definition" which has a child which is the expression for the variable. There might be more childs if the definition of a variable is more complex but generally it is that simple.
        For loop
        - The root node for For-loop is a node with two childs. The first child is the "for this long" -part and the second child is the "do" -part. The first child has multiple children as it needs a range list, a range from what to what to know how long it will carry on.
        Function call (if you implemented it)
        - Function call itself is the root node. It has a child "arguments" which in turn has a list of children which are the arguments (if there are any)
    Answer the following based on the syntax definition and your implementation:
        In which cases is it possible in your implementation to end up with a tree with empty child attributes (somewhere in the tree there is a place for a child node (or nodes), but there is none)? I.e., in which situations you end up with tree nodes with child_... attribute being None, or children_... attribute being an empty list?
        - 
        
        Are there places in your implementation where you were able to “simplify” the tree by omitting trivial/non-useful nodes or by collecting a recursive repeating structure into a list of child nodes?
        - Argument lists, formals and statement list at least are made simple by having them all in a list.
    
    Please mention in the document if you didn’t implement functions/subroutines (i.e. you are ok with passing with the minimum grade).
    - 
    
    What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?
    - 