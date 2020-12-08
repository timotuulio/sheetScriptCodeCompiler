
    What is an (abstract) syntax tree and how is it related to other parts in compilation?
    - Abstract syntax tree is a tree made with nodes that are tokens from the file that was read. They are pushed to the tree in logical order so that it is (at least somewhat) intuitive to read. Easiest example is a calculation 2 + 4 that has a node '+' with two child nodes '2' and '4'. Later on, by using this tree, it is possible to actually use the language and get the answer to this calculation. 
    
    How is the syntax tree generated using the PLY tool? I.e., what things are needed in the code and how are they related to syntactic rules of the language and the tree?
    - With PLY tool there is this variable p, which is the tokens (I think). When the code is read from a file, we make a nodes out of this p, give it name and sometimes a value, and then give it children. And as the file is being read the tree is being made at the same time. At each "rule" that is read we tell what needs to be done to the tree.
    
    Explain in English what kind of tree is formed in your code from the following syntactic elements:
        Variable definitions
        - When variable (and function) definitions are encountered, a "Funcs_vars[n]: variable definition" -node is made. It has a children which define the variable. There is a child which has the name and other child/children define the contents of the variable. If the variable is more complex, these children in turn may have their own child-nodes.
        
        For loop
        - The root node for For-loop is a node with two childs. The first child is the "for this long" -part and the second child is the "do" -part. The first child has multiple children as it needs a range list, a range from what to what to know how long it will carry on. The "do"-node has it's own children which explain what needs to be done in the loop.
        
        Function call (if you implemented it)
        - Function call itself is the root node. It has a child "arguments" which in turn has a list of children which are the arguments function takes (if there are any). It also has a node which has the name of the function, but that's about it. Nothing too complex
        
    Answer the following based on the syntax definition and your implementation:
        In which cases is it possible in your implementation to end up with a tree with empty child attributes (somewhere in the tree there is a place for a child node (or nodes), but there is none)? I.e., in which situations you end up with tree nodes with child_... attribute being None, or children_... attribute being an empty list?
        - I don't think there is such a place if the syntax is correct. For each list of children (where none or multiple children are allower) there are versions to have children or not have children. If there are no children, the program takes the path of no children. As for empty child nodes, I don't think that's possible either. I can't think of a situation where that could happen.
        
        Are there places in your implementation where you were able to “simplify” the tree by omitting trivial/non-useful nodes or by collecting a recursive repeating structure into a list of child nodes?
        - Argument lists, formals and statement list at least are made simple by having them all in a list. And there are plenty of nodes which were redundant and therefore skipped. Function_and_variable_definition is a variable_, subroutine_ or function_definition. Variable definition is sheet_, range_ or scalar_definition. Atoms are skipped because they hold no information as such.
    
    Please mention in the document if you didn’t implement functions/subroutines (i.e. you are ok with passing with the minimum grade).
    - I implemented them
    
    What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?
    - This part of the assignment was difficult as well. Same as previous parts, the start was really difficult but eventually when you started to get the hand of it, it started to get going. Half of the project was wondering about everything, half was somewhat-clear-and-not-too-hard-but-still-laborius coding. Recursion was one of the more troublesome parts as I had to change the original rules of the syntax checker to get the tree form more gracefully. Also I do fear that there are plenty of things that later needs to be remade for the last part of the assignment. The syntax tree seems correct enough and it's not like it needs to be the same as in the examples, but there very well might be stuff missing or maybe the structure needs reworking to better suit the last part. And not all child-node names are too well named.