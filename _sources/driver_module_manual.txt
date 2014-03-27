Driver Module reference guide
******************************

Software reference guide
=========================

Capabilities
-------------
The driver module contains all drivers developed for use with the TSTK. 
The driver module contains a method which will allow you to get the 
desired driver. 

How to use the driver module
-----------------------------
To use the driver module you import the module in your program, like::

    Import driver

To get a new object from one of the available drivers, you should use 
the get_driver function.
This function takes two arguments, a name and a driver_id. 
An example of this is::
    
    portal_driver = driver.get_driver(“portal”, 1)

This example will return a new instance of :py:class:`driver.Portal`
You can then use portal_driver by doing::

    fetched_page = portal_driver.fetch("http://www.google.com")
    print(fetched_page)


