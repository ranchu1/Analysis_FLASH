# ================= Compact ================= #
# --- fun [ Nuclear plot ] --- #
def plt_1D_NuclearComprehensive( chkfilename, weaklibTabDir ):
    import flashytlib.io as fyio
    import matplotlib.pyplot as plt
    
    print('flash5   chk :', chkfilename)
    
    [eosfile,opfiles] = fyio.IO_CheckWeaklibFile(weaklibTabDir,Verbose=False)
    
    # loading density, temperature, electron fraction
    plotvariables = ['r_cm','dens','temp','ye  ']
    nvar = len(plotvariables)
    var_data = nvar * ['?']
    ivar = 0
    for var_name in plotvariables:
        buffdata = fyio.IO_FLASH_1D_1Var(chkfilename, var_name, Verbose=False)
        var_data[ivar] = buffdata
        ivar = ivar + 1
        
    fig = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
    
    # === 1 == rho-temp-ye plot ===== #
    ax1  = fig.add_subplot(2,2,1)
    # --- density ---
    color = 'tab:red'
    ax1.set_xlabel('Radius [cm]')
    ax1.set_ylabel('Density [g cm-3] / Temperature [K]', color=color)
    lns1 = ax1.plot(var_data[0], var_data[1], color=color, label='Density')
    ax1.set_yscale('log')
    ax1.tick_params(axis='y', labelcolor=color)
    # --- temperature
    color = 'tab:green'
    lns2 = ax1.plot(var_data[0], var_data[2], color=color, label='Temperature')
    # --- electron fraction
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Electron Fraction', color=color)  # we already handled the x-label with ax1
    lns3 = ax2.plot(var_data[0], var_data[3], color=color, label='Electron Fraction')
    ax2.tick_params(axis='y', labelcolor=color)
    # -- finalize
    time = fyio.IO_FLASH_Time( chkfilename )
    plt.title(' t = %.4f'%(time)+'s ')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    lns = lns1 + lns2 + lns3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='right')
    
    ax2  = fig.add_subplot(2,2,2)
    
    ax3  = fig.add_subplot(2,2,3)
    ax4  = fig.add_subplot(2,2,4)
    
    # ===== adjust ===== #
    plt.subplots_adjust(left = 0.125,  # the left side of the subplots of the figure
                        right = 0.9,   # the right side of the subplots of the figure
                        bottom = 0.1,  # the bottom of the subplots of the figure
                        top = 0.9,     # the top of the subplots of the figure
                        wspace = 0.4,  # the amount of width reserved for space between subplots,
                        hspace = 0.4)  # the amount of height reserved for space between subplots
    plt.show()
    
# --- fun [ Eos plot ] --- #
def plt_1D_Eos( filename, optional_title='' ):
    import flashytlib.io as fyio
    import matplotlib.pyplot as plt
    import flashytlib.plot_basis as fypltb
    
    # loading density, temperature, electron fraction
    plotvariables = ['r_cm','dens','temp','ye  ']
    nvar = len(plotvariables)
    var_data = nvar * ['?']
    ivar = 0
    for var_name in plotvariables:
        buffdata = fyio.IO_FLASH_1D_1Var(filename, var_name, Verbose=False)
        var_data[ivar] = buffdata
        ivar = ivar + 1

    fypltb.plt_Eos_DTY( var_data[0], var_data[1], var_data[2], var_data[3], optional_title )        

    # --- fun [ Eos plot ] --- #
def plt_1D_Eos_multi( filenames, optional_title='', optional_legend = ''):
    import flashytlib.io as fyio
    import matplotlib.pyplot as plt
    import flashytlib.plot_basis as fypltb
    
    # loading density, temperature, electron fraction
    nfile = len(filenames)
    plotvariables = ['r_cm','dens','temp','ye  ']
    nvar  = len(plotvariables) * nfile
    var_data = nvar * ['?']
    ivar = 0
    
    for var_name in plotvariables:
        for ifile in range(nfile):
            buffdata = fyio.IO_FLASH_1D_1Var(filenames[ifile], var_name, Verbose=False)
            var_data[ivar] = buffdata
            ivar = ivar + 1
    
    fypltb.plt_Eos_DTY( \
                       var_data[0:nfile], \
                       var_data[nfile:2*nfile], \
                       var_data[2*nfile:3*nfile],\
                       var_data[3*nfile:4*nfile], \
                       optional_title, nfile = nfile, \
                       optional_legend = optional_legend ) 

# --- fun [ Number Density plot ] --- #
def plt_1D_NumberDensity( filename ):
    # plot number density N
    # integrate t001... (J) in chk and plot
    import flashytlib.calculator as fycal
    import flashytlib.plot as fyplt

    [NumberDensity, EnergyDensity, J, ECenter, Radius] = fycal.ReadMoment_Zeroth(filename)
    fyplt.arrayplot(Radius, NumberDensity,'linear','log','Radius [cm]','Number Density')


# ================ Basic ================= #

# --- fun [ matrix plot ] --- #
def matrixplot( TwoD_data, xTickLable=['x'], yTickLable=['y'] ):
    import matplotlib.pyplot as plt
  
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(TwoD_data, interpolation='nearest')
    fig.colorbar(cax)
  
    ax.set_xticklabels(['']+xTickLable)
    ax.set_yticklabels(['']+yTickLable)
  
    plt.show()
  
    return

# --- fun [ 1D array plot ] --- #
def arrayplot( OneD_data_X, OneD_data_Y, XLogFlag, YLogFlag, xLable=['x'], yLable=['y'], figflag=False ):
    import matplotlib.pyplot as plt
    
    if( figflag == False ):
        fig = plt.figure(num=None, figsize=(5, 5), dpi=80, facecolor='w', edgecolor='k')
        ax = fig.add_subplot(111)
    else:
        fig = figflag
        ax = fig.add_subplot(2,1,2)
 
    
    plt.plot(OneD_data_X,OneD_data_Y)
    
    ax.set_xscale(XLogFlag)
    ax.set_yscale(YLogFlag)
    
    plt.xlabel(xLable)
    plt.ylabel(yLable)
  
    plt.show()
  
    return( fig )
