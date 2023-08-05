
import os
import warnings

import numpy as np


# tofu
pfe = os.path.join(os.path.expanduser('~'), '.tofu', '_imas2tofu_def.py')
if os.path.isfile(pfe):
    # Make sure we load the user-specific file
    # sys.path method
    # sys.path.insert(1, os.path.join(os.path.expanduser('~'), '.tofu'))
    # import _scripts_def as _defscripts
    # _ = sys.path.pop(1)
    # importlib method
    import importlib.util
    spec = importlib.util.spec_from_file_location("_defimas2tofu", pfe)
    _defimas2tofu = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_defimas2tofu)
else:
    try:
        import tofu.imas2tofu._def as _defimas2tofu
    except Exception as err:
        from . import _def as _defimas2tofu

_ERRSHOT = False
_ERREXP = False

_DTLIM = _defimas2tofu._DTLIM
_INDEVENT = _defimas2tofu._INDEVENT


# #############################################################################
#                       Generic
# #############################################################################


def _check_shotExp_consistency(didd, lidd, tofustr='shot', imasstr='shot',
                               err=True, fallback=0):
    crit = None
    for idd in lidd:
        v0 = didd[idd]
        if imasstr in v0['params']:
            if crit is None:
                crit = v0['params'][imasstr]
            elif crit != v0['params'][imasstr]:
                ss = '{} : {}'.format(idd, str(v0['params'][imasstr]))
                msg = ("All idd refer to different {}!\n".format(imasstr)
                       + "\t- {}".format(ss))
                if err:
                    raise Exception(msg)
                else:
                    warnings.warn(msg)
    if crit is None:
        crit = fallback
    return crit


def get_lidsidd_shotExp(lidsok,
                        errshot=None, errExp=None, upper=True,
                        dids=None, didd=None):
    """ Check whether all shot / Exp are consistent accross the ids """

    if errshot is None:
        errshot = _ERRSHOT
    if errExp is None:
        errExp = _ERREXP

    lids = set(lidsok).intersection(dids.keys())
    lidd = set([dids[ids]['idd'] for ids in lids])

    # shot (non-identical => error if errshot is True, warning otherwise)
    shot = _check_shotExp_consistency(didd, lidd,
                                      tofustr='shot', imasstr='shot',
                                      err=errshot, fallback=0)

    # Exp (non-identical => error if errExp is True, warning otherwise)
    Exp = _check_shotExp_consistency(didd, lidd,
                                     tofustr='Exp', imasstr='tokamak',
                                     err=errExp, fallback='Dummy')
    if upper is True:
        Exp = Exp.upper()
    return lids, lidd, shot, Exp


# #############################################################################
#                       Extra
# #############################################################################


def extra_checkformat(dextra, fordata=None,
                      dids=None, didd=None, dshort=None):

    lc = [dextra is False, dextra is None,
          isinstance(dextra, str),
          isinstance(dextra, list),
          isinstance(dextra, dict)]
    if not any(lc):
        msg = ("Arg dextra must be either:\n"
               + "\t- None:     set to default\n"
               + "\t- False:    no extra signal\n"
               + "\t- str:      a single extra signal (shortcut)\n"
               + "\t- list:     a list of extra signals\n"
               + "\t- dict:     a dict of extra signals {ids: list of short}\n"
               + "\n  You provided: {}".format(dextra))
        raise Exception(msg)

    if dextra is False:
        if fordata is True:
            return None
        else:
            return None, None

    elif dextra is None:
        dextra = {}
        if 'equilibrium' in dids.keys():
            dextra.update({'equilibrium': [('ip', 'k'), ('BT0', 'm'),
                                           ('axR', (0., 0.8, 0.)),
                                           ('axZ', (0., 1., 0.)),
                                           'ax', 'sep', 't']})
        if 'core_profiles' in dids.keys():
            dextra.update({'core_profiles': ['ip', 'vloop', 't']})
        if 'lh_antennas' in dids.keys():
            dextra.update({'lh_antennas': [('power0', (0.8, 0., 0.)),
                                           ('power1', (1., 0., 0.)), 't']})
        if 'ic_antennas' in dids.keys():
            dextra.update({'ic_antennas': [
                ('power0', (0., 0., 0.8)),
                ('power1', (0., 0., 1.)),
                ('power2', (0., 0., 0.9)), 't']})
    if type(dextra) is str:
        dextra = [dextra]
    if type(dextra) is list:
        dex = {}
        for ee in dextra:
            lids = [ids for ids in dids.keys()
                    if ee in dshort[ids].keys()]
            if len(lids) != 1:
                msg = ("No / multiple matches:\n"
                       + "extra {} not available from self._dshort".format(ee))
                raise Exception(msg)
            if lids[0] not in dex.keys():
                dex = {lids[0]: [ee]}
            else:
                dex[lids[0]].append(ee)
        dextra = dex
    return dextra


