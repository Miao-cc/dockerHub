We had installed psrcat, tempo, presto-3.0.1, ubc_AI

# build pulsar base image
docker build -f Dockerfile_fast.search -t fast_psr:search .


# create container
./start.py docker-compose.yml

Or 

docker run -it -p 2223:22 -v ./:/work --name fast_pulsar_search fast_psr:search /bin/bash

##login to the container 
ssh -X -p 2223 psr@localhost

passwd: psr

--------------------------------------------------------------------------------
All this will need root
So login root by
    docker exec -it container-name /bin/bash


######
There will some errors when login in
1. X11 forwarding request failed on channel 0

    https://www.cyberciti.biz/faq/how-to-fix-x11-forwarding-request-failed-on-channel-0/
    
    In Ubuntu is not 'sshd' but 'ssh'
    So please run
    /etc/init.d/ssh reload

2. "X11 proxy: wrong authorisation protocol attempted"
    cp /home/psr/.Xauthority /root/

