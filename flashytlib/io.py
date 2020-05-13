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
    import numpy as np

    if( len(filenames) != len(directories) ):
        print('ERROR! Need number of directories = number of filenames ')
        return
    else:
        fnum = len(filenames)

    Energy            = fnum * ['?']
    Radius            = fnum * ['?']
    ZerothMoment      = fnum * [ nSpecies * ['?'] ]
    FirstMoment       = fnum * [ nSpecies * ['?'] ]
    NumberDensity     = fnum * [ nSpecies * ['?'] ]
    EnergyDensity     = fnum * [ nSpecies * ['?'] ]
    FluxDensity       = fnum * [ nSpecies * ['?'] ]
    AverageEnergy     = fnum * [ nSpecies * ['?'] ]
    AverageFluxFactor = fnum * [ nSpecies * ['?'] ]
    Luminosity        = fnum * [ nSpecies * ['?'] ]

    for ifile in range(fnum):
        print(filenames[ifile])
        for iS in range(nSpecies):
            [ NumberDensity[ifile][iS], EnergyDensity[ifile][iS], \
              AverageEnergy[ifile][iS], ZerothMoment[ifile][iS], \
              Energy[ifile], Radius[ifile] ] \
            = fycal.ReadMoment_Zeroth(filenames[ifile], directories[ifile], iSpecies=iS+1)
            [ FluxDensity[ifile][iS], Luminosity[ifile][iS], \
              FirstMoment[ifile][iS], Energy[ifile], Radius[ifile] ] \
            = fycal.ReadMoment_First(filenames[ifile], directories[ifile], iSpecies=iS+1)
            AverageFluxFactor[ifile][iS] \
            = np.true_divide(FluxDensity[ifile][iS],EnergyDensity[ifile][iS])

    return( Energy, Radius, ZerothMoment, FirstMoment, NumberDensity, EnergyDensity, \
            FluxDensity, AverageEnergy, AverageFluxFactor, Luminosity )

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
