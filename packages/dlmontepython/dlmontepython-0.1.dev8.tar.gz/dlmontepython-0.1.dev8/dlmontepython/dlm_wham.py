#!/usr/bin/env python

##############################################
#                                            #
# Weighted Histogram Analysis Utility (WHAU) #
# for combining (H)US FED data of DL_MONTE-2 #
#  (taking input from FEDDAT.???_### files)  #
#                                            #
#  Author: Andrey Brukhno (C) January 2018   #
#          Daresbury Laboratory, SCD, STFC   #
#                                            #
#  based on the WHAM scheme outlined by/in   #
# J.Kastner/WIREs Comput Mol Sci 2011;1:932  #
#                                            #
##############################################

# system modules (for parsing arguments, options, handling I/O files etc)
import os, sys, getopt, glob

import numpy as npy
from numpy import exp, log

#import math
#import matplotlib.pyplot as plt

print("\n##############################################")
print("#                                            #")
print("# Weighted Histogram Analysis Utility (WHAU) #")
print("# for combining (H)US FED data of DL_MONTE-2 #")
print("#  (taking input from FEDDAT.???_### files)  #")
print("#                                            #")
print("#  Author: Andrey Brukhno (C) January 2018   #")
print("#          Daresbury Laboratory, SCD, STFC   #")
print("#                                            #")
print("#  based on the WHAM scheme outlined by/in   #")
print("# J.Kastner/WIREs Comput Mol Sci 2011;1:932  #")
print("#                                            #")
print("##############################################\n")

sname = sys.argv[0]
nargs = len(sys.argv)-1

if nargs < 1:
   print(sys.argv[0]+": at least one argument is expected - full stop!\n")
   sys.exit(2)


def add_fed_window(k, xwin, bwin, pwin, xtot, ptot, pend, dbin, raw, fname) :

