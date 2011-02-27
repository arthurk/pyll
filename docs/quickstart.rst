Quickstart
==========

The first thing you'll need to do is to create a directory for you website::

    mkdir mysite

Lanyon will look for articles in a directory called ``input``, so you'll need
to create this as well::

    mkdir website/input
    cd website

Now you can execute the ``lanyon`` command. The output should look like this::

    OK (0 articles; 0.0 seconds)


You can start writing articles now. Let's create an empty file and run the
``lanyon`` command::

    touch input/hello.rst
    lanyon

The output should look like this::

    .
    OK (1 article; 0.29 seconds)
    
If you take a look at the directory listing, you'll see that an ``output`` directory
was created. This directory holds the generated website. You can open up
the generated article ``output/hello.html`` in you browser.
