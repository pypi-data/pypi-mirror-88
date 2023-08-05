.. _changelog:

Changelog
=========

A summary of changes in the Jupyter Server.
For more detailed information, see
`GitHub <https://github.com/jupyter/jupyter_server>`__.

.. tip::

     Use ``pip install jupyter_server --upgrade`` or ``conda upgrade jupyter_server`` to
     upgrade to the latest release.

.. we push for pip 9+ or it will break for Python 2 users when IPython 6 is out.

We strongly recommend that you upgrade to version 9+ of pip before upgrading ``jupyter_server``.

.. tip::

    Use ``pip install pip --upgrade`` to upgrade pip. Check pip version with
    ``pip --version``.

.. _release-1.0.6:

1.0.6
-----

1.0.6 is a security release, fixing one vulnerability:

- Fix open redirect vulnerability GHSA-grfj-wjv9-4f9v (CVE-2020-26232)

.. _release-1.0.0:

1.0.0
-----

- Extension discovery
- Classic server extension discovery and support
- Bug fixes
- Ready for users
- JupyterLab is the first server running on top of Jupyter Server

.. _release-0.0.2:

0.0.2
-----

- Introduce new extension module
- Pytest for unit tests
- Server documentation
- NbClassic for migration from notebook

.. _release-0.0.1:

0.0.1
-----

- First release of the Jupyter Server.
