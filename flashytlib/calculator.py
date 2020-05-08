# --- fun [ read zeroth moment J(e) and integrate ] --- #
def ReadMoment_Zeroth( filename, Dir ):
    # read moment J from chk as a functionn of energy
    import numpy as np
    import flashytlib.io as fyio
    import flashytlib.io_basis as fyiobasis
    import flashytlib.calculator as fycal

    nNodeE = 2 # default and only avaliable @ Mar.20
    # read in chk and determine nPointsE
    nPointsE = 0
    nPointsE = int(fyio.IO_FLASH_nPointsE( filename ))
    [eL, eR, zoomE] = fyiobasis.IO_CheckESetting(Dir+'/flash.par',False)
    Radius   = fyio.IO_FLASH_1D_1Var( filename,'r_cm', False )
    nPointsX = len(Radius)
    J_PhaseSpace_Nodes = np.zeros([nPointsX,nPointsE*nNodeE])
    J_PhaseSpace_SubCE = np.zeros([nPointsX,nPointsE])
    J_str = nPointsE*nNodeE *['']
    for i in range(nPointsE*nNodeE):
        J_str[i] = 't'+'{:03d}'.format(i+1)
        J_PhaseSpace_Nodes[:,i] = fyio.IO_FLASH_1D_1Var( filename,J_str[i], False )
    for ix in range(nPointsX):
        for ie in range(nPointsE):
            J_PhaseSpace_SubCE[ix,ie] = fycal.CellAve_Gaussian( J_PhaseSpace_Nodes[ix,ie*nNodeE:ie*nNodeE+2] )

    NumberDensity = np.zeros([nPointsX])
    EnergyDensity = np.zeros([nPointsX])
    # default Energy Grid setting
    
    [Ecenter, Ewidth, Enodes] = fycal.CreateGeometricMesh( nPointsE, nNodeE, eL, eR, zoomE)
    
    const = 4.0 * np.pi
    for ix in range(nPointsX):
        NumberDensity[ix] = const * fycal.TrapezoidalIntegral( Ecenter, J_PhaseSpace_SubCE[ix], 2. )
        # 2. => energy ** 2
        EnergyDensity[ix] = const * fycal.TrapezoidalIntegral( Ecenter, J_PhaseSpace_SubCE[ix], 3. )
        # 3. => energy ** 3

    AverageEnergy = np.true_divide(EnergyDensity,NumberDensity)

    return( NumberDensity, EnergyDensity, AverageEnergy, J_PhaseSpace_SubCE, Ecenter, Radius )

# --- fun [ read first moment H1(e) and integrate ] --- #
def ReadMoment_First( filename, Dir ):
    # read moment H1 from chk as a functionn of energy
    import numpy as np
    import flashytlib.io as fyio
    import flashytlib.io_basis as fyiobasis
    import flashytlib.calculator as fycal

    nNodeE = 2 # default and only avaliable @ Mar.20
    # read in chk and determine nPointsE
    nPointsE = 0
    nPointsE = int(fyio.IO_FLASH_nPointsE( filename ))
    [eL, eR, zoomE] = fyiobasis.IO_CheckESetting(Dir+'/flash.par', False)
    
    Radius   = fyio.IO_FLASH_1D_1Var( filename,'r_cm', False )
    nPointsX = len(Radius)
    H1_PhaseSpace_Nodes = np.zeros([nPointsX,nPointsE*nNodeE])
    H1_PhaseSpace_SubCE = np.zeros([nPointsX,nPointsE])
    H1_str = nPointsE*nNodeE *['']
    for i in range(nPointsE*nNodeE):
        H1_str[i] = 't'+'{:03d}'.format(i+1+nPointsE*nNodeE)
        H1_PhaseSpace_Nodes[:,i] = fyio.IO_FLASH_1D_1Var( filename,H1_str[i], False )
    for ix in range(nPointsX):
        for ie in range(nPointsE):
            H1_PhaseSpace_SubCE[ix,ie] = fycal.CellAve_Gaussian( H1_PhaseSpace_Nodes[ix,ie*nNodeE:ie*nNodeE+2] )

    Luminosity = np.zeros([nPointsX])

    [Ecenter, Ewidth, Enodes] = fycal.CreateGeometricMesh( nPointsE, nNodeE, eL, eR, zoomE)

    const = 4.0 * np.pi
    for ix in range(nPointsX):
        Luminosity[ix] = const * fycal.TrapezoidalIntegral( Ecenter, H1_PhaseSpace_SubCE[ix], 3. )
        # 3. => energy ** 3

    return( Luminosity, H1_PhaseSpace_SubCE, Ecenter, Radius )