# Read in data from a single window & add it to the total(s)

   tinp = npy.loadtxt(fname) #,skiprows=3,comments='#')
   ndat = len(tinp)

   if pend < 0 :
      print("ERROR: negative skip stride: ", pend)
      sys.exit(5)
   elif (ndat-pend*2) < 10 :
      print("ERROR: skipping more than half of sampled bins in set", k)
      print("ERROR: insufficient number of sampled bins (<10) in set", k)
      sys.exit(4)

   if raw and dbin > 1.e-10 :
   
      dxi   = dbin
      xbeg0 = min(tinp[:])
      xend0 = max(tinp[:])
      mbin  = int((xend0+1.e-10)//dxi)+1
      nbin  = int((xbeg0+1.e-10)//dxi)
      xbeg  = float(nbin)*dxi
      xend  = float(mbin)*dxi
      print("\nPreparing binning range on ",k," set with ",ndat," samples :")
      print("data  min & max :",xbeg0,xend0)
      print("range min & max :",xbeg,xend)
      print("bins  min & max :",(float(nbin)+0.5)*dxi,(float(mbin)-0.5)*dxi, \
      "(",nbin,"...",mbin,"->",mbin-nbin,"bins )")

      nbin = mbin - nbin

      hist, bins = npy.histogram(tinp[:], bins=nbin, range=(xbeg,xend)) #, density=True)

      bmin = -1
      bmax = nbin+100
      for i in range(len(hist)) :
         if hist[i] > 0.0 :
            bmax = i
            if bmin == -1 : bmin = i

      xdat = bins[bmin:bmax+1]+0.5*dxi
      pdat = hist[bmin:bmax+1]+1

      ndat = len(xdat)
      bdat = npy.zeros([ndat])

   else :

      xdat = tinp[pend:ndat-pend,0]
      bdat = tinp[pend:ndat-pend,1]
      pdat = tinp[pend:ndat-pend,2]

   ndat-= pend

   xwin.append([])
   bwin.append([])
   pwin.append([])

   xwin[k].extend(xdat)
   bwin[k].extend(bdat)
   pwin[k].extend(pdat)

   ndat-= pend

   xbeg = xdat[0]
   xend = xdat[ndat-1]
   dxi  = xdat[1]-xdat[0]

   bmin = 1.e100

   ntot0= len(xtot)
   if ntot0 > 0 :
      print ("... (ext) filling in arrays for ",k," range: ",xbeg,xend,pend,ndat,len(tinp),len(xtot))
      xbeg = xtot[0]
      xend = xtot[ntot0-1]
   else :
      xtot.extend(xdat)
      ptot.extend(pdat)
      print("... (ini) filling in arrays for ",k," range: ",xbeg,xend,pend,ndat,len(tinp),len(xtot))

      for i in range(ndat): 
         if pdat[i] > 1.e-10 : 
            bdat[i] = -bdat[i]-log(pdat[i]) # unfolded bias
            bmin = min(bmin,bdat[i])

      for i in range(ndat): 
         if pdat[i] > 1.e-10 : 
            bdat[i] -= bmin
            bwin[k][i] = bdat[i]
      return

   xbeg0 = min(xdat[0],xbeg)
   xend0 = max(xdat[ndat-1],xend)

   dxi = xdat[1]-xdat[0]
   dxt = xtot[1]-xtot[0]
   if abs(dxi-dxt) > 1.e-10 :
      print("ERROR: mismatch in bin sizes, dXi /= dXt - ",dxi,"=?=",dxt)
      sys.exit(3)

   for i in range(ndat):
      if pdat[i] > 1.e-10 :
         bdat[i] =-bdat[i]-log(pdat[i]) # unfolded bias
         bmin = min(bmin,bdat[i])

   jo = 0
   jt = 0
   for i in range(ndat):
      if pdat[i] > 1.e-10 : 
         bdat[i] -= bmin

         jt = int((xdat[i]-xbeg0+1.e-10)//dxt)
         if xdat[i] < xbeg :
            print("\nNOTE: windows input files must be sorted in acsending order!\n")
            sys.exit(6)
            #print "adding data at the bot of set",i,xdat[i],i+pend
            xtot.insert(i, xdat[i])
            ptot.insert(i, pdat[i])
         elif xdat[i] > xend :
            #print "adding data at the end of set",len(xtot),xdat[i],i+pend
            xtot.insert(len(xtot), xdat[i])
            ptot.insert(len(ptot), pdat[i])
         else :
            #print "adding data in the mid of set",jt,xdat[i],i+pend
            jo+= 1 
            ptot[jt] += pdat[i]
      
      bwin[k][i] = bdat[i]

   #print "... (tot) filling in arrays for ",k," range: ",xtot[0],xtot[len(xtot)-1],len(xtot),jo


def stitch_fed_windows(tol, mitr, xmin, fwin, pwin, xtot, ptot, fname) :

# Given data in a set of windows, iterate for weights and stitch probabilities into the total one

   nwin = len(pwin)
   ntot = len(ptot)
   porg = [ntot]             # total unfolded prob's
   zsum = [ntot]             # norm for weighted prob's in a window
   zold = [nwin]             # Z's at previous iteration
   zwin = [nwin]             # Z's at current iteration
   porg = npy.zeros([ntot])
   zsum = npy.zeros([ntot])
   zold = npy.ones([nwin])
   zwin = npy.ones([nwin])

   dxt  = xtot[1]-xtot[0]
   xbeg = xtot[0]

   psum = [nwin]
   psum = npy.zeros([nwin])
   for k in range(nwin): 
      psum[k] = sum(pwin[k]) # sum of counts in a window

   delta = 1.0e10
   niter = 0

   while delta > tol and niter < mitr :
       niter += 1

       zsum = npy.zeros([ntot]) # norm for weights in a window
       for k in range(nwin) : 
          zsum += exp(-fwin[k]*(xtot-xmin[k])**2)*psum[k]/zwin[k]

       porg  = (ptot/zsum)*sum(psum/zwin)
       porg /= sum(porg)

       zwin  = npy.zeros([nwin]) # Z's at current iteration
       for k in range(nwin):
          zwin[k] += sum(porg[:]*exp(-fwin[k]*(xtot[:]-xmin[k])**2))

       #zwin /= sum(zwin)

       delta = sum((log(zwin)-log(zold))**2)

       # save weights
       npy.savetxt(fname+'.dat', npy.c_[ xmin[:nwin], -log(zwin/zwin[nwin-1]) ], delimiter='   ')

       zold[:] = zwin[:]

   ptot[:] = porg[:]

   print("\nWHAM done after",niter,"iterations: SUM_win{ [ln(Z_new) - ln(Z_old)]^2 } =",delta)

   if delta > tol : 
      print("\nWHAM iteration finished before reaching the expected accuracy:",tol)


def main(argv):
   dinp = '.'
   finp = 'FEDDAT'
   fius = 'WINDOWS_HUS'
   dout = '.'
   fout = 'WHAMDAT'
   stst = '_TST'
   sfed = '_FED'
   spdf = '_PDF'
   dbin = 0.1
   raw_data = False

   script = argv[0]

   try:
      opts, args = getopt.getopt(argv[1:],"hrd:i:o:s:t:m:b:",["help", "raw", \
      "dir=","inp=","out=","skip=","miter=","toler=","bin="])
   except getopt.GetoptError:
      print("Try: "+script+" --help\n")
      sys.exit(2)

   skip  = 0
   mitr  = 1000
   toler = 1.e-10

   for opt, arg in opts:
      if (opt == '-h' or opt == '--help'):
         print('\n===========')
         print('Main usage:')
         print('===========\n')
         print(script+' [-d <directories>] -i <input> -o <output> -s <n_skip> -m <m_iter> -t <tolerance>\n')
         print('directory(ies) : pattern for input directories to search (optional) [.]')
         print('input  file(s) : pattern for included FEDDAT input files [FEDDAT]')
         print('output file    : output file(s) prefix [WHAMDAT]')
         print('n_skip         : number of bins to remove at the ends in each window [0]')
         print('m_iter         : maximum number of WHAM iterations [1000]')
         print('tolerance      : upper bound for accumulative error [1.e-10]')
         print('\n')
         sys.exit(1)
      elif opt in ("-r", "--raw"):
         raw_data = True
      elif opt in ("-d", "--dir"):
         dinp = arg
      elif opt in ("-i", "--inp"):
         finp = arg
      elif opt in ("-o", "--out"):
         fout = arg
      elif opt in ("-s", "--skip"):
         skip = max(abs(int(arg)),0)
      elif opt in ("-m", "--miter"):
         mitr = max(abs(int(arg)),100)
      elif opt in ("-t", "--toler"):
         toler = min(abs(float(arg)),1.e-5)
      elif opt in ("-b", "--bin"):
         dbin = abs(float(arg))
         raw_data = True

   print("\n",'='*26)
   print("Pattern for input files  : '"+dinp+"/"+finp+"' (see below)")
   print("Prefix for output files  : '"+dout+"/"+fout+"' (with suffices appended)")
   print("End bins skipped per set :",skip)
   print('='*26)
   print("List of input files :\n",'-'*26)
   print("0 : "+fius+" (HUS list)")
   #print "HUS list input file : "+fius

   flist = []
   nwin = 0
   for dn in sorted(glob.iglob(dinp)) :
      if os.path.isdir(dn):
         for fn in sorted(os.listdir(dn)) :
            dfn = str(dn+'/'+fn)
            if os.path.isfile(dfn) and (finp in fn) :
               nwin += 1
               flist.append(dfn)
               print(nwin,":",dfn)

   print('='*26,"\nCollecting the input data...\n",'-'*26)
   
   tinp = npy.loadtxt(fius)
   ninp = len(tinp)
   if ninp < nwin :
      print("ERROR: number of FED files < number of windows in WINDOWS_HUS input : ",nwin,"<?",ninp,"!")
      sys.exit(3)

   xmin = tinp[:,0]
   fwin = tinp[:,1]

   xwin = []
   bwin = []
   pwin = []
   xtot = []
   ptot = []

   for i in range(nwin) :
      add_fed_window(i, xwin, bwin, pwin, xtot, ptot, skip, dbin, raw_data, flist[i])
#      if len(xtot) > 0 : 
#         npy.savetxt(fout+stst+'.inp'+str(i), npy.c_[ xwin[i], bwin[i], pwin[i] ], delimiter='   ')

   if len(xwin) < 2 : 
      print("ERROR: insufficient data, too few windows in US input:",len(xwin),"?< 2")
      sys.exit(3)

   if len(xtot) < 10 : 
      print("ERROR: insufficient data, too few bins in US input:",len(xtot),"?< 10")
      sys.exit(3)

   npy.savetxt(fout+spdf+'.inp', npy.c_[ xtot, ptot/sum(ptot) ], delimiter='   ')

   print('='*26,"\nRunning WHAM iteration...\n",'-'*26)

   stitch_fed_windows(toler, mitr, xmin, fwin, pwin, xtot, ptot, fout+'_WGT')

   ptot /= sum(ptot)
   imin  = -1
   imax  = len(ptot)-1
   if ptot[imax] < 1.e-10 :
      for i in range(len(ptot)) : 
         if ptot[i] > 0.0 : 
            if imin == -1 : imin = i
            imax = i
   imax += 1

   npy.savetxt(fout+sfed+'.out', npy.c_[ xtot[imin:imax], -log(ptot[imin:imax]/ptot[imax-1]), ptot[imin:imax] ], delimiter='   ')
   npy.savetxt(fout+spdf+'.out', npy.c_[ xtot, ptot ], delimiter='   ')

   sys.exit(0)

if __name__ == "__main__":
   main(sys.argv)

sys.exit(0)

