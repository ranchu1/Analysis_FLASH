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
