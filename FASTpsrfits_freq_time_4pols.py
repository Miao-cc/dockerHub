import numpy as np 
#import pyfits
import astropy.io.fits as pyfits
import os
import datetime
import time
import sys
from array import array
from pylab import *

##############################################################
# Adapted from Downsamp_FASTpsrfits_freq_time_4pol.py
# 
# Output data for a selected time & freq. range and frequency downsampling rate in Fits format.
# (Output 4 pols Fits format as input datafile)
#
# Miaocc 2019/10/16
##############################################################

if (len(sys.argv)<6 or len(sys.argv)>7):
  	print '\n','Input error!','\n'
  	print '# Example:'
 	print '   python Downsamp_FASTpsrfits_freq_time_4pol.py startchan endchan startn endn xxx.fits'
	print 'or python Downsamp_FASTpsrfits_freq_time_4pol.py startchan endchan startn endn Fdsamp xxx.fits'
	print '(Fdsamp is downsampling rate on frequency channels, unit in 2^n)','\n'
	sys.exit()
elif len(sys.argv) == 6:
	startfreq=int(sys.argv[1])
	endfreq=int(sys.argv[2])
	startn=int(sys.argv[3])
	endn=int(sys.argv[4])
	filename=sys.argv[5]
	Fdsamp=1
elif len(sys.argv) == 7:
	startfreq=int(sys.argv[1])
	endfreq=int(sys.argv[2])
	startn=int(sys.argv[3])
	endn=int(sys.argv[4])
	Fdsamp=int(sys.argv[5])
	filename=sys.argv[6]

starttime=datetime.datetime.now()
linenum=endn-startn+1
chnum=endfreq-startfreq+1

Fdsamp=1
if chnum%Fdsamp != 0:
	print '\n','# Error! The input of "endfreq-startfreq+1" not be divided by "Fdsamp" !','\n'
	sys.exit()

fileroot=filename[0:-5]
print fileroot, ', Downsampling rate =', Fdsamp

hdulist = pyfits.open(filename)
hdu0 = hdulist[0]
data0 = hdu0.data
header0 = hdu0.header
print data0
hdu1 = hdulist[1]
data1 = hdu1.data
header1 = hdu1.header

float_data=np.array(data1['DATA'])

print "+++++++++++++++++++++++++output1"
print float_data[0,0:100,0,startfreq,0]

temp_float_dat_scl=np.array(data1['DAT_SCL'])
nline=header1['NAXIS2']
nsblk=header1['NSBLK']
tbin=header1['TBIN']
npol=header1['NPOL']
nsuboffs=header1['NSUBOFFS']
chan_bw=header1['CHAN_BW']
freq=header0['OBSFREQ']
nchan=header0['OBSNCHAN']
print 'Input  Number of subints =', size(temp_float_dat_scl)/npol/nchan, nline
print '       Num polarisations =', npol
print '       Ntsamp each subint=', nsblk, size(float_data)/nline/npol/nchan, size(float_data)/nline/nchan/npol
print '       Central freq(MHz) =', freq
print '       Freq. bandwidth   =', header0['OBSBW']
print '       Channel number    =', nchan
print '       Channel width(MHz)=', chan_bw
print '       data1[\'DATA\']     =', float_data.shape
hdu0.header['OBSFREQ']=((endfreq-startfreq+1)/2.+startfreq)*chan_bw + freq - header0['OBSBW']/2.
hdu0.header['OBSBW']=chnum*chan_bw*1.0
hdu0.header['OBSNCHAN']=chnum/Fdsamp*1.0
print 'Output Number of subints =', linenum
print '       Ntsamp each subint=', 'Same as input'
print '       Central freq(MHz) =', hdu0.header['OBSFREQ']
print '       Freq. bandwidth   =', hdu0.header['OBSBW']
print '       Channel number    =', hdu0.header['OBSNCHAN']
print '       Channel width(MHz)=', hdu0.header['OBSBW']/hdu0.header['OBSNCHAN'], chan_bw*Fdsamp*1.0

float_tsubint=np.array(data1['TSUBINT'])[startn:endn+1]
float_offs_sub=np.array(data1['OFFS_SUB'])[startn:endn+1]
float_lst_sub=np.array(data1['LST_SUB'])[startn:endn+1]
float_ra_sub=np.array(data1['RA_SUB'])[startn:endn+1]
float_dec_sub=np.array(data1['DEC_SUB'])[startn:endn+1]
float_glon_sub=np.array(data1['GLON_SUB'])[startn:endn+1]
float_glat_sub=np.array(data1['GLAT_SUB'])[startn:endn+1]
float_fd_ang=np.array(data1['FD_ANG'])[startn:endn+1]
float_pos_ang=np.array(data1['POS_ANG'])[startn:endn+1]
float_par_ang=np.array(data1['PAR_ANG'])[startn:endn+1]
float_tel_az=np.array(data1['TEL_AZ'])[startn:endn+1]
float_tel_zen=np.array(data1['TEL_ZEN'])[startn:endn+1]
#float_aux_dm=np.array(data1['AUX_DM'])[startn:endn+1]
#float_aux_rm=np.array(data1['AUX_RM'])[startn:endn+1]