# --- fun [ create mesh ] --- #    
def CreateMesh( N, nN, SW, xL, xR, ZoomOption=1.0 ):
    import numpy as np
    import flashytlib.calculator as fycal
    
    Mesh_Length = xR - xL
    
    if( ZoomOption > 1.0 ):
        Mesh = cal.CreateGeometricMesh( N, SW, xL, xR, Mesh_Center, Mesh_Width, ZoomOption )
    elif( ZoomOption == 1.0 ):
        Mesh = cal.CreateEquidistantMesh( N, SW, xL, xR, Mesh_Center, Mesh_Width )
        
    grid = np.zeros([nPoint])
    rate = np.exp(np.log(Xmax)/nPoint)
    print(rate)
    return( Mesh_Center, Mesh_Width )

# --- fun [ create geometric mesh ] --- #
def CreateGeometricMesh( N, nN, xL, xR, Zoom ):
    # mimic thornado's Mesh module
    # N = nPointsE, nN = nNode
    # ***BUT*** excluded ghost cells
    import numpy as np
    import flashytlib.calculator as fycal

    if( nN != 2 ): print('[CreateGeometricMesh]: Only for nNode=2')

    nCells = N
    Width  = np.zeros([nCells])
    Center = np.zeros([nCells])

    Width[0]  = ( xR - xL ) * ( Zoom - 1.0 ) / ( Zoom**N - 1.0 )
    Center[0] = xL + 0.5 * Width[0]
    for i in range(1,N):
        Width[i]  = Width[i-1] * Zoom
        Center[i] = xL + np.sum( Width[0:i] ) + 0.5*Width[i]

    NodesCoordinate = np.zeros([N*nN])
    [xQ, wQ] = fycal.GetTwoPointGaussianQuadrature( )
    for i in range(0,N):
        for ii in range(0,nN):
            NodesCoordinate[i*nN + ii] = Center[i] + Width[i] * xQ[ii]

    return( Center, Width, NodesCoordinate )

# --- fun [ cell average with Gaussian Quadrature ] --- #
def CellAve_Gaussian( NodeValues ):
    # SubcellReconstruction
    # with 2-point Gaussian Quadrature
    # input NodeValues[2]
    import numpy as np
    import flashytlib.calculator as fycal

    [ xG2, wG2 ] = fycal.GetTwoPointGaussianQuadrature()
    CellAve = NodeValues[0] * wG2[0] + NodeValues[1] * wG2[1]   
 
    return( CellAve )

# --- fun [ integral function ] --- #
def TrapezoidalIntegral( x, y, exp ) :
    # approximate the definite integral using trapezoidal rule
    # int_{xmin}^{xmax} [ y(x) * (x**exp) ] dx
    # when exponent exp = 0 => int_{xmin}^{xmax} y(x) dx
    import numpy as np
 
    integ = 0.
    ncell = len(x)
    if( len(x) != len(y) or len(x) < 2 ): 
        print('[TrapezoidalIntegral] Error: Dim mismatching')
        exit
    else:
        for ii in range(ncell-1):
            width = x[ii+1] - x[ii]
            integ = integ + 0.5 * width * ( y[ii]*(x[ii]**exp) + y[ii+1]*(x[ii+1]**exp) )

    return( integ )
    
# =========== Numbers ============= #
# --- fun [ Quadrature ] --- #
def GetTwoPointGaussianQuadrature( ):
    # mimic thornado's setting
    # output is xG2[2] and wG2[2]
    import numpy as np

    xG2 = np.zeros([2])
    wG2 = np.zeros([2])

    xG2[0] = - np.sqrt( 1.0 / 12.0 )
    xG2[1] = + np.sqrt( 1.0 / 12.0 )

    wG2[0] = 0.5
    wG2[1] = 0.5
    
    return( xG2, wG2 ) 
