"""
Comprehensive Guide to Run This Test Script
-------------------------------------------

Project Structure:
------------------
Your project should be structured as follows:

Hangman_2.0/
│   __init__.py         - Indicates that this directory is a Python package.
│   Decision_Tree.py    - The module you want to test.
└───Iris_testing/
    │   __init__.py     - Indicates that this directory is a subpackage.
    │   test_Decision_Tree.py - This test script.

Each directory contains an '__init__.py' file, making them recognizable as Python packages.

Running the Test:
-----------------
To run this test script, you should execute it as a module within the 'Hangman_2.0' package. 
This requires running the script from the directory *above* 'Hangman_2.0', NOT from within 'Hangman_2.0' or 'Iris_testing'.

For example, if your directory structure on your filesystem looks like this:

some_parent_directory/
└───Hangman_2/
    │   __init__.py
    │   Decision_Tree.py
    └───Iris_testing/
        │   __init__.py
        │   test_Decision_Tree.py

You should navigate to 'some_parent_directory' and then execute the test module using Python's '-m' option:

1. Open your terminal or command prompt.
2. Navigate to 'some_parent_directory'. Use the command 'cd path/to/some_parent_directory'.
3. Run the script with the command:
   'python -m Hangman_2.Iris_testing.test_Decision_Tree'

This command tells Python to run 'test_Decision_Tree.py' as a module within the 'Hangman_2.0.Iris_testing' package.

Why This Method:
-----------------
This method ensures that Python correctly recognizes the package structure and can resolve relative imports (like 'from .. import Decision_Tree') within the 'Hangman_2.0' package. Running the script directly or from the wrong directory would lead to import errors.

Important Notes:
----------------
- Ensure your current working directory is the one directly above 'Hangman_2'.
- If using an IDE, configure it to recognize 'Hangman_2.0' as the project root.
- This setup is crucial for maintaining a clear and scalable project structure, especially in larger or complex Python projects.
"""

import pandas as pd 

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from .. import Decision_Tree

data = pd.read_csv('.\\Hangman_2\\Iris_testing\\iris_dataset.csv')

X = data.iloc[:,:-1].values
Y = data.iloc[:, -1].values.reshape(-1,1)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.4)

tree = Decision_Tree.DecisionTree(min_split=3, max_depth=3)


tree.fit(X_train, Y_train)
predictions = tree.predict(X_test)

print(accuracy_score(Y_test, predictions))

