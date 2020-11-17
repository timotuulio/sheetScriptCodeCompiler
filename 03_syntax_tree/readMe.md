
    What is an (abstract) syntax tree and how is it related to other parts in compilation?
    How is the syntax tree generated using the PLY tool? I.e., what things are needed in the code and how are they related to syntactic rules of the language and the tree?
    Explain in English what kind of tree is formed in your code from the following syntactic elements:
        Variable definitions
        For loop
        Function call (if you implemented it)
    Answer the following based on the syntax definition and your implementation:
        In which cases is it possible in your implementation to end up with a tree with empty child attributes (somewhere in the tree there is a place for a child node (or nodes), but there is none)? I.e., in which situations you end up with tree nodes with child_... attribute being None, or children_... attribute being an empty list?
        Are there places in your implementation where you were able to “simplify” the tree by omitting trivial/non-useful nodes or by collecting a recursive repeating structure into a list of child nodes?
    Please mention in the document if you didn’t implement functions/subroutines (i.e. you are ok with passing with the minimum grade).
    What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?
