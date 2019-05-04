# BTrees-Linear-Hashing
My implementation of the B+ Trees and Linear Hashing

## Running the files
```
    python3 <filename> M B
```

## B+ Trees
- The file *myBPTree.py* contains my code for the B+ tree. It contains the operations like reading the input file, reading the parameters, **M** (the number of main memory buffers) and **B** (the buffer size) and calling some functions.
- I have created 2 classes, one for the complete tree, and one for individual node of a tree.
- The **splitNode** function in the **Node** class gives the mechanism to split the existing node, or basically extending the tree.
- The **BPlusTree** is the main class for the tree, which contains the functions of inserting a value in tree, searching for a value in the tree and range queries in the tree.

## Linear Hashing
- The file *myLinHash.py* contains the code for the Linear Hashing.
- Some of the major variables used in the code are:
    * i - splitting round (determines hash function - h0 and h1 ... hi and h_i+1 )
    * p - which bucket needs to be split next p_sequence = {0,1; 0,1,2,3; 0,1,2,3,4,5,6,7; 0,1,2,3,4...15; 0,..31; ...}, Taken powers of 2.
    * S - total number of records
    * b -	initial hash function, modulo 2
- Some of the basic functions in the code and their functioning are:
    * **insert_in_hash_table** - Insert new values in the hash table
    * **hash_table_too_full** - Function for checking the density of the hash table. As sepcified the density should be less than 75%.
    * **create_new_bucket** - This function creates a new bucket when the density of the table is too high.