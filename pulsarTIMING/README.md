We had installed psrcat, tempo, presto-3.0.1, tempo2, psrchive, dspsr

# build pulsar base image
docker build -f Dockerfile_fast.timing -t fast_psr:timing .

# create container
./start.py docker-compose.yml

Or 

docker run -it -p 2224:22 -v ./:/work --name fast_pulsar_timing fast_psr:timing /bin/bash

##login to the container 
ssh -X -p 2224 psr@localhost

passwd: psr

Note:

If you want to create this image, you need to copy the fast2gps.clk to this
folder.

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
