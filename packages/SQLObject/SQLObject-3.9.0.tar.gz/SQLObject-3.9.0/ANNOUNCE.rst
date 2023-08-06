Hello!

I'm pleased to announce version 3.9.0, the first release
of branch 3.9 of SQLObject.


What's new in SQLObject
=======================

Contributors for this release are:

+ Michael S. Root, Ameya Bapat - ``JSONCol``;

+ Jerry Nance - reported a bug with ``DateTime`` from ``Zope``.

Features
--------

* Add ``JSONCol``: a universal json column that converts simple Python objects
  (None, bool, int, float, long, dict, list, str/unicode to/from JSON using
  json.dumps/loads. A subclass of StringCol. Requires ``VARCHAR``/``TEXT``
  columns at backends, doesn't work with ``JSON`` columns.

* Extend/fix support for ``DateTime`` from ``Zope``.

* Drop support for very old version of ``mxDateTime``
  without ``mx.`` namespace.

Drivers
-------

* Support `mariadb <https://pypi.org/project/mariadb/>`_.

CI
--

* Run tests with Python 3.9 at Travis and AppVeyor.

For a more complete list, please see the news:
http://sqlobject.org/News.html


What is SQLObject
=================

SQLObject is an object-relational mapper.  Your database tables are described
as classes, and rows are instances of those classes.  SQLObject is meant to be
easy to use and quick to get started with.

It currently supports MySQL, PostgreSQL and SQLite; connections to other
backends - Firebird, Sybase, MSSQL and MaxDB (also known as SAPDB) - are
lesser debugged).

Python 2.7 or 3.4+ is required.


Where is SQLObject
==================

Site:
http://sqlobject.org

Development:
http://sqlobject.org/devel/

Mailing list:
https://lists.sourceforge.net/mailman/listinfo/sqlobject-discuss

Download:
https://pypi.org/project/SQLObject/3.9.0

News and changes:
http://sqlobject.org/News.html

StackOverflow:
https://stackoverflow.com/questions/tagged/sqlobject


Example
=======

Create a simple class that wraps a table::

  >>> from sqlobject import *
  >>>
  >>> sqlhub.processConnection = connectionForURI('sqlite:/:memory:')
  >>>
  >>> class Person(SQLObject):
  ...     fname = StringCol()
  ...     mi = StringCol(length=1, default=None)
  ...     lname = StringCol()
  ...
  >>> Person.createTable()

Use the object::

  >>> p = Person(fname="John", lname="Doe")
  >>> p
  <Person 1 fname='John' mi=None lname='Doe'>
  >>> p.fname
  'John'
  >>> p.mi = 'Q'
  >>> p2 = Person.get(1)
  >>> p2
  <Person 1 fname='John' mi='Q' lname='Doe'>
  >>> p is p2
  True

Queries::

  >>> p3 = Person.selectBy(lname="Doe")[0]
  >>> p3
  <Person 1 fname='John' mi='Q' lname='Doe'>
  >>> pc = Person.select(Person.q.lname=="Doe").count()
  >>> pc
  1
