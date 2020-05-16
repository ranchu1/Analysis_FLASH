def IO_GetMoments_n_ComputeMeanVars( filenames, directories, nSpecies ):
    """
    assumed 1D data, N filename = N directory
    input  : filenames, directories, nSpecies
    output : Energy, Radius, 
             ZerothMoment, FirstMoment, 
             NumberDensity, EnergyDensity, FluxDensity, 
             AverageEnergy, AverageFluxFactor, Luminosity
    """
    import flashytlib.calculator as fycal
    import flashytlib.io as fyio
    import numpy as np

    if( len(filenames) != len(directories) ):
        print('ERROR! Need number of directories = number of filenames ')
        return
    else:
        fnum = len(filenames)

    Times = fyio.IO_FLASH_Time(filenames)
  
    # first file read in
    for ifi in range(fnum):
        for iS in range(nSpecies):
            
            [NumDen1, EneDen1, AveEng1, ZerMom1, Ene1, Rad1] \
            = fycal.ReadMoment_Zeroth(filenames[ifi], directories[ifi], iSpecies=iS+1)
            
            [FluDen1, Lum1, FirMom1, Ene1, Rad1 ] \
            = fycal.ReadMoment_First(filenames[ifi], directories[ifi], iSpecies=iS+1)

            AveFlu1 = np.true_divide(FluDen1,EneDen1)

            if(iS == 0) : # make a list if not
                NumDen2 = [NumDen1]
                EneDen2 = [EneDen1]
                AveEng2 = [AveEng1]
                ZerMom2 = [ZerMom1]
                FluDen2 = [FluDen1]
                Lum2    = [Lum1]
                FirMom2 = [FirMom1]
                AveFlu2 = [AveFlu1]
                
            if (iS == 1 ): # add an element to list
                NumDen2.append(NumDen1)
                EneDen2.append(EneDen1)
                AveEng2.append(AveEng1)
                ZerMom2.append(ZerMom1)
                FluDen2.append(FluDen1)
                Lum2.append(Lum1)
                FirMom2.append(FirMom1)
                AveFlu2.append(AveFlu1)
                
        if( ifi == 0 ):
            Energy = [Ene1]
            Radius = [Rad1]
            NumberDensity = [NumDen2]
            EnergyDensity = [EneDen2]
            AverageEnergy = [AveEng2]
            ZerothMoment  = [ZerMom2]
            FluxDensity   = [FluDen2]
            Luminosity    = [Lum2]
            FirstMoment   = [FirMom2]
            AverageFluxFactor = [AveFlu2]
        else:
            Energy.append(Ene1)
            Radius.append(Rad1)
            NumberDensity.append(NumDen2)
            EnergyDensity.append(EneDen2)
            AverageEnergy.append(AveEng2)
            ZerothMoment.append(ZerMom2)
            FluxDensity.append(FluDen2)
            Luminosity.append(Lum2)
            FirstMoment.append(FirMom2)
            AverageFluxFactor.append(AveFlu2)

    print('shape Times  [nfum]',np.shape(Times))
    print('shape Energy [nfum,nE]',np.shape(Energy))
    print('shape Radius [nfum,nR]',np.shape(Radius))
    print('shape NumbDe [nfum,nS,nR]',np.shape(NumberDensity))
    #print('shape Moment [nfum,nS,nR,nE]',np.shape(ZerothMoment))
    
    return( Times, Energy, Radius, ZerothMoment, FirstMoment, NumberDensity, \
           EnergyDensity, FluxDensity, AverageEnergy, AverageFluxFactor, Luminosity )

# --- fun [ check files under directory ] --- #
def IO_CheckWeaklibFile( Dir, Verbose=False ):
    import flashytlib.io_basis as fyiob
 
    filelist = fyiob.IO_CheckFile(Dir)
    
    opfiles = 4*['']
    
    for f in filelist:
        for ii in range(len(f)):
            if(f[ii:ii+6] == 'wl-EOS'):
                eosfile = f
        if(f[len(f)-7:len(f)] == 'AbEm.h5'):
            opfiles[0] = f
        if(f[len(f)-7:len(f)] == '-Iso.h5'):  
            opfiles[1] = f
        if(f[len(f)-7:len(f)] == '-NES.h5'):
            opfiles[2] = f
        if(f[len(f)-7:len(f)] == 'Pair.h5'):  
            opfiles[3] = f   

    if (Verbose) :
        print('eos = ', eosfile)
        print('ops = ', opfiles)
        
    return(eosfile,opfiles)
        
