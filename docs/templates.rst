.. _templates:

Templates
=========

The Jinja2 template engine is used to render templates. If no template is specified the ``default.html`` template will be used. Custom templates must be located in the ``templates/`` directory.  You can use the ``template`` header in an article to specify a template file.

Template Context
----------------

The following variables are available in the template context:

**headers**
    The headers specified by an article. 
**body**
    The (processed) body
**articles**
    A list of all public articles sorted by date. Articles with the “hidden” status and a date that is in the future are not public.
**settings**
    Project settings

Template Filters
----------------

Beside the default Jinja2 filters, the following additional filters are available:

**datetimeformat(format)**
    Formats a datetime object to `format`. Example ``foobar|datetimeformat("%d %m %Y")``
**ordinalsuffix**
    Appends the ordinal suffix (st/nd/rd/th). Example: ``foobar|ordinalsuffix``

Article as a template
---------------------

Beside specifying a filename as a template, you can also use ``self`` to use the article itself as the template::

    template: self
    status: hidden

    {% extends "base.html" %}

    {% block content %}
    <div id="index_page">
        <ul>
        {% for article in articles %}
            <li>
                <span class="date">{{ article.headers.date|datetimeformat("%d. %b %Y") }}</span>
                <a href="{{ article.headers.url }}">{{ article.headers.title }}</a>
            </li>
        {% endfor %}
        </ul>
    </div>
    {% endblock %}

