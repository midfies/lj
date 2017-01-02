learning_journal README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/pip install -e .

- $VENV/bin/initialize_learning_journal_db development.ini

- $VENV/bin/pserve development.ini

https://marc-lj-401.herokuapp.com/

---------- coverage: platform linux2, python 2.7.6-final-0 -----------
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
learning_journal/__init__.py                  10      7    30%   8-14
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py            10      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      31     20    35%   23-26, 30-56
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             34      2    94%   17-18
learning_journal/views/notfound.py             0      0   100%
------------------------------------------------------------------------
TOTAL                                        121     29    76%

----------- coverage: platform linux, python 3.5.2-final-0 -----------
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
learning_journal/__init__.py                  10      7    30%   8-14
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py            10      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      31     20    35%   23-26, 30-56
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             34      2    94%   17-18
learning_journal/views/notfound.py             0      0   100%
------------------------------------------------------------------------
TOTAL                                        121     29    76%
