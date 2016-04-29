Deploy gsad behind an an nginx proxy
====================================

:category: OpenVAS
:author: Benoît Allard
:date: 2016-03-03-15-00
:tags: OpenVAS, NGINX
:status: draft

So, you have been toying with OpenVAS_ for some time, so far it does fit your needs, and you wanted to take it to the next level: deploy it seriously in your network.
You realized it quickly, the main interface is the gsad, and it is web-based.
You have been deploying a few web-applications before, so you are familiar with the configuration of nginx_ (or any similar proxy), you maybe even have a CDN running somewhere on your network, and you could not imagine deploy yet another web-based application without bringing all that knowledge you previously gathered into practice once more.

You are at the right place, as this article will take you through the installation of the gsad service, and will leave the serving of static assets to the experts.

.. _OpenVAS: http://www.openvas.org
.. _nginx: http://nginx.org/

Rebuild the service
-------------------

.. note::
    This step is not absolutely necessary, but it does not make much sense to leave the internal file server (and all its pre-compiled vulnerabilities) running if you do not plan to use it.

The first necessary step is to disable the internal file server of the gsad service.
To do so, just add the following to your cmake invocation ``-DSERVE_STATIC_ASSETS=0`` and rebuild the daemon.
Do not forget to at least set the ``CMAKE_BUILD_TYPE`` to ``Release`` as well.
Just ``make install``, and you are done for this part.


Give the right parameters to the gsad service
---------------------------------------------

The following step is about disabling all the additional features from the gsad like redirection (80 -> 443) and the TLS negotiation.
The ``--no-redirect`` and ``--http-only`` parameters are there for that purpose.

Additionally, we will use a unix socket to communicate between our proxy and the gsad service.
We use for that the ``--unix-socket=/var/run/gsad.sock`` parameter.
The gsad service will make sure to leave the rights on that socket unchanged, so if you need some special ones, just create the socket beforehand, and set the permissions on it as you wish.
The actual path you use is not relevant as long as you give the same one to your proxy configuration.

.. note::
  As we do not plan to make any direct file access from the gsad service, it does no make much sense to use the ``--do-chroot`` parameter, and as we do not need to open any priviledged port, the ``--drop-priviledge`` one is not necessary either.
  We can already start with lowered priviledges.

Configure your proxy
--------------------

Comes the last part: teaching the proxy (in our case, nginx) to communicate with the service.
Here comest the time where you might want to configure the TLS negotiation, or just leave it away if you are in a trusted zone anyway, and you do not want to bother with certificates.
gsad comes with two *faces*, we will use here the ``classic`` one.
If you compiled your gsad locally, the files will be installed under the following path: ``/usr/local/share/openvas/gsa/classic``.
Those are the files you will want to serve directly.
There are three directories in there: ``js``, ``css``, and ``img``.
For the gsad service, there are at least two extra header fields you will want to set via your proxy:

``X-Real-IP``:
  OpenVAS will use this IP instead of the IP of the proxy to identify the session, and propose some shortcut like in the task creation Wizard.
  
``X-Forwarded-Protocol``:
  This will be used as the protocol when the redirect URL needs to be formed.

You might want to set ``Host`` and ``X-Forwarded-For`` as well, but gsad is not parsing them (yet ?) at this moment.

As a last point, if you are configuring your proxy to serve gsad over HTTPS, you probably also want to setup a redirect in your proxy configuration as well.
I believe the right HTTP code to use here is 301 Moved Permanently.
It will be cached by other proxies, and will only create troubles if you ever want to stop delivering the gsad over HTTPS.
