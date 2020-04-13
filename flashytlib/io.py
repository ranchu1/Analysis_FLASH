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
    # give the list of unk in a FLASH chk file
    # and nPointsE
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
def IO_FLASH_Time( filename ):
    ## read time
    import h5py

    f = h5py.File(filename, 'r')
    real_scalars = f['real scalars']
    f_time = real_scalars[0][1]
    return( f_time )

# ------------------------------------------------------------
def IO_FLASH_1D_1Var( filename, str_var, Verbose ):
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