def extra_get_fordataTrue(inds, vs, vc, out, dout,
                          ids=None, dshort=None, dcomp=None):
    for ii in inds:
        ss = vs[ii]
        if ss == 't':
            continue
        if out[ss]['isempty'] is True:
            continue
        if ss in dshort[ids].keys():
            dd = dshort[ids][ss]
        else:
            dd = dcomp[ids][ss]
        label = dd.get('quant', 'unknown')
        units = out[ss]['units']
        key = '{}.{}'.format(ids, ss)

        if 'sep' == ss.split('.')[-1].lower():
            out[ss]['data'] = np.swapaxes(out[ss]['data'], 1, 2)

        datastr = 'data'
        if any([ss.split('.')[-1].lower() == s0 for s0 in ['sep', 'ax', 'x']]):
            datastr = 'data2D'

        dout[key] = {'t': out['t']['data'],
                     datastr: out[ss]['data'],
                     'label': label, 'units': units, 'c': vc[ii]}


def extra_get_fordataFalse(out, d0d, dt0,
                           ids=None, dshort=None, dcomp=None):
    any_ = False
    keyt = '{}.t'.format(ids)
    for ss in out.keys():
        if ss == 't':
            continue
        if out[ss]['isempty'] is True:
            continue
        if ss in dshort[ids].keys():
            dd = dshort[ids][ss]
        else:
            dd = dcomp[ids][ss]
        dim = dd.get('dim', 'unknown')
        quant = dd.get('quant', 'unknown')
        units = out[ss]['units']
        key = '{}.{}'.format(ids, ss)

        if 'sep' == ss.split('.')[-1].lower():
            out[ss]['data'] = np.swapaxes(out[ss]['data'], 1, 2)

        d0d[key] = {'data': out[ss]['data'], 'name': ss,
                    'origin': ids, 'dim': dim, 'quant': quant,
                    'units': units, 'depend': (keyt,)}
        any_ = True
    if any_ is True:
        dt0[keyt] = {'data': out['t']['data'], 'name': 't',
                     'origin': ids, 'depend': (keyt,)}


# #############################################################################
#                       Config
# #############################################################################


