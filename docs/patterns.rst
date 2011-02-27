Patterns
========

This documents lists useful patterns.

Creating an index page
----------------------

The easiest way to create an index page is to create an ``index.html`` file 
in the ``input`` directory and loop over the ``articles`` variable:

Create the file::

    touch input/index.html

The content might look like this::

    status: hidden
    template: self

    {% extends "base.html" %}

    {% block content %}
        <ul>
        {% for article in articles %}
            <li><a href="{{ article.url }}">{{ article.title }}</a></li>
        {% endfor %}
        </ul>
    {% endblock %}

Setting the status to ``hidden`` prevents that the index page itself will
show up in the ``articles`` variable.

Creating an Atom feed
---------------------

Creating a feed is similar to creating an index page. Create an ``atom.xml``
file::
    
    touch input/atom.xml

And make sure you set ``status: hidden``, so the feed itself doesn't show up in the 
``articles`` variable::

    status: hidden
    template: self

    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <title>My Website</title>
        <link href="http://example.org/atom.xml" rel="self" />
        <link href="http://example.org" />
        <updated>{{ articles[-1].headers.date|datetimeformat("%Y-%m-%dT%H:%M:%SZ") }}</updated>
        <id>http://example.org/</id>
        <author>
            <name>Foo Bar</name>
            <email>foobar@example.org</email>
        </author>

        {% for article in articles %}
        <entry>
            <title>{{ article.headers.title }}</title>
            <link href="http://example.org/{{ article.headers.url }}" />
            <updated>{{ article.headers.date|datetimeformat("%Y-%m-%dT%H:%M:%SZ") }}</updated>
            <id>http://example.org/{{ article.headers.url }}</id>
            <content type="html">{{ article.body|e }}</content>
         </entry>
     {% endfor %}
    </feed>

