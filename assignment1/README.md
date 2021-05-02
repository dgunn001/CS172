# CS172 - Assignment 1 (Tokenization)

## Team member 1 - Darrien Gunn
## Team member 2 - Alex Nguyen

###### Provide a short explanation of your design
* Used iterators to traverse the doc and remove stop words and puntuations
* Break the text down to tokens while removing the the stop words by reference each other
* Created a List of List for termInfo, docIndex and termIndex
* Use these list to populate the txt files 
* Read and write to the txt files to have them work with the extra credit format
* Created helper functions for data retrievel

###### Language used, how to run your code, if you attempted the extra credit (stemming), etc. 
# Langauge: Python
# How to run the code
1. ./read_index.py --doc DOCNAME
2. ./read_index.py --term TERMID
3. ./read_index.py --term TERMID --doc DOCNAME
4. ./read_index.py --doc DOCNAME --term TERMID
# Extra Credit
It was attempted and the text files look correct.