def config_extract_lS(ids, occ, wall, description_2d, mod,
                      kwargs=None, mobile=None):
    """ Extract all relevant structures """

    nlim = len(wall.limiter.unit)
    nmob = len(wall.mobile.unit)
    # onelimonly = False

    # ----------------------------------
    # Relevant only if vessel is filled
    # try:
    #    if len(wall.vessel.unit) != 1:
    #        msg = "There is no / several vessel.unit!"
    #        raise Exception(msg)
    #    if len(wall.vessel.unit[0].element) != 1:
    #        msg = "There is no / several vessel.unit[0].element!"
    #        raise Exception(msg)
    #    if len(wall.vessel.unit[0].element[0].outline.r) < 3:
    #        msg = "wall.vessel polygon has less than 3 points!"
    #        raise Exception(msg)
    #    name = wall.vessel.unit[0].element[0].name
    #    poly = np.array([wall.vessel.unit[0].element[0].outline.r,
    #                     wall.vessel.unit[0].element[0].outline.z])
    # except Exception as err:
    #    # If vessel not in vessel, sometimes stored a a single limiter
    #    if nlim == 1:
    #        name = wall.limiter.unit[0].name
    #        poly = np.array([wall.limiter.unit[0].outline.r,
    #                         wall.limiter.unit[0].outline.z])
    #        onelimonly = True
    #    else:
    #        msg = ("There does not seem to be any vessel, "
    #               + "not in wall.vessel nor in wall.limiter!")
    #        raise Exception(msg)
    # cls = None
    # if name == '':
    #     name = 'ImasVessel'
    # if '_' in name:
    #     ln = name.split('_')
    #     if len(ln) == 2:
    #         cls, name = ln
    #     else:
    #         name = name.replace('_', '')
    # if cls is None:
    #     cls = 'Ves'
    # assert cls in ['Ves', 'PlasmaDomain']
    # ves = getattr(mod, cls)(Poly=poly, Name=name, **kwargs)

    # Determine if mobile or not
    # if onelimonly is False:
    if mobile is None:
        if nlim == 0 and nmob > 0:
            mobile = True
        elif nmob == 0 and nlim > 0:
            mobile = False
        elif nmob > nlim:
            msgw = 'wall.description_2[{}]'.format(description_2d)
            msg = ("\nids wall has less limiter than mobile units\n"
                   + "\t- len({}.limiter.unit) = {}\n".format(msgw, nlim)
                   + "\t- len({}.mobile.unit) = {}\n".format(msgw, nmob)
                   + "  => Choosing mobile by default")
            warnings.warn(msg)
            mobile = True
        elif nmob <= nlim:
            msgw = 'wall.description_2[{}]'.format(description_2d)
            msg = ("\nids wall has more limiter than mobile units\n"
                   + "\t- len({}.limiter.unit) = {}\n".format(msgw, nlim)
                   + "\t- len({}.mobile.unit) = {}\n".format(msgw, nmob)
                   + "  => Choosing limiter by default")
            warnings.warn(msg)
            mobile = False
    assert isinstance(mobile, bool)

    # Get PFC
    if mobile is True:
        units = wall.mobile.unit
    else:
        units = wall.limiter.unit
    nunits = len(units)

    if nunits == 0:
        msg = ("There is no unit stored !\n"
               + "The required 2d description is empty:\n")
        ms = "len(idd.{}[occ={}].description_2d".format(ids, occ)
        msg += "{}[{}].limiter.unit) = 0".format(ms,
                                                 description_2d)
        raise Exception(msg)

    lS = [None for _ in units]
    for ii in range(0, nunits):
        try:
            if mobile is True:
                outline = units[ii].outline[0]
            else:
                outline = units[ii].outline
            poly = np.array([outline.r, outline.z])

            if units[ii].phi_extensions.size > 0:
                pos, extent = units[ii].phi_extensions.T
            else:
                pos, extent = None, None
            name = units[ii].name
            cls, mobi = None, None
            if name == '':
                name = 'unit{:02.0f}'.format(ii)
            if '_' in name:
                ln = name.split('_')
                if len(ln) == 2:
                    cls, name = ln
                elif len(ln) == 3:
                    cls, name, mobi = ln
                else:
                    name = name.replace('_', '')
            if cls is None:
                if ii == nunits - 1:
                    cls = 'Ves'
                else:
                    cls = 'PFC'
            # mobi = mobi == 'mobile'
            lS[ii] = getattr(mod, cls)(Poly=poly, pos=pos,
                                       extent=extent,
                                       Name=name,
                                       **kwargs)
        except Exception as err:
            msg = ("PFC unit[{}] named {} ".format(ii, name)
                   + "could not be loaded!\n"
                   + str(err))
            raise Exception(msg)
    return lS


# #############################################################################
#                       Plasma
# #############################################################################


