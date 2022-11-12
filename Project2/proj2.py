#
# Name: Ziyi Liu
#

from Proj2_tree import printTree

#
# The following two trees are useful for testing.
#
smallTree = \
    ("Is it bigger than a breadbox?",
        ("an elephant", None, None),
        ("a mouse", None, None))
mediumTree = \
    ("Is it bigger than a breadbox?",
        ("Is it gray?",
            ("an elephant", None, None),
            ("a tiger", None, None)),
        ("a mouse", None, None))


def main():
    """
    Main funtion, Play 20 questions interface.

        Parameters:
            None

        Returns:
            None
    """
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.
    print("Welcome to the 20 Questions game!")
    user_load = yes("Would you like to load a saved game? \000")
    if user_load == True:
        filename = input("What is the name of the file? \000")
        treeFile = open(filename, 'r')
        tree = loadTree(treeFile)
        treeFile.close()
    else:
        tree = mediumTree
    
    continue_play = True
    while continue_play:
        tree = play(tree)
        continue_play = yes("Would you like to play again? \000")
    
    user_save = yes("Would you like to save your game? \000")
    if user_save == True:
        filename = input("What is the name of the file? \000")
        treeFile = open(filename, 'w')
        saveTree(tree, treeFile)
        treeFile.close()
        print("Thank you! Tree saved!")
    print("Goodbye!")


    


def simplePlay(tree):
    """
    The recursive function is used to play the game with a simple tree.

        parameters:
            qustion and answer with the structure of a tree

        returns:
            bool, recursive function
    """
    root, left, right = tree
    ans = yes(f"{root}\n")
    if isLeaf(tree):
        if ans:
            print("I got it!")
            return True
        return False
    if ans:
        return simplePlay(left)
    return simplePlay(right)
    


    
def play(tree):
    """    
    The recursive function is used to play the game with a tree, could add a node to the tree.
        parameters:
            qustion and answer with the structure of a tree

        returns:
            None, recursive function
    """
    root, left, right = tree
    ans = yes(f"{root}\n")
    if isLeaf(tree):
        if ans:
            print("I got it!")
            return tree
        return palyLeaf(tree)
    if ans:
        newTree = play(left)
        return (root, newTree, right)
    newTree = play(right)
    return (root, left, newTree)
    



# Determine the node is leaf or not     
def isLeaf(tree):
    _, left, right = tree
    if left == None and right == None:
        return True
    return False

# Ask user a yes/no question, return bool
def yes(prompt):
    guess = input(prompt)
    yes_options = ['yes', 'y', 'yup', 'sure', 'true']
    if (guess.lower() in yes_options):
        return True
    return False
    
# Suggest an answer and deciding whether it is correct
def palyLeaf(tree):
    origin_ans, _, _ = tree
    new_ans = input("What was it? \n")
    new_question = input(f"What's a question that distinguishes between a/an {new_ans} and a/an {origin_ans}? \n")
    ans = yes(f"And what's the answer for {new_ans}?")
    if ans:
        return (new_question, (new_ans, None, None), (origin_ans, None, None))
    return (new_question, (origin_ans, None, None), (new_ans, None, None))

# Save tree into a file
def saveTree(tree, treeFile):
    root, left, right = tree
    if isLeaf(tree):
        print('Leaf', file = treeFile)
        print(root, file = treeFile)
    else:
        print('Internal Node', file = treeFile)
        print(root, file = treeFile)
        if left is not None:
            saveTree(left, treeFile)
        if right is not None:
            saveTree(right, treeFile)

# Load tree from a file
def loadTree(treeFile):
    line = treeFile.readline()
    if line == '':
        return None
    elif line == 'Leaf\n':
        root = treeFile.readline()
        root = root.rstrip('\n')
        return (root, None, None)
    root = treeFile.readline()
    root = root.rstrip('\n')
    left = loadTree(treeFile)
    right = loadTree(treeFile)
    return (root, left, right)

#
# The following two-line "magic sequence" must be the last thing in
# your file.  After you write the main() function, this line it will
# cause the program to automatically play 20 Questions when you run
# it.
#
if __name__ == '__main__':
    main()
