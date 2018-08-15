# Copyright (C) 2016 by Ewan Barr
# Licensed under the Academic Free License version 3.0
# This program comes with ABSOLUTELY NO WARRANTY.
# You are free to modify and redistribute this code as long
# as you do not remove the above attribution and reasonably
# inform receipients that you have modified the original work.

#FROM ubuntu:xenial-20160923.1
FROM ubuntu:18.04

#MAINTAINER Ewan Barr "ebarr@mpifr-bonn.mpg.de"
MAINTAINER Chenchen Miao "miaocc@nao.cas.cn" 
#adopted from Ewan Barr's repo

ENV DEBIAN_FRONTEND=noninteractive

# Switch account to root and adding user accounts and password
USER root
RUN echo "root:root" | chpasswd && \
    mkdir -p /root/.ssh 

# Create psr user which will be used to run commands with reduced privileges.
RUN adduser --disabled-password --gecos 'unprivileged user' psr && \
    echo "psr:psr" | chpasswd && \
    mkdir -p /home/psr/.ssh && \
    chown -R psr:psr /home/psr/.ssh

# Create space for ssh daemon and update the system
#RUN echo 'deb http://us.archive.ubuntu.com/ubuntu trusty main multiverse' >> /etc/apt/sources.list && \
RUN echo 'deb mirror://mirrors.ubuntu.com/mirrors.txt trusty main multiverse' >> /etc/apt/sources.list && \
    mkdir /var/run/sshd && \
    apt-get -y check && \
    apt-get -y update && \
    apt-get install -y apt-utils apt-transport-https software-properties-common  && \
    apt-get -y update --fix-missing && \
    apt-get -y upgrade 

# Install dependencies
RUN apt-get -y update --fix-missing
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get --no-install-recommends -y install \
    build-essential \
    autoconf \
    autotools-dev \
    automake \
    pkg-config \
    csh \
    wget \
    git \
    libcfitsio-dev \
    pgplot5 \
    swig2.0 \    
    python \
    python-dev \
    python-pip \
    python-tk  \
    libfftw3-3 \
    libfftw3-bin \
    libfftw3-dev \
    libfftw3-single3 \
    libx11-dev \
    libpng-dev \
    libpnglite-dev \   
    libglib2.0-0 \
    libglib2.0-dev \
    libblas-dev \
    libgtk3.0-cil-dev \
    gir1.2-gtk-3.0 \
    python-gobject \
    openssh-server \
    libgomp1 \
    openmpi-bin \
    openmpi-common \
    openmpi-doc \
    libpomp-dev \
    libopenmpi-dev \
    libiomp-dev \
    libiomp-doc \
    libiomp5 \
    libiomp5-dbg \
    docker.io \
    libtool  \
    libsysfs-dev \
    xorg \
    openbox \
    imagemagick \
    vim \
    tree \
    screen \
    libgsl-dev \
    libatlas-base-dev \
    liblapack-dev \
    libblas-dev \
    g++-6 \
    gcc-6 \
    gfortran-6 \
    libtmglib-dev 

#RUN apt-get --no-install-recommends -y install \
    #openbox \
    #imagemagick \
    #vim \
    #tree \
    #screen \
    #libgsl-dev \
    #libatlas-base-dev \
    #liblapack-dev \
    #libblas-dev \
    #g++-6 \
    #gcc-6 \
    #gfortran-6 \
    #libtmglib-dev 

