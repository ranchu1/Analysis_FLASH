def plt_Eos_DTY( r, D, T, Y, title, nfile = 1, optional_legend =''):
    # plot 1D density-temperature-electron fraction data
    import matplotlib.pyplot as plt

    LineTypes = ['solid','dashed','dotted','dashdot']
    LineWeights = [1.0,1.5,1.5]
    
    if (nfile > 1):
        # plot on one figure
        # in case no legend is provided, make it empty
        if(optional_legend ==''):
            optional_legend = [''] * nfile
            
        fig, ax1 = plt.subplots(num=None, figsize=(8,6), dpi=80, facecolor='w', edgecolor='k')
        # --- density ---
        color = 'tab:red'
        ax1.set_xlabel('Radius [cm]')
        ax1.set_ylabel('Density [g cm-3] / Temperature [K]', color=color)
        for ifile in range(nfile):
            ax1.plot(r[ifile], D[ifile], \
                     color=color, \
                     linewidth=LineWeights[ifile%len(LineWeights)], \
                     linestyle=LineTypes[ifile%len(LineTypes)],\
                     label=optional_legend[ifile]+' Density ')
        ax1.set_yscale('log')
        ax1.set_xscale('log')
        ax1.tick_params(axis='y', labelcolor=color)
        # --- temperature
        color = 'tab:green'
        
        for ifile in range(nfile):
            ax1.plot(r[ifile], T[ifile],\
                     color=color, \
                     linewidth=LineWeights[ifile%len(LineWeights)], \
                     linestyle=LineTypes[ifile%len(LineTypes)],\
                     label=optional_legend[ifile]+' Temperature')
        # --- electron fraction
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel('Electron Fraction', color=color)  # we already handled the x-label with ax1
        
        for ifile in range(nfile):
            ax2.plot(r[ifile], Y[ifile], \
                     color=color, \
                     linewidth=LineWeights[ifile%len(LineWeights)], \
                     linestyle=LineTypes[ifile%len(LineTypes)],\
                     label=optional_legend[ifile]+' Electron Fraction')
        ax2.tick_params(axis='y', labelcolor=color)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2,\
                   loc='upper center', bbox_to_anchor=(0.5, 0.8),
           ncol=3 )
        ax1.set_title(title)
        plt.show()
        return
    else:
        # plot on one figure
        fig, ax1 = plt.subplots()
        # --- density ---
        color = 'tab:red'
        ax1.set_xlabel('Radius [cm]')
        ax1.set_ylabel('Density [g cm-3] / Temperature [K]', color=color)
        lns1 = ax1.plot(r, D, color=color, label='Density')
        ax1.set_yscale('log')
        ax1.set_xscale('log')
        ax1.tick_params(axis='y', labelcolor=color)
        # --- temperature
        color = 'tab:green'
        lns2 = ax1.plot(r, T, color=color, label='Temperature')
        # --- electron fraction
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel('Electron Fraction', color=color)  # we already handled the x-label with ax1
        lns3 = ax2.plot(r, Y, color=color, label='Electron Fraction')
        ax2.tick_params(axis='y', labelcolor=color)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        lns = lns1 + lns2 + lns3
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='right')
        ax1.set_title(title)
        plt.show()
        return
    return
 
def plt_array( X, Ys ):
    # plot an array, Ys, with shared x-axis, X
    import matplotlib.pyplot as plt
    
    # plot on one figure
    fig, ax1 = plt.subplots()
    ax1.plot(X, Ys)
    
    return( fig )
    