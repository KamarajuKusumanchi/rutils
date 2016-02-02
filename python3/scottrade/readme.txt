-------------------------------------------------------------------------------
To run the unit tests simply do

 % python3 -m unittest -v
test_new_format (tests.test_scottrade.TestScottrade) ... ok
Ran 1 test in 0.000s
OK
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Notes on tests/__init__.py

The tests/__init__.py is not needed if you specify the test script manually.
But it is needed if you want the tests to be automatically discovered. In any
case you do not need __init__.py in the current directory. For example

 % tree
.
├── scottrade.py
└── tests
    └── test_scottrade.py

1 directory, 2 files

Here there is no tests/__init__.py . 

The command below specifies the test script explicitly. So it works
irrespective of whether there is tests/__init__.py

 % python3 -m unittest -v tests/test_scottrade.py
test_new_format (tests.test_scottrade.TestScottrade) ... ok
Ran 1 test in 0.000s
OK

But this one does not

 % python3 -m unittest -v 
Ran 0 tests in 0.000s
OK

But it will work if you create an empty __init__.py file in tests directory.

 % touch tests/__init__.py

 % python3 -m unittest -v 
test_new_format (tests.test_scottrade.TestScottrade) ... ok
Ran 1 test in 0.000s
OK

Read https://docs.python.org/3/tutorial/modules.html for more information on
how __init__.py file is used.
-------------------------------------------------------------------------------
