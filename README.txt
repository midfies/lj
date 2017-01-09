learning_journal README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/pip install -e .

- $VENV/bin/initialize_learning_journal_db development.ini

- $VENV/bin/pserve development.ini

Changes Made


---------- coverage: platform linux2, python 2.7.6-final-0 -----------
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
learning_journal/__init__.py                  11      8    27%   8-15
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py            12      0   100%
learning_journal/routes.py                    11      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      31     20    35%   23-26, 30-56
learning_journal/security.py                  26      0   100%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             74      0   100%
learning_journal/views/notfound.py             0      0   100%
------------------------------------------------------------------------
TOTAL                                        192     28    85%

36 passed in 5.24 seconds
py35 inst-nodeps: /home/fyza/codefellows/401/3_week/pyramid/learning_journal/.tox/dist/learning_journal-0.0.zip
py35 installed: beautifulsoup4==4.5.3,coverage==4.3.1,decorator==4.0.10,ipython==5.1.0,ipython-genutils==0.1.0,Jinja2==2.8.1,learning-journal==0.0,Mako==1.0.6,MarkupSafe==0.23,passlib==1.7.0,PasteDeploy==1.5.2,pexpect==4.2.1,pickleshare==0.7.4,prompt-toolkit==1.0.9,psycopg2==2.6.2,ptyprocess==0.5.1,py==1.4.32,Pygments==2.1.3,pyramid==1.7.3,pyramid-debugtoolbar==3.0.5,pyramid-ipython==0.2,pyramid-jinja2==2.7,pyramid-mako==1.0.2,pyramid-tm==1.1.1,pytest==3.0.5,pytest-cov==2.4.0,repoze.lru==0.6,simplegeneric==0.8.1,six==1.10.0,SQLAlchemy==1.1.4,traitlets==4.3.1,transaction==2.0.3,translationstring==1.3,venusian==1.0,waitress==1.0.1,wcwidth==0.1.7,WebOb==1.7.0,WebTest==2.0.24,zope.deprecation==4.2.0,zope.interface==4.3.3,zope.sqlalchemy==0.7.7
py35 runtests: PYTHONHASHSEED='1046984846'
py35 runtests: commands[0] | py.test --cov=learning_journal learning_journal/tests.py -q --cov-report term-missing
....................................

----------- coverage: platform linux, python 3.5.2-final-0 -----------
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
learning_journal/__init__.py                  11      8    27%   8-15
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py            12      0   100%
learning_journal/routes.py                    11      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      31     20    35%   23-26, 30-56
learning_journal/security.py                  26      0   100%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             74      0   100%
learning_journal/views/notfound.py             0      0   100%
------------------------------------------------------------------------
TOTAL                                        192     28    85%