def plasma_checkformat_dsig(dsig=None,
                            lidsplasma=None, dids=None,
                            dshort=None, dcomp=None):
    lidsok = set(lidsplasma).intersection(dids.keys())

    lscom = ['t']
    lsmesh = ['2dmeshNodes', '2dmeshFaces',
              '2dmeshR', '2dmeshZ']

    lc = [dsig is None,
          type(dsig) is str,
          type(dsig) is list,
          type(dsig) is dict]
    assert any(lc)

    # Convert to dict
    if lc[0]:
        dsig = dict.fromkeys(lidsok)
    elif lc[1] or lc[2]:
        if lc[1]:
            dsig = [dsig]
        dsig = dict.fromkeys(lidsok.intersection(dsig))

    for ids in dsig.keys():
        if dsig[ids] is None:
            dsig[ids] = sorted(set(list(dshort[ids].keys())
                                   + list(dcomp[ids].keys())))

    # Check content
    dout = {}
    for k0, v0 in dsig.items():
        lkeysok = sorted(set(list(dshort[k0].keys())
                             + list(dcomp[k0].keys())))
        if k0 not in lidsok:
            msg = ("Only the following ids are relevant to Plasma2D:\n"
                   + "\t- {}\n".format(lidsok)
                   + "  => ids {} from dsig is ignored".format(k0))
            warnings.warn(msg)
            continue
        lc = [v0 is None, type(v0) is str, type(v0) is list]
        if not any(lc):
            msg = ("Each value in dsig must be either:\n"
                   + "\t- None\n"
                   + "\t- str : a valid shortcut\n"
                   + "\t- list of str: list of valid shortcuts\n"
                   + "You provided:\n{}".format(dsig))
            raise Exception(msg)
        if lc[0]:
            dsig[k0] = lkeysok
        if lc[1]:
            dsig[k0] = [dsig[k0]]
        if not all([ss in lkeysok for ss in dsig[k0]]):
            msg = ("All requested signals must be valid shortcuts !\n"
                   + "    - dsig[{}] = {}".format(k0, dsig[k0]))
            raise Exception(msg)

        # Check presence of minimum
        lc = [ss for ss in lscom if ss not in dsig[k0]]
        if len(lc) > 0:
            msg = ("dsig[{}] does not have {}\n".format(k0, lc)
                   + "    - dsig[{}] = {}".format(k0, dsig[k0]))
            raise Exception(msg)

        # Check required minimum for 2dmesh, for valid shortcuts
        if any(['2d' in ss for ss in dsig[k0]]):
            lsmesh0 = set(lsmesh).intersection(dshort[k0].keys())
            dsig[k0] += list(lsmesh0.difference(dsig[k0]))
        dout[k0] = dsig[k0]
    return dout


def plasma_plot_args(plot, plot_X, plot_sig,
                     dsig=None):
    # Set plot
    if plot is None:
        plot = not (plot_sig is None and plot_X is None)

    if plot is True:
        # set plot_sig
        if plot_sig is None:
            lsplot = [ss for ss in list(dsig.values())[0]
                      if ('1d' in ss and ss != 't'
                          and all([sub not in ss
                                   for sub in ['rho', 'psi', 'phi']]))]
            if not (len(dsig) == 1 and len(lsplot) == 1):
                msg = ("Direct plotting only possible if\n"
                       + "sig_plot is provided, or can be derived from:\n"
                       + "\t- unique ids: {}\n\t".format(dsig.keys())
                       + "- unique non-(t, radius) 1d sig: {}".format(lsplot))
                raise Exception(msg)
            plot_sig = lsplot
        if type(plot_sig) is str:
            plot_sig = [plot_sig]

        # set plot_X
        if plot_X is None:
            lsplot = [ss for ss in list(dsig.values())[0]
                      if ('1d' in ss and ss != 't'
                          and any([sub in ss
                                   for sub in ['rho', 'psi', 'phi']]))]
            if not (len(dsig) == 1 and len(lsplot) == 1):
                msg = ("Direct plotting only possible if\n"
                       + "X_plot is provided, or can be derived from:\n"
                       + "\t- unique ids: {}\n".format(dsig.keys())
                       + "\t- unique non-t, 1d radius: {}".format(lsplot))
                raise Exception(msg)
            plot_X = lsplot
        if type(plot_X) is str:
            plot_X = [plot_X]
    return plot, plot_X, plot_sig


# #############################################################################
#                       Cam
# #############################################################################


def cam_checkformat_geom(ids=None, geomcls=None, indch=None,
                         lidsdiag=None, dids=None, didsdiag=None):

    # Check ids
    idsok = set(lidsdiag).intersection(dids.keys())
    if ids is None and len(idsok) == 1:
        ids = next(iter(idsok))

    if ids not in dids.keys():
        msg = ("Provided ids should be available as a self.dids.keys()!\n"
               + "\t- provided: {}\n".format(str(ids))
               + "\t- available: {}".format(sorted(dids.keys())))
        raise Exception(msg)

    if ids not in lidsdiag:
        msg = ("Requested ids is not pre-tabulated !\n"
               + "  => Be careful with args (geomcls, indch)")
        warnings.warn(msg)
    else:
        if geomcls is None:
            geomcls = didsdiag[ids]['geomcls']

    # Check data and geom
    import tofu.geom as tfg

    lgeom = [kk for kk in dir(tfg) if 'Cam' in kk]
    if geomcls not in [False] + lgeom:
        msg = "Arg geomcls must be in {}".format([False]+lgeom)
        raise Exception(msg)

    if geomcls is False:
        msg = "ids {} does not seem to be a ids with a camera".format(ids)
        raise Exception(msg)

    return geomcls


def cam_compare_indch_indchr(indch, indchr, nch, indch_auto=None):
    if indch_auto is None:
        indch_auto = True
    if indch is None:
        indch = np.arange(0, nch)
    if not np.all(np.in1d(indch, indchr)):
        msg = ("indch has to be changed, some data may be missing\n"
               + "\t- indch: {}\n".format(indch)
               + "\t- indch recommended: {}".format(indchr)
               + "\n\n  => check self.inspect_channels() for details")
        if indch_auto is True:
            indch = indchr
            warnings.warn(msg)
        else:
            raise Exception(msg)
    return indch


def inspect_channels_dout(ids=None, indch=None, geom=None,
                          out=None, nch=None, dshort=None,
                          lsig=None, lsigshape=None,
                          compute_ind=None):
    dout = {}
    for k0, v0 in out.items():
        v0 = v0['data']
        if len(v0) != nch:
            if len(v0) != 1:
                import pdb          # DB
                pdb.set_trace()     # DB
            continue
        if isinstance(v0[0], np.ndarray):
            dout[k0] = {'shapes': np.array([vv.shape for vv in v0]),
                        'isnan': np.array([np.any(np.isnan(vv))
                                           for vv in v0])}
            if k0 == 'los_ptsRZPhi':
                dout[k0]['equal'] = np.array([np.allclose(vv[0, ...],
                                                          vv[1, ...])
                                             for vv in v0])
        elif type(v0[0]) in [int, float, np.int, np.float, str]:
            dout[k0] = {'value': np.asarray(v0).ravel()}
        else:
            typv = type(v0[0])
            k0str = (dshort[ids][k0]['str']
                     if k0 in dshort[ids].keys() else k0)
            msg = ("\nUnknown data type:\n"
                   + "\ttype({}) = {}".format(k0str, typv))
            raise Exception(msg)

    lsig = sorted(set(lsig).intersection(dout.keys()))
    lsigshape = sorted(set(lsigshape).intersection(dout.keys()))

    # --------------
    # Get indchout
    indchout = None
    if compute_ind:
        if geom in ['only', True] and 'los_ptsRZPhi' in out.keys():
            indg = ((np.prod(dout['los_ptsRZPhi']['shapes'], axis=1) == 0)
                    | dout['los_ptsRZPhi']['isnan']
                    | dout['los_ptsRZPhi']['equal'])
            if geom == 'only':
                indok = ~indg
                indchout = indok.nonzero()[0]
        if geom != 'only':
            shapes0 = np.concatenate([np.prod(dout[k0]['shapes'],
                                              axis=1, keepdims=True)
                                      for k0 in lsigshape], axis=1)
            indok = np.all(shapes0 != 0, axis=1)
            if geom is True and 'los_ptsRZPhi' in out.keys():
                indok[indg] = False
        if not np.any(indok):
            indchout = np.array([], dtype=int)
        elif geom != 'only':
            indchout = (np.arange(0, nch)[indok]
                        if indch is None else np.r_[indch][indok])
            lshapes = [dout[k0]['shapes'][indchout, :] for k0 in lsigshape]
            lshapesu = [np.unique(ss, axis=0) for ss in lshapes]
            if any([ss.shape[0] > 1 for ss in lshapesu]):
                for ii in range(len(lshapesu)):
                    if lshapesu[ii].shape[0] > 1:
                        _, inv, counts = np.unique(lshapes[ii], axis=0,
                                                   return_counts=True,
                                                   return_inverse=True)
                        indchout = indchout[inv == np.argmax(counts)]
                        lshapes = [dout[k0]['shapes'][indchout, :]
                                   for k0 in lsigshape]
                        lshapesu = [np.unique(ss, axis=0) for ss in lshapes]
    return dout, indchout


