Universal Conceptual Cognitive Annotation
=========================================

UCCA is a linguistic framework for semantic annotation, whose details
are available at `the following
paper <http://aclweb.org/anthology/P13-1023>`__:

::

    @inproceedings{abend2013universal,
      author={Abend, Omri  and  Rappoport, Ari},
      title={{U}niversal {C}onceptual {C}ognitive {A}nnotation ({UCCA})},
      booktitle={Proc. of ACL},
      month={August},
      year={2013},
      pages={228--238},
      url={http://aclweb.org/anthology/P13-1023}
    }

This Python 3 package provides an API to the UCCA annotation and tools
to manipulate and process it. Its main features are conversion between
different representations of UCCA annotations, and rich objects for all
of the linguistic relations which appear in the theoretical framework
(see ``core``, ``layer0``, ``layer1`` and ``convert`` modules under the
``ucca`` package).

The ``scripts`` package contains various utilities for processing
passage files.

To parse text to UCCA graphs, use `TUPA, the UCCA
parser <https://github.com/danielhers/tupa>`__.

Authors
-------

-  Amit Beka: amit.beka@gmail.com
-  Daniel Hershcovich: daniel.hershcovich@gmail.com

License
-------

This package is licensed under the GPLv3 or later license.

::

                [ ~ Dependencies scanned by PyUp.io ~ ]

|Build Status (Travis CI)| |Build Status (AppVeyor)| |Build Status
(Docs)| |PyPI version|

.. |Build Status (Travis CI)| image:: https://travis-ci.org/danielhers/ucca.svg?branch=master
   :target: https://travis-ci.org/danielhers/ucca
.. |Build Status (AppVeyor)| image:: https://ci.appveyor.com/api/projects/status/github/danielhers/ucca?svg=true
   :target: https://ci.appveyor.com/project/danielh/ucca
.. |Build Status (Docs)| image:: https://readthedocs.org/projects/ucca/badge/?version=latest
   :target: http://ucca.readthedocs.io/en/latest/
.. |PyPI version| image:: https://badge.fury.io/py/UCCA.svg
   :target: https://badge.fury.io/py/UCCA
