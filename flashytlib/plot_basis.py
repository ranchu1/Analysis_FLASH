def plt_Eos_DTY( r, D, T, Y ):
    # plot 1D density-temperature-electron fraction data
    import matplotlib.pyplot as plt

    # plot on one figure
    fig, ax1 = plt.subplots()
    # --- density ---
    color = 'tab:red'
    ax1.set_xlabel('Radius [cm]')
    ax1.set_ylabel('Density [g cm-3] / Temperature [K]', color=color)
    lns1 = ax1.plot(r, D, color=color, label='Density')
    ax1.set_yscale('log')
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

    plt.show()
    
    return
 
def plt_array( X, Ys ):
    # plot an array, Ys, with shared x-axis, X
    import matplotlib.pyplot as plt
    
    # plot on one figure
    fig, ax1 = plt.subplots()
    ax1.plot(X, Ys)
    
    return( fig )
    