# --- fun [ determine nPointsE ] --- #
def IO_FLASH_nPointsE( filename ):
    """ gives the nPointsE in the checkpoint file
    assumed nNodeX = nNodeE = 2, nSpecies = 2
    input  : filename
    output : nPointsE
    """
    import h5py

    encoding = 'utf-8'
    f = h5py.File(filename, 'r') 
    unknown_names = f['unknown names']
    #print(len(unknown_names),' in unk list' )
    thornado_var_num = 0
    for unknown in unknown_names:
        str_unknown = str(unknown, encoding)
        if( str_unknown[0] == 't' ):
            if( str_unknown[1] >= '0' and str_unknown[1] <= '9' ):
                thornado_var_num = thornado_var_num + 1
    
    #print( thornado_var_num,' moments variables and each moment component has', 
    #       thornado_var_num/4, ' Nodes' ) 
    #print( ' with nNodeX = 2, nNodeE = 2, it indicates nPointsE =', thornado_var_num/16 )
    return( thornado_var_num/16 )

# ------------------------------------------------------------
def IO_FLASH_Time( filenames ):
    """ return files' time
    input  : filenames
    output : f_time
    """
    import h5py

    numfile = len(filenames)
    times = ['?'] * numfile
    for i in range(numfile):
       f = h5py.File(filenames[i], 'r')
       real_scalars = f['real scalars']
       f_time   = real_scalars[0][1]
       f_time   = float(f_time)
       times[i] = f_time

    return( times )

# ------------------------------------------------------------
def IO_FLASH_1D_1Var( filename, str_var, Verbose ):
    """
    input  : filename, str variablename
    output : variable data
    """
    import h5py
    import numpy as np
    import matplotlib.pyplot as plt
    
    encoding = 'utf-8'
    
    data_var = 0.0
    
    f = h5py.File(filename, 'r')   
    ## read time
    real_scalars = f['real scalars']
    f_time = real_scalars[0][1]
    if Verbose: print( filename, ' time =', f_time ,' s', ', ploting ', str_var, '...')
    
    ## look up if variable is in UNK list
    index_var = -1 # default for [not found]
    if( str_var == 'r_cm' ): 
        index_var = 0 # default for [radius]
    else:
        unknown_names = f['unknown names']
        for unknown in unknown_names:
            str_unknown = str(unknown, encoding)
            if( str_unknown == str_var ): 
                index_var = 1 # default for [knowns]
                break
    if( index_var == -1 ): 
        print('Error: unknown variables !', str_var )
        print('Known :',unknown_names)
        
    if( index_var >= 0 ): # look into dataset
        ## read block numbers and parameters
        integer_scalars = f['integer scalars']
        nxb = integer_scalars[0][1]
        global_block = integer_scalars[4][1]
        gsurr_blks = f['gsurr_blks']
        which_child = f['which child']
        block_size = f['block size']
        bounding_box = f['bounding box']
        ## count how many meaningful blocks
        blk_count = 0
        for ii in range(len(which_child[:])):
            if (gsurr_blks[ii,0,0,1,1] == 1 ):
                blk_count = blk_count + 1
        ## initial output data_var
        data_var = np.zeros(nxb*blk_count)
        ## feed in data
        if (index_var == 0): # for radius
            ii_count = -1
            for ii in range(global_block):
                if (gsurr_blks[ii,0,0,1,1] == 1):
                    ii_count = ii_count + 1
                    for jj in range(nxb): # over subcell [8]
                        kk = jj + ii_count * nxb
                        dsubcell = block_size[ii,0]/nxb
                        data_var[kk] = bounding_box[ii,0,0] + dsubcell * (jj+0.5)
        elif (index_var == 1): # for other variables
            data_buff = f[str_var]
            ii_count = -1
            for ii in range(global_block):
                if (gsurr_blks[ii,0,0,1,1] == 1):
                    ii_count = ii_count + 1
                    for jj in range(nxb): # over subcell [8]
                        kk = jj + ii_count * nxb
                        data_var[kk] = data_buff[ii,0,0,jj]
    
    return( data_var )
   
# ============= Need Development ================ #
        
# ------------------------------------------------------------
def IO_FLASH_1D_VarArr( ):
    print('Nothing')
    
