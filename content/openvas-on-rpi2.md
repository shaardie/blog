title: Installing OpenVAS on the Raspberry Pi 2
category: OpenVAS
date: 2016-03-10
tags: OpenVAS, Raspberry Pi 2
status: draft

[OpenVAS][openvas-website] calls itself the *The world's most advanced Open
Source vulnerability scanner and manager* and it is quite a nice tool to scan
small and large networks to find vulnerabilities.

It is able to scan your network from a server on a daily, weekly or
what-so-ever bases and send you reports for example via email. Also it is easy
to create new scan configurations for a completely new network.

Therefor it is the perfect candidate to install on a [Raspberry Pi
2][rpi-website], because it is an energy-efficient and portable device. You can
set up a home server and scan your network on a regular base or bring it to
other networks and scan them.

Unfortunately OpenVAS has also some disadvantages. It needs some hardware to
run properly and is not very easy to install.

The first disadvantage is the reason why i use a Raspberry Pi 2 to run
OpenVAS. The Raspberry Pi might not have enough power. Also it goes without
saying, that you be not be able to run very fast scans or scan very large
networks.

The second disadvantage will be hopefully compensated by this post.

In the following i will describe the installation process of OpenVAS on the
Raspberry Pi 2, but this instruction should be easily adoptable to other
machines.


##Operation System Debian

First of all i need a operating system on the Raspberry Pi 2. OpenVAS is
developed on a [Debian][debian-website] and therefor i will also use it.
Fortunately the Raspberry Pi 2 comes with a **ARM Cortex-A7 CPU** which is
naturally supported by Debian. So i do not need to use a Raspbian, but a
minimal stock Debian Jessie.

Instead of debootstraping our own, i will use the one created by
[collabora][collabora-website]. This can be found [here][rpi-image].

To copy this image to you sd card `/dev/sdb` execute the following command.
This will erase all data on the sd card. **CAUTION!** This step only sensible,
if your sd card is plugged in at `/dev/sdb`. Replace it with your sd card
drive.

    :::bash
    gunzip -c jessie-rpi2-20150705.img.gz | dd of=/dev/sdb

We used a 16GB sd card and the image does not use the full size so i resized
the partition. An instruction for that, can be found [here][resize].

Now you should be able to plug in the sd card to the Raspberry Pi 2 and start
it. You can log in with the credentials:

    :::text
    user: root
    passwort: debian

It goes without saying that you should change this password (you can use `passwd` for that).

Now i should update our operating system to the newest version

    :::bash
    apt-get update && apt-get -y dist-upgrade

After the update it would be nice to set the correct locales set

    :::bash
    dpkg-reconfigure locales

Now i have a up to date Debian Jessie and can go on with installing the OpenVAS software.

##Script

The easiet thing you can do to install OpenVAS now is using the shell script
printed below, but i recommend to skip this section and move on with the manual
installation. This post is maybe obsolete for the latest svn revision from
OpenVAS at the time you are reading this. If you use the manual steps you can
adjust the steps do get a proper installation.

    :::bash
    #!/bin/bash

    set -u
    set -e

    REVISION="HEAD"
    PACKAGES=openvas-smb openvas-libraries openvas-scanner openvas-manager gsa
    PREREQUISITES="subversion \
      gcc \
      bison \
      flex \
      cmake
      pkg-config \
      libglib2.0-dev \
      libgnutls28-dev \
      libgcrypt20-dev \
      zlib1g-dev \
      libpcap-dev \
      libgpgme11-dev \
      uuid-dev \
      libssh-gcrypt-dev \
      libhiredis-dev \
      libsnmp-dev \
      libksba-dev \
      libldap2-dev \
      gcc-mingw-w64 \
      heimdal-dev \
      libpopt-dev \
      libpcap-dev \
      libssh-gcrypt-dev \
      libgpgme11-dev \
      zlib1g-dev \
      libhiredis-dev \
      libsnmp-dev \
      rsync \
      redis-server \
      nmap \
      gnutls-bin \
      xsltproc \
      xmlstarlet \
      texlive-latex-base \
      texlive-latex-extra \
      xmlstarlet \
      zip \
      rpm \
      fakeroot \
      alien \
      gnupg \
      wget \
      curl \
      python \
      libxml2-dev \
      libxslt1-dev \
      libmicrohttpd-dev \
      libsqlite3-dev \
      sqlite3"

      echo "Install Prerequisites"
      apt-get update && apt-get install -y $PREREQUISITES

      echo "Checkout OpenVAS source code"
      svn checkout --revision $REVISION \
        --non-interactive \
        --trust-server-cert \
        https://scm.wald.intevation.org/svn/openvas/trunk

      echo "Install OpenVAS"
      cd trunk
      for package in $PACKAGES
      do
        echo "Install $package"
        mkdir -p $package/build
        cd $package/build
        cmake ..
        make
        make install
        cd ../../
      done

      echo "Update dynamic linker run-time bindings"
      ldconfig

      echo "Configure Redis Server"
      cp openvas-scanner/doc/example_redis_2_6.conf.in /etc/redis/redis.conf
      systemctl restart redis-server

      echo "Create Certificate Structure"
      openvas-manage-certs -a

      echo "Create Systemd Service files"
      echo "[Unit]
      Description=OpenVAS Scanner
      After=network.target redis-server.target

      [Service]
      ExecStart=/usr/local/sbin/openvassd --foreground --listen=127.0.0.1

      [Install]
      WantedBy=multi-user.target" \
        > /etc/systemd/system/multi-user.target.wants/openvassd.service

      echo "[Unit]
      Description=OpenVAS Manager
      After=network.target redis-server.target

      [Service]
      ExecStart=/usr/local/sbin/openvasmd --foreground --listen=127.0.0.1

      [Install]
      WantedBy=multi-user.target" \
        > /etc/systemd/system/multi-user.target.wants/openvasmd.service

      echo "
      [Unit]
      Description=Greenbone Security Assistant
      After=network.target redis-server.target

      [Service]
      ExecStart=/usr/local/sbin/gsad --foreground --drop-privileges

      [Install]
      WantedBy=multi-user.target" \
        > /etc/systemd/system/multi-user.target.wants/gsad.service

      echo "Starting services"
      systemctl start openvassd
      systemctl start openvasmd
      systemctl start gsad

      echo "Update NVT, SCAP and CERT. This can take a while."
      openvas-nvt-sync
      openvas-cert-sync
      sed -i 's/^SPLIT_PART_SIZE=/SPLIT_PART_SIZE=34952/' /usr/local/sbin/openvas-scapdata-sync
      openvas-scapdata-sync

      echo "Create first user admin"
      openvasmd --create-user admin
      openvasmd --user=admin --new-password admin

      echo "Installation finish"
      echo "Login to the Web Interface using
        Username: admin
        Password: admin"


##Manual Installation

###Prerequisites

###Source Code

###Installation

###Configuration

[rpi-image]: https://images.collabora.co.uk/rpi2/jessie-rpi2-20150705.img.gz
[resize]: https://geekpeek.net/resize-filesystem-fdisk-resize2fs/
[rpi-website]: https://www.raspberrypi.org/
[openvas-website]: http://www.openvas.org/
[debian-website]: https://www.debian.org/
[collabora-website]: https://www.collabora.com/
