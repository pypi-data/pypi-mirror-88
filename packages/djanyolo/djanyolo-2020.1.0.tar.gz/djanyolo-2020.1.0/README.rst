DjanYolo
=============

Manage yolo images efficiently. A django app template that can be loaded to any existing app.

Features
---------
* Supports Django models
* Admin panel
* Image annotation
* Image cropping


Note
--------
This pypi is a part of #100DaysOfCode challenge. I needed to learn how packing are pushed and managed on pypi. So came up with simple module that was already cooked up. Check `original repo <https://github.com/MexsonFernandes/DjanYolo/>`__.

How to install?
----------------


.. code:: python

    INSTALLED_APPS = (
        # ...
        'djanyolo',
    )
    
Register route
----------------

.. code:: python

  from django.urls import include
  
  urlpatterns = [
        # ...
        url(r'^djanyolo$', include('djanyolo.urls')),
  ]
  
Have fun!
