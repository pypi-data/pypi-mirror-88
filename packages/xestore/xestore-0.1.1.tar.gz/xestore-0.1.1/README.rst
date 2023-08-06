=======
xestore
=======


.. image:: https://img.shields.io/pypi/v/xestore.svg
        :target: https://pypi.python.org/pypi/xestore

.. image:: https://img.shields.io/travis/jmosbacher/xestore.svg
        :target: https://travis-ci.com/jmosbacher/xestore

.. image:: https://readthedocs.org/projects/xestore/badge/?version=latest
        :target: https://xestore.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A simple file and document storage utility for XENONnT

Usage
-----

.. code-block:: python

    import xestore
    store = xestore.XeStore()
    store.login()
    
    store.files.upload("a_public_file.txt")
    store.files.private.upload("a_private_file.txt")
    
    store.files['a_public_file'].download(PATH_TO_SAVE)

    doc = {"list": [1,2,3]}
    store.documents.upload(doc, name="new_document", **metadata)
    


* Free software: MIT
* Documentation: https://xestore.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage
