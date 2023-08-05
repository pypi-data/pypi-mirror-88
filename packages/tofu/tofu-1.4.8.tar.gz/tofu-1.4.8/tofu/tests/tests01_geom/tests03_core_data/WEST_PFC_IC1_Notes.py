#!/usr/bin/env python

# Built-in
import os
import argparse

# Common
import numpy as np

_save = True
_here = os.path.abspath(os.path.dirname(__file__))
_Exp, _Cls, _name = os.path.split(__file__)[1].split('_')[:3]
assert not any([any([ss in s for ss in ['Notes','.']])
               for s in [_Exp, _Cls, _name]])

def get_notes():
    notes = {}
    # Samples from 3D drawings
    # IC1
    notes['sampXYZ'] = [[-2471.450, -494.911, 1590.106],  # Back
                        [-2469.748, -335.000, 1749.276],  # Back
                        [-2515.174, -335.000, 1787.393],  # Back
                        [-2515.174,  335.000, 1787.393],  # Back
                        [-2469.748,  335.000, 1749.276],  # Back
                        [-2471.450,  494.911, 1590.106],  # Back
                        [-2292.115,  504.105, 1578.294],    # 1st pt
                        [-2286.026,  504.799, 1544.321],
                        [-2287.754,  465.078, 1545.771],
                        [-2293.653,  468.768, 1579.584],    # bottom
                        [-2293.811,  467.342, 1579.717],    # bottom
                        [-2287.937,  463.423, 1545.925],
                        [-2294.923,  424.698, 1551.787],
                        [-2300.025,  432.890, 1584.931],    # bottom
                        [-2300.371,  431.522, 1585.221],    # bottom
                        [-2295.324,  423.110, 1552.123],
                        [-2307.354,  386.556, 1562.218],
                        [-2311.074,  399.002, 1594.202],    # bottom
                        [-2310.685,  397.685, 1595.181],    # bottom
                        [-2307.977,  385.107, 1562.740],
                        [-2319.952,  356.614, 1572.789],
                        [-2322.660,  369.192, 1605.229],    # bottom
                        [-2323.367,  367.162, 1605.909],    # bottom
                        [-2320.358,  355.596, 1573.129],
                        [-2331.369,  326.447, 1582.369],
                        [-2334.481,  338.013, 1615.148],    # bottom
                        [-2335.222,  335.939, 1615.770],    # bottom
                        [-2331.741,  325.407, 1582.681],
                        [-2341.768,  295.659, 1591.094],
                        [-2345.249,  306.191, 1624.184],    # bottom
                        [-2345.920,  304.077, 1624.747],    # bottom
                        [-2342.104,  294.599, 1591.377],
                        [-2351.128,  264.308, 1598.948],
                        [-2354.943,  273.786, 1632.318],    # bottom
                        [-2355.543,  271.635, 1632.821],    # bottom
                        [-2351.429,  263.230, 1599.201],
                        [-2359.431,  232.454, 1605.916],
                        [-2363.545,  240.860, 1639.536],    # bottom
                        [-2364.073,  238.677, 1639.979],    # bottom
                        [-2359.696,  231.360, 1606.138],
                        [-2366.663,  200.158, 1611.984],
                        [-2371.039,  207.476, 1645.825],    # bottom
                        [-2371.493,  205.265, 1646.205],    # bottom
                        [-2366.890,  199.049, 1612.174],
                        [-2372.808,  167.481, 1617.140],
                        [-2377.411,  173.696, 1651.171],    # bottom
                        [-2377.790,  171.461, 1651.489],    # bottom
                        [-2372.998,  166.360, 1617.300],
                        [-2377.855,  134.484, 1621.375],
                        [-2382.647,  139.586, 1655.565],    # bottom
                        [-2382.952,  137.332, 1655.820],    # bottom
                        [-2378.008,  133.354, 1621.503],
                        [-2381.795,  101.232, 1624.681],
                        [-2386.739,  105.210, 1658.998],
                        [-2386.968,  102.941, 1659.190],    # bottom
                        [-2381.910,  100.094, 1624.778],    # bottom
                        [-2384.620,   67.787, 1627.052],
                        [-2389.678,   70.634, 1661.465],    # bottom
                        [-2389.831,   68.354, 1661.593],    # bottom
                        [-2384.697,   66.644, 1627.116],
                        [-2386.325,   34.213, 1628.482],
                        [-2391.459,   35.923, 1662.959],    # bottom
                        [-2391.536,   33.637, 1663.023],    # bottom
                        [-2386.364,   33.066, 1628.515],
                        [-2386.907,    0.574, 1628.970],
                        [-2392.079,    1.144, 1663.479],    # bottom
                        [-2392.079,   -1.144, 1663.479],    # bottom
                        [-2386.907,   -0.574, 1628.970],
                        [-2386.364,  -33.066, 1628.515],
                        [-2391.536,  -33.637, 1663.023],    # bottom
                        [-2391.459,  -35.923, 1662.959],    # bottom
                        [-2386.325,  -34.213, 1628.482],
                        [-2384.697,  -66.644, 1627.116],
                        [-2389.831,  -68.354, 1661.593],    # bottom
                        [-2389.678,  -70.634, 1661.465],    # bottom
                        [-2384.620,  -67.787, 1627.052],
                        [-2381.910, -100.094, 1624.778],
                        [-2386.968, -102.941, 1659.190],    # bottom
                        [-2386.739, -105.210, 1658.998],    # bottom
                        [-2381.795, -101.232, 1624.681],
                        [-2378.008, -133.354, 1621.503],
                        [-2382.952, -137.332, 1655.820],    # bottom
                        [-2382.647, -139.586, 1655.565],    # bottom
                        [-2377.855, -134.484, 1621.375],
                        [-2372.998, -166.360, 1617.300],
                        [-2377.790, -171.461, 1651.489],    # bottom
                        [-2377.411, -173.696, 1651.171],    # bottom
                        [-2372.808, -167.481, 1617.140],
                        [-2366.890, -199.049, 1612.174],
                        [-2371.493, -205.265, 1646.205],    # bottom
                        [-2371.039, -207.476, 1645.825],    # bottom
                        [-2366.663, -200.158, 1611.984],
                        [-2359.696, -231.360, 1606.138],
                        [-2364.073, -238.677, 1639.979],    # bottom
                        [-2363.545, -240.860, 1639.536],    # bottom
                        [-2359.431, -232.454, 1605.916],
                        [-2351.429, -263.230, 1599.201],
                        [-2355.543, -271.635, 1632.821],    # bottom
                        [-2354.943, -273.786, 1632.318],    # bottom
                        [-2351.128, -264.308, 1598.948],
                        [-2342.104, -294.599, 1591.377],
                        [-2345.920, -304.077, 1624.747],    # bottom
                        [-2345.249, -306.191, 1624.184],    # bottom
                        [-2341.768, -295.659, 1591.094],
                        [-2331.741, -325.407, 1582.681],
                        [-2335.222, -335.939, 1615.770],    # bottom
                        [-2334.481, -338.013, 1615.148],    # bottom
                        [-2331.369, -326.447, 1582.369],
                        [-2320.358, -355.596, 1573.129],
                        [-2323.469, -367.162, 1605.909],    # bottom
                        [-2322.660, -369.192, 1605.229],    # bottom
                        [-2319.952, -356.614, 1572.789],
                        [-2307.977, -385.107, 1562.740],
                        [-2310.685, -397.685, 1595.181],    # bottom
                        [-2311.074, -399.002, 1594.202],    # bottom
                        [-2307.354, -386.556, 1562.218],
                        [-2295.324, -423.110, 1552.123],
                        [-2300.371, -431.522, 1585.211],    # bottom
                        [-2300.025, -432.890, 1584.931],    # bottom
                        [-2294.923, -424.698, 1551.787],
                        [-2287.937, -463.423, 1545.925],
                        [-2293.811, -467.342, 1579.717],    # bottom
                        [-2293.653, -468.768, 1579.584],    # bottom
                        [-2287.754, -465.078, 1545.771],
                        [-2286.026, -504.799, 1544.321],
                        [-2292.115, -504.105, 1578.294]]    # Last pt

    notes['sampXYZ'] = np.array(notes['sampXYZ'])
    nn = notes['sampXYZ'].shape[0]
    ind = np.arange(8,nn-4,4)
    notes['indedges'] = np.array([ind,ind+3])
    ind = np.arange(9,nn-4,4)
    notes['indbottom'] = np.unique(np.array([ind,ind+1]).ravel())
    return notes


