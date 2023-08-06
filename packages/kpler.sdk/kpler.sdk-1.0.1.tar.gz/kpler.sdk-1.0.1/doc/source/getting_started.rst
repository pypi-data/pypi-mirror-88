Getting started
***************

Setup
-----

Supported Python: ``3.7``, ``3.8``, and ``3.9``

.. code-block::
   :linenos:

    pip install kpler.sdk


Authentication
--------------

Create a ``Configuration`` with the targeted ``Platform``, your ``email`` and ``password`` to pass it to the client :

.. code-block:: python
   :linenos:


   from kpler.sdk.configuration import Configuration
   from kpler.sdk import Platform
   config = Configuration(Platform.Liquids, "<your email>", "<your password>")

   from kpler.sdk.resources.trades import Trades
   trades_client = Trades(config)

Available platforms:

   - ``LNG``
   - ``LPG``
   - ``Dry``
   - ``Liquids``
