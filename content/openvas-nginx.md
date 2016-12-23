title: Deploy gsad behind an an nginx proxy
category: OpenVAS
author: Benoît Allard
date: 2016-04-30
tags: OpenVAS, NGINX
status:  published

[OpenVAS](http://www.openvas.org) is a network vulnerability scanner published
under the [GNU GPLv2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
license. For those with difficulties to understand all those license legalese,
this means your freedom is not impacted by this software. This license, allows
you to do whatever you want with it as long as you do not restraint the freedom
of others. This includes reading the source code, modifying it, using and
distributing a modified version. You are just not allowed to distribute it
under a more restrictive license. All this is allowed for OpenVAS at no
extra-cost. Proprietary equivalences for OpenVAS includes *Nessus* from
Tenable, or *Nexpose* from Rapid7.

So, you have been toying with OpenVAS for some time, so far it does fit your
needs, and you wanted to take it to the next level: deploy it seriously in your
network. You realised it quickly, the main interface is the gsad, and it is
web-based. You have been deploying a few web-applications before, so you are
familiar with the configuration of [nginx](http://nginx.org/) (or any similar
proxy), you maybe even have a CDN running somewhere on your network, and you
could not imagine deploy yet another web-based application without bringing all
that knowledge you previously gathered into practice once more.

You are at the right place, as this article will take you through the
installation of the gsad service, and will leave the serving of static assets
to the experts.

Rebuild the service
-------------------

> **note**

> This step is not absolutely necessary, but it does not make much sense to
> leave the internal file server (together with its integrated vulnerabilities)
> running if you do not plan to use it.

The first necessary step is to disable the internal file server of the gsad
service. To do so, just add the following to your cmake invocation
`-DSERVE_STATIC_ASSETS=0` and rebuild the daemon. Do not forget to at least set
the `CMAKE_BUILD_TYPE` to `Release` as well. Just `make install`, and you are
done for this part.

Give the right parameters to the gsad service
---------------------------------------------

The following step is about disabling the TLS negotiation. The `--http-only`
parameters is there for that purpose.

Additionally, we will use a unix socket to communicate between our proxy and
the gsad service. We use for that the `--unix-socket=/var/run/gsad.sock`
parameter. The gsad service will make sure to leave the rights on that socket
unchanged, so if you need some special ones, just create the socket beforehand,
and set the permissions on it as you wish. The actual path you use is not
relevant as long as you give the same one to your proxy configuration.

> **note**

> As we do not plan to make any direct file access from the gsad service, it
> does no make much sense to use the `--do-chroot` parameter, and as we do not
> need to open any privileged port, the `--drop-privilege` one is not necessary
> either. We can already start with lowered privileges.

Configure your proxy
--------------------

Comes the last part: teaching the proxy (in our case, nginx) to communicate
with the service. Here comest the time where you might want to configure the
TLS negotiation, or just leave it away if you are in a trusted zone anyway, and
you do not want to bother with certificates. gsad comes with two *faces*, we
will use here the `classic` one. If you compiled your gsad locally, the files
will be installed under the following path:
`/usr/local/share/openvas/gsa/classic`. Those are the files you will want to
serve directly. There are three directories in there: `js`, `css`, and `img`.
For the gsad service, there are at least two extra header fields you will want
to set via your proxy:

`X-Real-IP`: OpenVAS will use this IP instead of the IP of the proxy to
identify the session, and propose some shortcut like in the task creation
Wizard.

`X-Forwarded-Protocol`: This will be used as the protocol when the redirect URL
needs to be formed.

You might want to set `Host` and `X-Forwarded-For` as well, but gsad is not
parsing them (yet ?) at this moment.

As a last point, if you are configuring your proxy to serve gsad over
HTTPS, you probably also want to setup a redirect in your proxy
configuration as well. I believe the right HTTP code to use here is 301
Moved Permanently. It will be cached by other proxies, and will only
create troubles if you ever want to stop delivering the gsad over HTTPS.

Files
-----

**gsad.conf**:

    upstream gsa { server unix:///var/run/gsad.sock; }

    server {
      listen [::]:80 ipv6only=off;
      return 301 https://$host$request_uri;
    }

    server {

      listen [::]:443 ssl ipv6only=off;

      ssl_certificate     /usr/local/var/lib/openvas/CA/servercert.pem;
      ssl_certificate_key /usr/local/var/lib/openvas/private/CA/serverkey.pem;


      root /usr/local/share/openvas/gsa/classic;

      location ~ ^/(js/|css/|img/) {
        root /usr/local/share/openvas/gsa/classic;
      }

      location / {
        proxy_pass http://gsa;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Protocol $scheme;
        proxy_set_header X-Real-IP $remote_addr;
      }

    }


**gsad.service**:

    [Unit]
    Documentation=man:gsad(8) http://www.openvas.org/
    Wants=openvas-manager.service

    [Service]
    Type=simple
    ExecStart=/usr/local/sbin/gsad --foreground --http-only --unix-socket=/var/run/gsad.sock
    Environment=LD_LIBRARY_PATH=/usr/local/lib
    Restart=always

    [Install]
    WantedBy=multi-user.target
