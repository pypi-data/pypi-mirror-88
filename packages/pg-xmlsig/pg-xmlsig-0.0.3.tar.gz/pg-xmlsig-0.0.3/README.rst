===================================
PGXmlSIG: Python native XML Signature
===================================

A python native library that signs and verifies xml signatures. Based on xmlsig.

Highlights:
 * Build on top of lxml and cryptography


Installation
------------

.. code-block:: bash

    pip install pg-xmlsig

Usage
=====

.. code::

  import pgxmlsig

  sign = pgxmlsig.template.create(c14n_method=xmlsig.constants.TransformExclC14N, sign_method=xmlsig.constants.TransformRsaSha1)
  ref = pgxmlsig.template.add_reference(sign, xmlsig.constants.TransformSha1)
  pgxmlsig.template.add_transform(ref, xmlsig.constants.TransformEnveloped)

  ctx = pgxmlsig.SignatureContext()



To have more examples, look at the source code of the testings

Functionality
=============

Signature is only valid using RSA and HMAC validation.
ECDSA and DSA is still being implemented

License
=======

This library is published under the BSD license.