def cam_to_Cam_Du(out, ids=None):
    Etendues, Surfaces, names = None, None, None
    if 'los_ptsRZPhi' in out.keys():
        oo = out['los_ptsRZPhi']['data']
        D = np.array([oo[:, 0, 0]*np.cos(oo[:, 0, 2]),
                      oo[:, 0, 0]*np.sin(oo[:, 0, 2]), oo[:, 0, 1]])
        u = np.array([oo[:, 1, 0]*np.cos(oo[:, 1, 2]),
                      oo[:, 1, 0]*np.sin(oo[:, 1, 2]), oo[:, 1, 1]])
        u = (u-D) / np.sqrt(np.sum((u-D)**2, axis=0))[None, :]
        dgeom = (D, u)
        indnan = np.any(np.isnan(D), axis=0) | np.any(np.isnan(u), axis=0)
        if np.any(indnan):
            nunav, ntot = str(indnan.sum()), str(D.shape[1])
            msg = ("Some lines of sight unavailable in {}:\n".format(ids)
                   + "\t- unavailable LOS: {0} / {1}\n".format(nunav, ntot)
                   + "\t- indices: {0}".format(str(indnan.nonzero()[0])))
            warnings.warn(msg)
    else:
        dgeom = None

    if 'etendue' in out.keys():
        Etendues = out['etendue']['data']
    if 'surface' in out.keys():
        Surfaces = out['surface']['data']
    if 'names' in out.keys():
        names = out['names']['data']
    return dgeom, Etendues, Surfaces, names


# #############################################################################
#                       Data
# #############################################################################


def data_checkformat_tlim(t, tlim=None,
                          names=None, times=None, indevent=None,
                          returnas=bool, Exp=None):
    # Check inputs
    if tlim is None:
        tlim = _DTLIM.get(Exp, False)
    if indevent is None:
        indevent = _INDEVENT
    if names is not None:
        names = np.char.strip(names)
    if returnas is None:
        returnas = bool
    if returnas not in [bool, int]:
        msg = ("Arg returnas must be in [bool, int]\n"
               + "\t- provided: {}".format(retrunas))
        raise Exception(msg)
    assert returnas in [bool, int]
    lc = [tlim is None,
          tlim is False,
          (isinstance(tlim, list) and len(tlim) == 2
           and all([(type(tt) in [int, float, np.int_, np.float_]
                     or (isinstance(tt, str)
                         and names is not None
                         and tt in names)
                     or tt is None) for tt in tlim]))]

    if not any(lc):
        msg = ("tlim must be either:\n"
               + "\t- None:  set to default (False)\n"
               + "\t- False: no time limit\n"
               + "\t- list:  a list of 2, lower and upper limits [t0, t1]:\n"
               + "\t\t- [None, float]: no lower, explicit upper limit\n"
               + "\t\t- [float, float]: explicit lower and upper limit\n"
               + "\t\t- [float, str]: explicit lower, event name for upper\n\n"
               + "  You provided: {}".format(tlim))
        if any([isinstance(tt, str) for tt in tlim]):
            msg += '\n\nAvailable events:\n' + str(names)
        warnings.warn(msg)
        tlim = False
    if tlim is None:
        tlim = False

    # Compute
    indt = np.ones((t.size,), dtype=bool)
    if tlim is not False:
        for ii in range(len(tlim)):
            if isinstance(tlim[ii], str):
                ind = (names == tlim[ii]).nonzero()[0][indevent]
                tlim[ii] = times[ind]
        if tlim[0] is not None:
            indt[t < tlim[0]] = False
        if tlim[1] is not None:
            indt[t > tlim[1]] = False
    t = t[indt]
    if returnas is int:
        indt = np.nonzero(indt)[0]
    return {'tlim': tlim, 'nt': t.size, 't': t, 'indt': indt}


