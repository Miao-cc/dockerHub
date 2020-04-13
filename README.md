# docker images for fast pulsar searching and timing

## how to create
1. create  pulsarENV
2. create pulsarSEARCH
3. create pulsarTIMING

## Notes
1. pulsarENV

This image is for the base environment. We installed the useful softwate and
python module.

2. pulsarSEARCH

This image is for pulsar search. We installed psrcat, tempo, ubc_AI and presto-3.0.1.

3. pulsarTIMING

This image is for pulsar timing. We installed tempo2, psrchive and dspsr.
Contained pulsar search software also.

4. psrTiming-docker
Old docker iamge. Not needed now.
