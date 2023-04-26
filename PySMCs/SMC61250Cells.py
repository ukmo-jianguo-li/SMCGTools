"""
#; Adapted to generate G6-25kmSMCels from ASCII Bathymetry files. 
#;                                   JGLi18Sep2014
#; Adapted for global 6-12-25-50 km SMC grid for CMA model. JGLi10Aug2018 
#; Converted from IDL into Python code.    JGLi14Feb2019 
#; Rectify size-1 cell bug and re-generate 6-50 cels.  JGLi04May2021 
#; Modified for SMCGTools to generate sample 6-50 cells.  JGLi06Oct2021 
#;
"""
 
def main():
    """ SMC61250Cells.py to generate the 6-50 km cells. """

##  Import relevant modules and functions
    import numpy as np

    from readtext  import readtext
    from smcellgen import smcellgen

    print( " Program to generate SMC61250 grid cell array. " )

#; Open the 6km global Bathymetry data file
    Wrkdir='./'
    Bathyfile ='../Bathys/Glob6kmBathy.dat'

    headrs, bathyin = readtext( Bathyfile, skiprows=[0,1] )
    NLon =   int( headrs[0] )
    NLat =   int( headrs[1] )
    FLon = float( headrs[2] )
    FLat = float( headrs[3] )
    DLon = float( headrs[4] )
    DLat = float( headrs[5] )

    print (' NLon, NLat, FLat, FLon, DLat, DLon = ') 
    print (  NLon, NLat, FLat, FLon, DLat, DLon )

##  As formated input was read as a table of 2-D arrays 
##  and black spaces in the table are changed into none
##  the read array need to be reshaped to original shape
##  and trailing nones are removed.
    nrocos = bathyin.shape
    ncolin = nrocos[0]*nrocos[1]//NLat
    Bathy = bathyin.reshape((NLat,ncolin))[:,:NLon]
    print (' Coverted Bathy shape =', Bathy.shape )

##  Pack bathy parameters into one list.
    ndzlonlat=[ NLon, NLat, DLon, DLat, FLon, FLat ]

##  Set SMC grid parameters.
    NRLv = 4
    ZLon = 0.0
    ZLat = 0.0
    Depmin= 0.0
    Global= True
    Arctic= True
    GridNm='SMC61250'

    mlvlxy0 = [ NRLv, ZLon, ZLat ]

    smcellgen(Bathy, ndzlonlat, mlvlxy0, FileNm=Wrkdir+GridNm, 
              Global=Global, Arctic=Arctic, depmin=Depmin)

##  Save SMC grid information for later use.
    flxy = open(Wrkdir+GridNm+"GInfo.txt", 'w')
    flxy.writelines(" SMC grid parameters for "+GridNm+" \n")
    flxy.writelines(" NLon, NLat= %d, %d \n" % (NLon, NLat) )
    flxy.writelines(" DLon, DLat= %f, %f \n" % (DLon, DLat) )
    flxy.writelines(" ZLon, ZLat= %f, %f \n" % (ZLon, ZLat) )
    flxy.writelines(" NRLv, MFct= %d, %d \n" % (NRLv, 2**(NRLv-1)) )
    flxy.writelines(" Global, Arctic= %s, %s \n" % (Global, Arctic) )
    flxy.writelines(" End of SMC grid information. \n")
    flxy.close()

##  End of SMC61250Cels.py


if __name__ == '__main__':
    main()

