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

    xestore.login()

    xestore.publish_file(path, metadata={}, private=False)

    xestore.download_file("filename.npy", savedir="./", private=False)

    doc = {"list": [1,2,3]}
    xestore.publish_document(doc, name="new document", metadata={}, private=False)
    




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
