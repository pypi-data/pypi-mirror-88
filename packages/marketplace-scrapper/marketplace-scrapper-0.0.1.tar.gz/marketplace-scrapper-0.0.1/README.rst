Visual Studio Marketplace Scrapper.
===================================

| Get the details of an extension from ``marketplace.visualstudio.com``.
| Details are:

1. Extension title: ``title: STRING``
2. Extension publisher name: ``publisher_name: STRING``
3. Extension main image/logo: ``default_image: URL``
4. Number of installs: ``installs: INTEGER``

| All you need is the extension ID eg: ``muremwa.read-urls``
| The extension ID is called the **'Unique Identifier'**.

Installation
------------

You can install using pip.

.. code::

    pip install marketplace-scrapper

Usage
-----

In python code.
~~~~~~~~~~~~~~~

Import the main function.

.. code:: python

    import vscrap

    details = vscrap.get_extension_details('muremwa.read-urls')

The main function returns a dict with the details as described above.

.. code:: python

    {
        'title': 'django-read-urls',
        'publisher_name': 'muremwa',
        'default_image': 'https://cdn./*',
        'installs': 1010
    }

.. figure:: img/py_look.jpg
   :alt: Looks like this in python


In command line
~~~~~~~~~~~~~~~

Use the ``scrap.extension`` module and add one argument, the extension ID.

.. code::

        python -m scrap.extension muremwa.read-urls

.. figure:: img/cmd_look.jpg
   :alt: Looks like this in commandline
