HOLY
====

Holy is a Python script which uses `ast` module to convert a Python source code to Ruby.
Holy is basically a `NodeVisitor` with ruby output.
See [`ast` documentation](http://docs.python.org/2/library/ast.html) for more information

Installation and Usage
======================

    $ sudo pip install holy
    $ holy <(<<EOF
    for i in range(5,10):
            print i
    EOF)

The above will result in

    5.upto(10) do |i|
      puts i
    end

Holy is in very early stages of development.
If you want to contribute, please open an issue on github to discuss the matters.