RUN rm -rf /var/lib/apt/lists/* 
    

RUN apt-get -y clean

#set gcc, g++ and gfortran version
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-6 50 && \
    update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-6 50 && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 50 

# Install python packages
#RUN pip install  pip setuptools -U  && \
#RUN python -m pip install --upgrade --force pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple setuptools==33.1.1
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -Iv scipy==0.19.0 numpy  matplotlib
#RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -Iv scipy==0.19.0 numpy  matplotlib  pyfits  pywavelets scikit-learn==0.12.1 theano==0.8 pyephem 

# astropy 
#COPY sshd_config /etc/ssh/sshd_config
USER psr

# Define home, psrhome, OSTYPE and create the directory
ENV HOME /home/psr
ENV PSRHOME $HOME/software
ENV OSTYPE linux
RUN mkdir -p $PSRHOME

# PGPLOT
ENV PGPLOT_DIR /usr/lib/pgplot5
ENV PGPLOT_FONT /usr/lib/pgplot5/grfont.dat
ENV PGPLOT_INCLUDES /usr/include
ENV PGPLOT_BACKGROUND white
ENV PGPLOT_FOREGROUND black
ENV PGPLOT_DEV /xs
WORKDIR $PSRHOME

# Pull all repos
# get psrcat tempo presto psrchive
RUN wget http://www.atnf.csiro.au/people/pulsar/psrcat/downloads/psrcat_pkg.tar.gz && \
    tar -xvf psrcat_pkg.tar.gz -C $PSRHOME && \
    wget https://www.imcce.fr/content/medias/recherche/equipes/asd/calceph/calceph-3.1.0.tar.gz && \
    tar -xvf calceph-3.1.0.tar.gz -C $PSRHOME && \
    git clone git://git.code.sf.net/p/tempo/tempo && \
    git clone git://git.code.sf.net/p/psrchive/code psrchive && \
    git clone https://bitbucket.org/psrsoft/tempo2.git tempo2Install
    #git clone https://github.com/zhuww/presto.git && \

#calceph
ENV CALCEPH $PSRHOME/calceph
ENV PATH $PATH:$PSRHOME/calceph
ENV F77 gfortran
WORKDIR $PSRHOME/calceph-3.1.0
RUN ./configure --disable-shared CC=gcc FC=gfortran --prefix=$CALCEPH && \
    make && \
    #make check && \
    make install


# Psrcat
ENV PSRCAT_FILE $PSRHOME/psrcat_tar/psrcat.db
ENV PATH $PATH:$PSRHOME/psrcat_tar
WORKDIR $PSRHOME/psrcat_tar
RUN /bin/bash makeit
#RUN /bin/bash makeit && \
    #rm -f ../psrcat_pkg.tar.gz

# Tempo
ENV TEMPO $PSRHOME/tempo
ENV PATH $PATH:$PSRHOME/tempo/bin
WORKDIR $TEMPO
RUN ls -lrt 
RUN ./prepare && \
    ./configure --prefix=$PSRHOME/tempo && \
    make && \
    make install && \
    rm -rf .git

##TEMPO2
#
ENV TEMPO2 $PSRHOME/tempo2
ENV PATH $PATH:$TEMPO2/bin
ENV PGPLOT_DIR /usr/lib/pgplot5
ENV PGPLOT_FONT /usr/lib/pgplot5/grfont.dat
ENV PSRCAT_FILE $PSRHOME/psrcat_tar/psrcat.db
ENV PYTHONPATH $PYTHONPATH:$PSRCHIVE/lib/python2.7/site-packages
ENV C_INCLUDE_PATH $C_INCLUDE_PATH:$CALCEPH/include
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$CALCEPH/lib
WORKDIR $PSRHOME/tempo2Install
RUN cp $CALCEPH/include/* . && \
     ./bootstrap && \
    cp -r T2runtime $TEMPO2 && \
    ./configure --prefix=$TEMPO2 && \
    make && \
    make install && \
    make plugins && \
    make plugins-install
    #ln -s T2runtime/* $TEMPO2/





#PSRCHiVE
ENV PSRCHIVE $PSRHOME/psrchive
ENV PATH $PATH:$PSRCHIVE/bin
ENV PGPLOT_DIR /usr/lib/pgplot5
ENV PGPLOT_FONT /usr/lib/pgplot5/grfont.dat
ENV PSRCAT_FILE $PSRHOME/psrcat_tar/psrcat.db
ENV PYTHONPATH $PYTHONPATH:$PSRCHIVE/lib/python2.7/site-packages
ENV TEMPO2 $PSRHOME/tempo2
WORKDIR $PSRCHIVE
RUN ./bootstrap && \
    ./configure --prefix=$PSRCHIVE && \
    make && \
    make check && \
    make install

#RUN ENV | awk '{print "export ",$0}' >> $HOME/.profile
COPY bashrc $HOME
RUN cat bashrc >> $HOME/.bashrc

WORKDIR $HOME
USER root
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