float_dat_freq=np.zeros([linenum, chnum/Fdsamp])
float_dat_wts=np.zeros([linenum, chnum/Fdsamp])
float_dat_offs=np.zeros([linenum,npol*chnum/Fdsamp])
float_dat_scl=np.zeros([linenum,npol*chnum/Fdsamp])

float_dat_freq=np.array(data1['DAT_FREQ'])[startn:endn+1,startfreq:endfreq+1].reshape(linenum,chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
float_dat_wts=np.array(data1['DAT_WTS'])[startn:endn+1,startfreq:endfreq+1].reshape(linenum,chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
for ipol in range(npol):
	temp_float_dat_offs=np.array(data1['DAT_OFFS']).reshape(nline,npol,nchan)
	float_dat_offs[:,ipol*chnum/Fdsamp:(ipol+1)*chnum/Fdsamp]=temp_float_dat_offs[startn:endn+1,ipol,startfreq:endfreq+1].reshape(linenum,chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
	temp_float_dat_scl=np.array(data1['DAT_SCL']).reshape(nline,npol,nchan)
	float_dat_scl[:,ipol*chnum/Fdsamp:(ipol+1)*chnum/Fdsamp]=temp_float_dat_scl[startn:endn+1,ipol,startfreq:endfreq+1].reshape(linenum,chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
	print 'ipol = ', ipol
	print 'shape of float_dat_offs =', float_dat_offs.shape
	print 'shape of float_dat_scl =', float_dat_scl.shape

temp_data2=np.zeros([nsblk*npol*chnum/Fdsamp],dtype='uint8')
float_data2=np.zeros([linenum,nsblk,npol,chnum/Fdsamp,1],dtype='uint8')
#dataformat=str(size(float_data2)/linenum/Fdsamp)+'B'
dataformat=str(nsblk*npol*chnum/Fdsamp)+'B'


#print dataformat,(float_data2).shape

#for i in range(linenum):
	#temp_data=float_data[i+startn,:].reshape([size(float_data[i+startn,:])/nsblk/nchan/npol,nsblk,npol,nchan])
	#aaaaa=float_data[i+startn,:].shape
	#print i, startn,aaaaa,'shape of temp_data =', temp_data.shape,temp_data[:,:,1,startfreq:endfreq+1].shape
	#for jpol in range(npol):
		#temp_data2[ipol*nsblk*chnum/Fdsamp:(ipol+1)*nsblk*chnum/Fdsamp]=temp_data[:,:,jpol,startfreq:endfreq+1].reshape(nsblk*chnum/Fdsamp,Fdsamp).sum(axis=-1)/Fdsamp
	
	#float_data2[i, :]=temp_data2.reshape(nsblk,npol,chnum/Fdsamp)
print "shape"
print float_data.shape
print startfreq-endfreq-1, chnum
for i in range(linenum):
    for jpol in range(npol):
        float_data2[i,:,jpol,:,:]=float_data[i,:,jpol,startfreq:endfreq+1,:]


float_dataf=float_data2
print "Shape of float data: ", float_dataf.shape
print float_dataf[0,0:100,0,0,0]

#dataformat=str(size(float_data)/nline/nchan*chnum/Fdsamp)+'E'
dataformat2=str(chnum/Fdsamp)+'E'
dataformat3=str(npol*chnum/Fdsamp)+'E'
print dataformat,dataformat2,dataformat3
dataDim = '(1,'+str(chnum)+','+str(npol)+','+str(nsblk)+')'
print "out data dim: ", dataDim

#column1_data = pyfits.Column(name='INDEXVAL',format='1D',array=float_indexval)
column2_data = pyfits.Column(name='TSUBINT',format='1D',array=float_tsubint,unit='s')
column3_data = pyfits.Column(name='OFFS_SUB',format='1D',array=float_offs_sub,unit='s')
column4_data = pyfits.Column(name='LST_SUB',format='1D',array=float_lst_sub,unit='s')
column5_data = pyfits.Column(name='RA_SUB',format='1D',array=float_ra_sub,unit='deg')
column6_data = pyfits.Column(name='DEC_SUB',format='1D',array=float_dec_sub,unit='deg')
column7_data = pyfits.Column(name='GLON_SUB',format='1D',array=float_glon_sub,unit='deg')
column8_data = pyfits.Column(name='GLAT_SUB',format='1D',array=float_glat_sub,unit='deg')
column9_data = pyfits.Column(name='FD_ANG',format='1E',array=float_fd_ang,unit='deg')
column10_data = pyfits.Column(name='POS_ANG',format='1E',array=float_pos_ang,unit='deg')
column11_data = pyfits.Column(name='PAR_ANG',format='1E',array=float_par_ang,unit='deg')
column12_data = pyfits.Column(name='TEL_AZ',format='1E',array=float_tel_az,unit='deg')
column13_data = pyfits.Column(name='TEL_ZEN',format='1E',array=float_tel_zen,unit='deg')
#column14_data = pyfits.Column(name='AUX_DM',format='1E',array=float_aux_dm)
#column15_data = pyfits.Column(name='AUX_RM',format='1E',array=float_aux_rm)
column16_data = pyfits.Column(name='DAT_FREQ',format=dataformat2,array=float_dat_freq,unit='deg')
column17_data = pyfits.Column(name='DAT_WTS',format=dataformat2,array=float_dat_wts,unit='deg')
column18_data = pyfits.Column(name='DAT_OFFS',format=dataformat3,array=float_dat_offs,unit='deg') 
column19_data = pyfits.Column(name='DAT_SCL',format=dataformat3,array=float_dat_scl,unit='MHz')

#column20_data = pyfits.Column(name='DATA',format=dataformat,array=float_dataf,unit='Jy')
column20_data = pyfits.Column(name='DATA',format=dataformat,dim=dataDim,array=float_dataf,unit='Jy')
print '       float_dataf    =', float_dataf.shape

#table_hdu = pyfits.new_table([column2_data,column3_data,column4_data,column5_data,column6_data,column7_data,column8_data,column9_data,column10_data,column11_data,column12_data,column13_data,column16_data,column17_data,column18_data,column19_data,column20_data])
table_hdu = pyfits.BinTableHDU.from_columns([column2_data,column3_data,column4_data,column5_data,column6_data,column7_data,column8_data,column9_data,column10_data,column11_data,column12_data,column13_data,column16_data,column17_data,column18_data,column19_data,column20_data])

table_hdu.header.append(('INT_TYPE','TIME','Time axis (TIME, BINPHSPERI, BINLNGASC, etc)'))
table_hdu.header.append(('INT_UNIT','SEC','Unit of time axis (SEC, PHS (0-1),DEG)'))
table_hdu.header.append(('SCALE','FluxDec','Intensiy units (FluxDec/RefFlux/Jansky)'))
table_hdu.header.append(('NPOL',npol,'Nr of polarisations'))
table_hdu.header.append(('POL_TYPE','AABBCRCI','Polarisation identifier (e.g., AABBCRCI, AA+BB)'))
table_hdu.header.append(('TBIN',tbin,'[s] Time per bin or sample'))
table_hdu.header.append(('NBIN',1,'Nr of bins (PSR/CAL mode; else 1)'))
table_hdu.header.append(('NBIN_PRD',0,'Nr of bins/pulse period (for gated data)'))
table_hdu.header.append(('PHS_OFFS',0.0,'Phase offset of bin 0 for gated data'))
table_hdu.header.append(('NBITS',8,'Nr of bits/datum (SEARCH mode "X" data, else 1)'))
table_hdu.header.append(('NSUBOFFS',nsuboffs,'Subint offset (Contiguous SEARCH-mode files)'))
table_hdu.header.append(('NCHAN',chnum/Fdsamp,'Number of channels/sub-bands in this file'))
table_hdu.header.append(('CHAN_BW',chan_bw*Fdsamp*1.0,'[MHz] Channel/sub-band width'))
table_hdu.header.append(('NCHNOFFS',0,'Channel/sub-band offset for split files'))
table_hdu.header.append(('NSBLK',nsblk,'Samples/row (SEARCH mode, else 1)'))
table_hdu.header.append(('extname','subint  ','name of this binary table extension'))

hdulist2 = pyfits.HDUList([hdu0,table_hdu])
outname1=fileroot+'_4pols_'+sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'.fits'
rmcomm1='rm -f '+outname1
os.system(rmcomm1)


print "++++++++++++++++++++++++++++++++++++++++++++++=="
print "out File header:"
hdutmp = hdulist2[1]
datatmp = hdutmp.data
float_datatmp=np.array(datatmp['DATA'])
print float_datatmp.shape
print "++++++++++++++++++++++++++++++++++++++++++++++=="


hdulist2.writeto(outname1)

print '--------------------------------------------'
print '             Finished!                      '
endtime=datetime.datetime.now()
print 'START:',starttime
print 'END:',endtime
duration=endtime-starttime
print 'DURATION:',duration.seconds,' sec'
