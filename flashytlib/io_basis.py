def IO_FLASHStandardProfile( filename ):
    # reader for FLASH5 standard profile
    import numpy as np

    print('Reading ', filename, ' ...')

    f = open(filename)
    # Data information line
    line = f.readline()
    # number of variables line
    line = f.readline()
    # number of data line
    line = f.readline()
    # variables name
    cha_dens = f.readline()
    cha_temp = f.readline()
    cha_ye   = f.readline()
    # read data 
    lines = f.readlines()
    temp_radi = [line.split()[0] for line in lines]
    temp_dens = [line.split()[1] for line in lines]
    temp_temp = [line.split()[2] for line in lines]
    temp_ye   = [line.split()[3] for line in lines]

    radius = np.asarray([float(i) for i in temp_radi])
    dens   = np.asarray([float(i) for i in temp_dens])
    temp   = np.asarray([float(i) for i in temp_temp])
    ye     = np.asarray([float(i) for i in temp_ye])

    f.close()

    return( radius, dens, temp, ye )
   
# --- fun [ check files under directory ] --- #
def IO_CheckFile( Dir, Verbose=False ):
    import glob

    filelist = glob.glob(Dir+"*")
    if (Verbose) :
        for f in filelist:
            print(f)

    return( filelist ) 

# --- search parameter files for energy setting -- #
def IO_CheckESetting( filename, Verbose=False):
    """ search parfile for eR, eL and zoomE
    need parfilename as input """
    import os.path

    if os.path.isfile(filename):
        print ("File exist")
        f = open(filename)
        info = f.readlines()
        for i in info:
            if (i[0:5] == 'rt_eL'):
                eL = float(i.split()[2])
                if (Verbose) :
                    print(i,' => eL = ',eL)
            if (i[0:5] == 'rt_eR'):
                eR = float(i.split()[2])
                if (Verbose) :
                    print(i,' => eR = ',eR)
            if (i[0:8] == 'rt_zoomE'):
                zoomE = float(i.split()[2])
                if (Verbose) :
                    print(i,' => zoomE = ',zoomE)
        f.close()
    else:
        print ("File not exist")

    return( eL, eR, zoomE )