def make_Poly(save=_save, path=_here):
    notes = get_notes()
    Rref, Rmax = 3., 3.4

    R = np.hypot(notes['sampXYZ'][:,0],notes['sampXYZ'][:,2])/1000.
    Z = notes['sampXYZ'][:,1]/1000.
    R = R-np.min(R[np.abs(Z)<0.01])+Rref
    R[2:4] = Rmax

    Poly1 = np.array([R,Z])
    ind = notes['indedges']
    Ptemp = 0.5*(Poly1[:,ind[0,:]] + Poly1[:,ind[1,:]])
    Poly0 = np.concatenate((Poly1[:,:ind[0,0]], Ptemp,
                            Poly1[:,ind[1,-1]+1:]),axis=1)
    if save:
        cstr = '%s_%s_%s'%(_Exp,_Cls,_name)
        pathfilext = os.path.join(path, cstr+'_V0.txt')
        np.savetxt(pathfilext, Poly0)
        pathfilext = os.path.join(path, cstr+'_V1.txt')
        np.savetxt(pathfilext, Poly1)
    return Poly0, Poly1, notes



if __name__=='__main__':

    # Parse input arguments
    msg = 'Launch creation of polygons txt from bash'
    parser = argparse.ArgumentParser(description = msg)

    parser.add_argument('-save', type=bool, help='save ?', default=_save)
    parser.add_argument('-path', type=str, help='saving path ?', default=_here)

    args = parser.parse_args()

    # Call wrapper function
    make_Poly(save=args.save, path=args.path)
