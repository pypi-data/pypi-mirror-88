Install
=======

Preferable way is to :ref:`download <download>` tarball with the
signature from `official website <http://www.pyderasn.cypherpunks.ru/>`__::

    $ [fetch|wget] http://www.pyderasn.cypherpunks.ru/pyderasn-8.2.tar.xz
    $ [fetch|wget] http://www.pyderasn.cypherpunks.ru/pyderasn-8.2.tar.xz.sig
    $ gpg --verify pyderasn-8.2.tar.xz.sig pyderasn-8.2.tar.xz
    $ xz --decompress --stdout pyderasn-8.2.tar.xz | tar xf -
    $ cd pyderasn-8.2
    $ python setup.py install
    # or copy pyderasn.py (+six.py, possibly termcolor.py) to your PYTHONPATH

PyDERASN depends on `six <https://pypi.org/project/six/>`__ package
for keeping compatibility with Py27/Py35. It is included in the tarball.
You can also find it mirrored on :ref:`download <download>` page.
``termcolor`` is an optional dependency used for output colourizing.
``urwid`` is an optional dependency used for :ref:`interactive browser <browser>`.

You could use pip (**no** OpenPGP authentication is performed!) with PyPI::

    $ cat > requirements.txt <<EOF
    pyderasn==8.2 --hash=sha256:TO-BE-FILLED
    six==1.15.0 --hash=sha256:30639c035cdb23534cd4aa2dd52c3bf48f06e5f4a941509c8bafd8ce11080259
    EOF
    $ pip install --requirement requirements.txt

You have to verify downloaded tarballs integrity and authenticity to be
sure that you retrieved trusted and untampered software. `GNU Privacy
Guard <https://www.gnupg.org/>`__ is used for that purpose.

For the very first time it is necessary to get signing public key and
import it. It is provided below, but you should check alternative
resources.

::

    pub   rsa2048/0x04A933D1BA20327A 2017-09-20
          2ED6 C846 3051 02DF 5B4E  0383 04A9 33D1 BA20 327A
    uid   PyDERASN releases <pyderasn@cypherpunks.ru>

    $ gpg --auto-key-locate dane --locate-keys pyderasn at cypherpunks dot ru
    $ gpg --auto-key-locate wkd --locate-keys pyderasn at cypherpunks dot ru

.. literalinclude:: ../PUBKEY.asc