def data_checkformat_dsig(ids=None, dsig=None, data=None, X=None,
                          datacls=None, geomcls=None,
                          lidsdiag=None, dids=None, didsdiag=None,
                          dshort=None, dcomp=None):

    # Check ids
    idsok = set(lidsdiag).intersection(dids.keys())
    if ids is None and len(idsok) == 1:
        ids = next(iter(idsok))

    if ids not in dids.keys():
        msg = "Provided ids should be available as a self.dids.keys() !"
        raise Exception(msg)

    if ids not in lidsdiag:
        msg = "Requested ids is not pre-tabulated !\n"
        msg = "  => Be careful with args (dsig, datacls, geomcls)"
        warnings.warn(msg)
    else:
        if datacls is None:
            datacls = didsdiag[ids]['datacls']
        if geomcls is None:
            geomcls = didsdiag[ids]['geomcls']
        if dsig is None:
            dsig = didsdiag[ids]['sig']
    if data is not None:
        if not isinstance(data, str):
            msg = ("data was expected as a str\n"
                   + "\t- provided: {}".format(data))
            raise Exception(msg)
        dsig['data'] = data
    if X is not None:
        if not isinstance(X, str):
            msg = ("X was expected as a str\n"
                   + "\t- provided: {}".format(X))
            raise Exception(msg)
        dsig['X'] = X

    # Check data and geom
    import tofu.geom as tfg
    import tofu.data as tfd

    if datacls is None:
        datacls = 'DataCam1D'
    ldata = [kk for kk in dir(tfd) if 'DataCam' in kk]
    if datacls not in ldata:
        msg = "Arg datacls must be in {}".format(ldata)
        raise Exception(msg)
    lgeom = [kk for kk in dir(tfg) if 'Cam' in kk]
    if geomcls not in [False] + lgeom:
        msg = "Arg geom must be in {}".format([False] + lgeom)
        raise Exception(msg)

    # Check signals
    c0 = type(dsig) is dict
    c0 = c0 and 'data' in dsig.keys()
    ls = ['t', 'X', 'lamb', 'data']
    c0 = c0 and all([ss in ls for ss in dsig.keys()])
    if not c0:
        msg = ("Arg dsig must be a dict with keys:\n"
               + "\t- 'data' : shortcut to the main data to be loaded\n"
               + "\t- 't':       (optional) shortcut to time vector\n"
               + "\t- 'X':       (optional) shortcut to abscissa vector\n"
               + "\t- 'lamb':    (optional) shortcut to wavelengths")
        raise Exception(msg)

    dout = {}
    lok = set(dshort[ids].keys()).union(dcomp[ids].keys())
    for k, v in dsig.items():
        if v in lok:
            dout[k] = v

    return datacls, geomcls, dout


# #############################################################################
#                       signal
# #############################################################################


def signal_get_synth(ids, dsig=None,
                     quant=None, ref1d=None, ref2d=None,
                     q2dR=None, q2dPhi=None, q2dZ=None,
                     didsdiag=None, lidsplasma=None, dshort=None, dcomp=None):

    # Check quant, ref1d, ref2d
    dq = {'quant': quant, 'ref1d': ref1d, 'ref2d': ref2d,
          'q2dR': q2dR, 'q2dPhi': q2dPhi, 'q2dZ': q2dZ}
    for kk, vv in dq.items():
        lc = [vv is None, type(vv) is str, type(vv) in [list, tuple]]
        assert any(lc)
        if lc[0]:
            dq[kk] = didsdiag[ids]['synth']['dsynth'].get(kk, None)
        if type(dq[kk]) is str:
            dq[kk] = [dq[kk]]
        if dq[kk] is not None:
            for ii in range(0, len(dq[kk])):
                v1 = tuple(dq[kk][ii].split('.'))
                assert len(v1) == 2
                assert v1[0] in lidsplasma
                assert (v1[1] in dshort[v1[0]].keys()
                        or v1[1] in dcomp[v1[0]].keys())
                dq[kk][ii] = v1

    # Check dsig
    if dsig is None:
        dsig = didsdiag[ids]['synth']['dsig']

    for k0, v0 in dsig.items():
        if type(v0) is not list:
            v0 = [v0]
        c0 = k0 in lidsplasma
        c0 = c0 and all([type(vv) is str for vv in v0])
        if not c0:
            msg = "Arg dsig must be a dict (ids:[shortcut1, shortcut2...])"
            raise Exception(msg)
        dsig[k0] = v0

    # Check dsig vs quant/ref1d/ref2d consistency
    for kk, vv in dq.items():
        if vv is None:
            continue
        for ii in range(0, len(vv)):
            if vv[ii][0] not in dsig.keys():
                dsig[vv[ii][0]] = []
            if vv[ii][1] not in dsig[vv[ii][0]]:
                dsig[vv[ii][0]].append(vv[ii][1])
            dq[kk][ii] = '{}.{}'.format(vv[ii][0], vv[ii][1])

    lq = didsdiag[ids]['synth']['dsynth'].get('fargs', None)
    if lq is not None:
        for qq in lq:
            q01 = qq.split('.')
            assert len(q01) == 2
            if q01[0] not in dsig.keys():
                dsig[q01[0]] = [q01[1]]
            else:
                dsig[q01[0]].append(q01[1])

    if dq['quant'] is None and dq['q2dR'] is None and lq is None:
        msg = "both quant and q2dR are not specified !"
        raise Exception(msg)

    # Remove unused keys
    for kk in list(dq.keys()):
        if dq[kk] is None:
            del dq[kk]
    return dsig, dq, lq
