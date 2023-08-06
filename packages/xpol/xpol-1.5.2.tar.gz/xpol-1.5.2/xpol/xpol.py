from __future__ import division

import healpy as hp
import numpy as np
import _flib as flib
import os
from astropy.io import fits

__all__ = ['Xpol','Xcov','Bins','fsky','Xpol_Wrapper','gaussian_apodization','sample_variance']


def fsky(mask):
    return np.mean(mask**2)**2/np.mean(mask**4)

def gaussian_apodization( mask, deg, threshold=1e-5):
    smask = hp.smoothing( mask, fwhm=np.deg2rad(deg), verbose=False)
    smask[smask < (0. + threshold)] = 0.+ threshold
    smask[smask > (1. - threshold)] = 1.- threshold
    return smask

def sample_variance( l, cl, fsky=1.):
    cosmic = np.sqrt( 2./(2*l+1))/fsky * cl
    cosmic[3] = np.sqrt( 1./(2*l+1)*(cl[0]*cl[1]+cl[3]*cl[3]))/fsky
    if len(cl) > 4:
        cosmic[4] = np.sqrt( 1./(2*l+1)*(cl[0]*cl[2]+cl[4]*cl[4]))/fsky
    if len(cl) > 5:
        cosmic[5] = np.sqrt( 1./(2*l+1)*(cl[1]*cl[2]+cl[5]*cl[5]))/fsky        
    return cosmic



class Bins(object):
    """
        lmins : list of integers
            Lower bound of the bins
        lmaxs : list of integers
            Upper bound of the bins (not included)
    """
    def __init__( self, lmins, lmaxs):
        if not(len(lmins) == len(lmaxs)):
            raise ValueError('Incoherent inputs')

        lmins = np.asarray( lmins)
        lmaxs = np.asarray( lmaxs)
        cutfirst = np.logical_and(lmaxs>=2 ,lmins>=2)
        self.lmins = lmins[cutfirst]
        self.lmaxs = lmaxs[cutfirst]
        
        self._derive_ext()
    
    @classmethod
    def fromdeltal( cls, lmin, lmax, delta_ell):
        nbins = (lmax - lmin + 1) // delta_ell
        lmins = lmin + np.arange(nbins) * delta_ell
        lmaxs = lmins + delta_ell
        return cls( lmins, lmaxs)

    def _derive_ext( self):
        self.lmin = min(self.lmins)
        self.lmax = max(self.lmaxs)-1
        if self.lmin < 1:
            raise ValueError('Input lmin is less than 1.')
        if self.lmax < self.lmin:
            raise ValueError('Input lmax is less than lmin.')
        
        self.nbins = len(self.lmins)
        self.lbin = (self.lmins + self.lmaxs - 1) / 2
        self.dl   = (self.lmaxs - self.lmins)

    def bins(self):
        return self.lmins, self.lmaxs
    
    def cut_binning(self, lmin, lmax):
        sel = np.where( (self.lmins >= lmin) & (self.lmaxs <= lmax+1) )[0]
        self.lmins = self.lmins[sel]
        self.lmaxs = self.lmaxs[sel]
        self._derive_ext()
    
    def _bin_operators(self):
        ell2 = np.arange(self.lmax+1)
        ell2 = ell2 * (ell2 + 1) / (2 * np.pi)
        p = np.zeros((self.nbins, self.lmax+1))
        q = np.zeros((self.lmax+1, self.nbins))
        
        for b, (a, z) in enumerate(zip(self.lmins, self.lmaxs)):
            p[b, a:z] = ell2[a:z] / (z - a)
            q[a:z, b] = 1 / ell2[a:z]
        
        return p, q

    def bin_spectra(self, spectra, Dl=False):
        """
        Average spectra in bins specified by lmin, lmax and delta_ell,
        weighted by `l(l+1)/2pi`.
        Return Cb
        """
        spectra = np.asarray(spectra)
        minlmax = min([spectra.shape[-1] - 1,self.lmax])
        if Dl:
            fact_binned = 1.
        else:
            fact_binned = 2 * np.pi / (self.lbin * (self.lbin + 1))
            
        _p, _q = self._bin_operators()
        return np.dot(spectra[..., :minlmax+1], _p.T[:minlmax+1,...]) * fact_binned





class Xpol(object):
    """
    (Cross-) power spectra estimation using the Xpol method.
    Hinshaw et al. 2003, Tristram et al. 2005.

    Example
    -------
    bins = Bins( lmins, lmaxs)
    xpol = Xpol(mask, bins)
    lbin = xpol.lbin
    biased, unbiased = xpol.get_spectra(map)
    biased, unbiased = xpol.get_spectra(map1, map2)

    """
    def __init__(self, mask, bins, mask2=None, polar=True, verbose=False):
        """
        Parameters
        ----------
        mask : boolean Healpix map
            Mask defining the region of interest (of value True)
        bins: class binning

        """
        mask = np.asarray(mask)
        lmin = int(bins.lmin)
        lmax = int(bins.lmax)
        nside = hp.npix2nside(len(mask))
        if lmax > 3*nside-1:
            raise ValueError('Input lmax is too high for resolution.')

        self.verbose = verbose
        self.nside = nside
        self.polar = polar
        self.lmin  = lmin
        self.lmax  = lmax
        
        if self.verbose: print( "alm2map mask")
        wlmax = 3*nside-1
        if mask2 is None:
            wl = hp.anafast(mask,lmax=wlmax)
            self.mask = self.mask2 = mask
        else:
            wl = hp.anafast(mask,map2=mask2,lmax=wlmax)
            self.mask  = mask
            self.mask2 = mask2
        
        self.wl    = wl
        
        if self.verbose: print( "Compute bin operators")
        self._p, self._q = bins._bin_operators()
        self.lbin = bins.lbin
        self.bin_spectra = bins.bin_spectra

        if self.verbose: print( "Compute Mll")
        mll_binned = self._get_Mbb()

        if self.verbose: print( "Inverse Mll")
        self.mll_binned_inv = self._inv_mll(mll_binned)
#        self.mll_binned_inv = np.linalg.inv(mll_binned)

    def get_spectra(self, map1, map2=None, bell=None, bell1=None, bell2=None, pixwin=True):
        """
        Return biased and Xpol-debiased estimations of the power spectra of
        a Healpix map or of the cross-power spectra if *map2* is provided.
        
        bins = Bins.fromdeltal( lmin, lmax, deltal)
        xpol = Xpol(mask, bins)
        biased, unbiased = xpol.get_spectra(map1, [map2])

        The unbiased Cls are binned. The number of bins is given by
        (lmax - lmin) // delta_ell, using the values specified in the Xpol's
        object initialisation. As a consequence, the upper bound of the highest
        l bin may be less than lmax. The central value of the bins can be
        obtained through the attribute `xpol.lbin`.

        Parameters
        ----------
        map1 : Nx3 or 3xN array
            The I, Q, U Healpix maps.
        map2 : Nx3 or 3xN array, optional
            The I, Q, U Healpix maps.

        Returns
        -------
        biased : float array of shape (9, lmax+1)
            The anafast's pseudo (cross-) power spectra for TT,EE,BB,TE,TB,EB,ET,BT,BE.
            The corresponding l values are given by `np.arange(lmax + 1)`.

        unbiased : float array of shape (9, nbins)
            The Xpol's (cross-) power spectra for TT,EE,BB,TE,TB,EB,ET,BT,BE.
            The corresponding l values are given by `xpol.lbin`.

        """

        #Map1
        if self.verbose:
            if map2 is None:
                print( "Compute alms")
            else:
                print( "Compute alms map1")
        map1 = np.asarray(map1)
        if map1.shape[-1] == 3:
            map1 = map1.T
        
        self._removeUndef(map1)
        alms1 = hp.map2alm(map1 * self.mask, pol=self.polar, lmax=self.lmax)

        #Map2
        if map2 is None:
            alms2 = alms1
        else:
            if self.verbose: print( "Compute alms map2")
            map2 = np.asarray(map2)
            if map2.shape[-1] == 3:
                map2 = map2.T
            self._removeUndef(map2)
            alms2 = hp.map2alm( map2 * self.mask2, pol=self.polar, lmax=self.lmax)
        
        #alm2cl
        if self.verbose: print( "Alms 2 cl")
        biased = hp.alm2cl( alms1, alms2, lmax=self.lmax) #healpy order (TT,EE,BB,TE,EB,TB)
        biased = biased[[0,1,2,3,5,4]] #swith TB and EB
        if self.polar:
            biased21 = hp.alm2cl( alms2, alms1, lmax=self.lmax)
            biased21 = biased21[[0,1,2,3,5,4]] #swith TB and EB
            biased = np.array( np.concatenate( (biased, biased21[[3,4,5]]))) #concatenate with alms2xalms1
        del( alms1)
        del( alms2)

        #beam function
        if self.verbose: print( "Correct beams")
        fact_binned = self.lbin * (self.lbin + 1) / (2 * np.pi)
        if bell is not None:
            bl = bell[:self.lmax+1]**2
        else:
            bl = np.ones(self.lmax+1)
        if bell1 is not None:
            if bell2 is None:
                bell2 = bell1
            bl *= bell1[:self.lmax+1]*bell2[:self.lmax+1]
        if pixwin:
            bl *= hp.pixwin(self.nside)[:self.lmax+1]**2
        
        #bin spectra
        if self.verbose: print( "Bin spectrum")
        binned = self.bin_spectra(biased)*fact_binned
#        unbiased = np.dot(self.mll_binned_inv, binned.ravel()).reshape(6, -1)

        #debias
        if self.verbose: print( "Debias spectra")
        unbiased = self._debias_spectra( binned)
        unbiased /= fact_binned * self.bin_spectra(bl)

        return biased, unbiased

    def _debias_spectra(self, binned):
        if self.polar:
            TT_TT, EE_EE, EE_BB, TE_TE, EB_EB = self.mll_binned_inv
        else:
            TT_TT = self.mll_binned_inv

        n = len(TT_TT)
        if self.polar is False:
            TT = np.dot( TT_TT, binned)
            return np.asarray(TT)

        out = np.zeros( (2*n,2*n) )
        out[0*n:1*n, 0*n:1*n] = EE_EE
        out[1*n:2*n, 1*n:2*n] = EE_EE
        out[0*n:1*n, 1*n:2*n] = EE_BB
        out[1*n:2*n, 0*n:1*n] = EE_BB
        vec = np.dot( out, binned[1:3].ravel())
        
        TT = np.dot( TT_TT, binned[0])
        EE = vec[0:n]
        BB = vec[n:]
        TE = np.dot( TE_TE, binned[3])
        TB = np.dot( TE_TE, binned[4])
        EB = np.dot( EB_EB, binned[5])
        ET = np.dot( TE_TE, binned[6])
        BT = np.dot( TE_TE, binned[7])
        BE = np.dot( EB_EB, binned[8])
        
        return np.asarray( [TT,EE,BB,TE,TB,EB,ET,BT,BE])

    def _replaceUndefWith0(self,mymap):
        for i in range(len(mymap)):
            if( float(mymap[i]) == hp.UNSEEN):
                mymap[i] = 0.

    def _removeUndef(self,mymap):
        if self.polar:
            for m in mymap:
                self._replaceUndefWith0( m)
        else:
            self._replaceUndefWith0( mymap)

    def _inv_mll(self, mll_binned):
        if self.polar:
            TT_TT, EE_EE, EE_BB, TE_TE, EB_EB = mll_binned
        else:
            TT_TT = mll_binned

        n = len(TT_TT)
        TT_TT = np.linalg.inv(TT_TT)
        if self.polar is False:
            return TT_TT
        
        TE_TE = np.linalg.inv(TE_TE)
        EB_EB = np.linalg.inv(EB_EB)
        out = np.zeros( (2*n,2*n) )
        out[0*n:1*n, 0*n:1*n] = EE_EE
        out[1*n:2*n, 1*n:2*n] = EE_EE
        out[0*n:1*n, 1*n:2*n] = EE_BB
        out[1*n:2*n, 0*n:1*n] = EE_BB
        out = np.linalg.inv(out)
        EE_EE = out[0*n:1*n, 0*n:1*n]
        EE_BB = out[0*n:1*n, 1*n:2*n]
        
        return TT_TT, EE_EE, EE_BB, TE_TE, EB_EB

    def _get_Mll_blocks(self):
        if self.polar:
            TT_TT, EE_EE, EE_BB, TE_TE, EB_EB, ier = flib.xpol.mll_blocks_pol(self.lmax, self.wl)
        else:
            TT_TT, ier = flib.xpol.mll_blocks(self.lmax, self.wl)
        if ier > 0:
            msg = ['Either L2 < ABS(M2) or L3 < ABS(M3).',
                   'Either L2+ABS(M2) or L3+ABS(M3) non-integer.'
                   'L1MAX-L1MIN not an integer.',
                   'L1MAX less than L1MIN.',
                   'NDIM less than L1MAX-L1MIN+1.'][ier-1]
            raise RuntimeError(msg)

        if self.polar:
            return TT_TT, EE_EE, EE_BB, TE_TE, EB_EB
        else:
            return TT_TT

    def _get_Mbb(self):
        if self.polar:
            TT_TT, EE_EE, EE_BB, TE_TE, EB_EB = self._get_Mll_blocks()
        else:
            TT_TT = self._get_Mll_blocks()

        def func(x):
            return np.dot(np.dot(self._p, x), self._q)
        n = len(self.lbin)

        TT_TT = func(TT_TT)
        if self.polar is False:
            return TT_TT

        EE_EE = func(EE_EE)
        EE_BB = func(EE_BB)
        TE_TE = func(TE_TE)
        EB_EB = func(EB_EB)
        
        return TT_TT, EE_EE, EE_BB, TE_TE, EB_EB



class Xcov(Xpol):
    """
    (Cross-) power spectra covariance matrix estimation.
    Couchot et al. 2017

    Example
    -------
    xcov = Xcov(mask, lmin, lmax, delta_ell)

    """
    def __init__(self, mask, bins):
        """
        Parameters
        ----------
        mask : boolean Healpix map
            Mask defining the region of interest (of value True)

        """
        Xpol.__init__(self,mask,bins)
        
        self.dl = bins.dl
        self.wl = hp.anafast(mask**2)
        self.TT_TT, self.EE_EE, self.EE_BB, self.TE_TE, self.EB_EB = self._get_Mbb()


    def _get_pcl_cov(self, clAC, clBD, clAD, clBC):
        n = len(self.lbin)
        out = np.zeros((5*n, 5*n))
        nu_l = (2.*self.lbin+1.) * self.dl
        
        #TT_TT
        out[0*n:1*n, 0*n:1*n] = np.sqrt(abs(np.outer(clAC[0],clAC[0])*np.outer(clBD[0],clBD[0])))*self.TT_TT/nu_l + \
                                np.sqrt(abs(np.outer(clAD[0],clAD[0])*np.outer(clBC[0],clBC[0])))*self.TT_TT/nu_l

        #TT_EE
        out[0*n:1*n, 1*n:2*n] = np.sqrt(abs(np.outer(clAC[3],clAC[3])*np.outer(clBD[3],clBD[3])))*self.TT_TT/nu_l + \
                                np.sqrt(abs(np.outer(clAD[3],clAD[3])*np.outer(clBC[3],clBC[3])))*self.TT_TT/nu_l

        #TT_BB
        out[0*n:1*n, 2*n:3*n] = 0.

        #TT_TE
        out[0*n:1*n, 3*n:4*n]= np.sqrt(abs(np.outer(clAC[0],clAC[0])*np.outer(clBD[3],clBD[3])))*self.TT_TT/nu_l + \
                               np.sqrt(abs(np.outer(clAD[3],clAD[3])*np.outer(clBC[0],clBC[0])))*self.TT_TT/nu_l

        #TT_ET
        out[0*n:1*n, 4*n:5*n] = np.sqrt(abs(np.outer(clAC[3],clAC[3])*np.outer(clBD[0],clBD[0])))*self.TT_TT/nu_l + \
                                np.sqrt(abs(np.outer(clAD[0],clAD[0])*np.outer(clBC[3],clBC[3])))*self.TT_TT/nu_l

        #EE_TT
        out[1*n:2*n, 0*n:1*n] = np.sqrt(abs(np.outer(clAC[4],clAC[4])*np.outer(clBD[4],clBD[4])))*self.TT_TT/nu_l + \
                                np.sqrt(abs(np.outer(clAD[4],clAD[4])*np.outer(clBC[4],clBC[4])))*self.TT_TT/nu_l

        #EE_EE
        out[1*n:2*n, 1*n:2*n] = np.sqrt(abs(np.outer(clAC[1],clAC[1])*np.outer(clBD[1],clBD[1])))*self.EE_EE/nu_l + \
                                np.sqrt(abs(np.outer(clAD[1],clAD[1])*np.outer(clBC[1],clBC[1])))*self.EE_EE/nu_l

        #EE_BB
        out[1*n:2*n, 2*n:3*n] = ( np.sqrt(abs(np.outer(clAC[1],clAC[1])*np.outer(clBD[1],clBD[1]))) + \
                                  np.sqrt(abs(np.outer(clAC[1],clAC[1])*np.outer(clBD[2],clBD[2]))) + \
                                  np.sqrt(abs(np.outer(clAC[2],clAC[2])*np.outer(clBD[1],clBD[1]))) + \
                                  np.sqrt(abs(np.outer(clAC[2],clAC[2])*np.outer(clBD[2],clBD[2]))) )*self.EE_BB/nu_l + \
                                ( np.sqrt(abs(np.outer(clAD[1],clAD[1])*np.outer(clBC[1],clBC[1]))) + \
                                  np.sqrt(abs(np.outer(clAD[1],clAD[1])*np.outer(clBC[2],clBC[2]))) + \
                                  np.sqrt(abs(np.outer(clAD[2],clAD[2])*np.outer(clBC[1],clBC[1]))) + \
                                  np.sqrt(abs(np.outer(clAD[2],clAD[2])*np.outer(clBC[2],clBC[2]))) )*self.EE_BB/nu_l

        #EE_TE
        out[1*n:2*n, 3*n:4*n] = np.sqrt(abs(np.outer(clAC[4],clAC[4])*np.outer(clBD[1],clBD[1])))*self.TE_TE/nu_l + \
                                np.sqrt(abs(np.outer(clAD[1],clAD[1])*np.outer(clBC[4],clBC[4])))*self.TE_TE/nu_l

        #EE_ET
        out[1*n:2*n, 4*n:5*n] = np.sqrt(abs(np.outer(clAC[1],clAC[1])*np.outer(clBD[4],clBD[4])))*self.TE_TE/nu_l + \
                                np.sqrt(abs(np.outer(clAD[4],clAD[4])*np.outer(clBC[1],clBC[1])))*self.TE_TE/nu_l
        
        #BB_TT
        out[2*n:3*n, 0*n:1*n] = 0.

        #BB_EE
        out[2*n:3*n, 1*n:2*n] = np.sqrt(abs(np.outer(clAC[1],clAC[1])*np.outer(clBD[1],clBD[1])))*self.EE_BB/nu_l + \
                                np.sqrt(abs(np.outer(clAD[1],clAD[1])*np.outer(clBC[1],clBC[1])))*self.EE_BB/nu_l

        #BB_BB
        out[2*n:3*n, 2*n:3*n] = np.sqrt(abs(np.outer(clAC[2],clAC[2])*np.outer(clBD[2],clBD[2])))*self.EE_EE/nu_l + \
                                np.sqrt(abs(np.outer(clAD[2],clAD[2])*np.outer(clBC[2],clBC[2])))*self.EE_EE/nu_l

        #BB_TE
        out[2*n:3*n, 3*n:4*n] = 0.

        #BB_ET
        out[2*n:3*n, 4*n:5*n] = 0.

        #TE_TT
        out[3*n:4*n, 0*n:1*n] = np.sqrt(abs(np.outer(clAC[0],clAC[0])*np.outer(clBD[4],clBD[4])))*self.TT_TT/nu_l + \
                                np.sqrt(abs(np.outer(clAD[0],clAD[0])*np.outer(clBC[4],clBC[4])))*self.TT_TT/nu_l

        #TE_EE
        out[3*n:4*n, 1*n:2*n] = np.sqrt(abs(np.outer(clAC[3],clAC[3])*np.outer(clBD[1],clBD[1])))*self.TE_TE/nu_l + \
                                np.sqrt(abs(np.outer(clAD[3],clAD[3])*np.outer(clBC[1],clBC[1])))*self.TE_TE/nu_l

        #TE_BB
        out[3*n:4*n, 2*n:3*n] = 0.

        #TE_TE
        out[3*n:4*n, 3*n:4*n] = np.sqrt(abs(np.outer(clAC[0],clAC[0])*np.outer(clBD[1],clBD[1])))*self.TE_TE/nu_l + \
                                np.sqrt(abs(np.outer(clAD[3],clAD[3])*np.outer(clBC[4],clBC[4])))*self.TT_TT/nu_l

        #TE_ET
        out[3*n:4*n, 4*n:5*n] = np.sqrt(abs(np.outer(clAC[3],clAC[3])*np.outer(clBD[4],clBD[4])))*self.TT_TT/nu_l + \
                                np.sqrt(abs(np.outer(clAD[0],clAD[0])*np.outer(clBC[1],clBC[1])))*self.TE_TE/nu_l

        #ET_TT
        out[4*n:5*n, 0*n:1*n] = np.sqrt(abs(np.outer(clAC[4],clAC[4])*np.outer(clBD[0],clBD[0])))*self.TT_TT/nu_l + \
                                np.sqrt(abs(np.outer(clAD[4],clAD[4])*np.outer(clBC[0],clBC[0])))*self.TT_TT/nu_l

        #ET_EE
        out[4*n:5*n, 1*n:2*n] = np.sqrt(abs(np.outer(clAC[1],clAC[1])*np.outer(clBD[3],clBD[3])))*self.TE_TE/nu_l + \
                                np.sqrt(abs(np.outer(clAD[1],clAD[1])*np.outer(clBC[3],clBC[3])))*self.TE_TE/nu_l

        #ET_BB
        out[4*n:5*n, 2*n:3*n] = 0.

        #ET_TE
        out[4*n:5*n, 3*n:4*n] = np.sqrt(abs(np.outer(clAC[4],clAC[4])*np.outer(clBD[3],clBD[3])))*self.TT_TT/nu_l + \
                                np.sqrt(abs(np.outer(clAD[1],clAD[1])*np.outer(clBC[0],clBC[0])))*self.TE_TE/nu_l

        #ET_ET
        out[4*n:5*n, 4*n:5*n] = np.sqrt(abs(np.outer(clAC[1],clAC[1])*np.outer(clBD[0],clBD[0])))*self.TE_TE/nu_l + \
                                np.sqrt(abs(np.outer(clAD[4],clAD[4])*np.outer(clBC[3],clBC[3])))*self.TT_TT/nu_l
        
        
        return out


    def get_clcov_blocks(self, clAC, clBD, clAD, clBC, nsm=2):
        sclAC = self._smooth_cl( clAC, nsm=nsm)
        sclBD = self._smooth_cl( clBD, nsm=nsm)
        sclAD = self._smooth_cl( clAD, nsm=nsm)
        sclBC = self._smooth_cl( clBC, nsm=nsm)

        n = len(self.lbin)
        TT_TT, EE_EE, EE_BB, TE_TE, EB_EB = self.mll_binned_inv
        invmll = np.zeros((5*n, 5*n))
        invmll[  0:  n,   0:  n] = TT_TT
        invmll[  n:2*n,   n:2*n] = EE_EE
        invmll[2*n:3*n, 2*n:3*n] = EE_EE
        invmll[  n:2*n, 2*n:3*n] = EE_BB
        invmll[2*n:3*n,   n:2*n] = EE_BB
        invmll[3*n:4*n, 3*n:4*n] = TE_TE
        invmll[4*n:5*n, 4*n:5*n] = TE_TE
        
        return np.dot(invmll, np.dot(self._get_pcl_cov(sclAC, sclBD, sclAD, sclBC), invmll))

    def _smooth_cl( self, cl, lcut=0, nsm=2):
        import scipy.ndimage as nd

        if nsm == 0:
            return(cl)
        
        #gauss filter
        if lcut < 2*nsm:
            shift=0
        else:
            shift=2*nsm

        scl = np.copy(cl)
        data = nd.gaussian_filter1d( cl[max(0,lcut-shift):], nsm)
        scl[lcut:] = data[shift:]
        
        return scl




class Xpol_Wrapper(object):
    """
    (Cross-) power spectra estimation using the Xpol method.
    Hinshaw et al. 2003, Tristram et al. 2005.

    Wrapping to the C code.

    Example
    -------
    bins = Bins( lmins, lmaxs)
    xpol = Xpol(mask, bins)
    lbin = xpol.lbin
    biased, unbiased = xpol.get_spectra(map)
    biased, unbiased = xpol.get_spectra(map1, map2)

    """

    def __init__(self, mask, bins, mask2=None, polar=True, tmpdir=None, nprocs=8, verbose=False):
        """
        Parameters
        ----------
        mask : boolean Healpix map
            Mask defining the region of interest (of value True)
        bins: class binning (WARNING: for now only all multipoles)

        """
        
        if tmpdir is None:
            self._tmpdir = os.getenv("TMPDIR",".")
        else:
            self._tmpdir = tmpdir
        if not os.path.isdir(self._tmpdir):
            raise ValueError('No temporary directory.')
        
        self._runnb = np.random.randint(100000)
        
        self.mpirun = self._check_exe( "mpirun")+"/mpirun"
        self.bindir = self._check_exe( "xpol")
        self.lmin = int(bins.lmin)
        self.lmax = int(bins.lmax)
        self.nside = hp.npix2nside(len(mask))
        self.nprocs = nprocs
        
        self.nstokes = 3 if polar else 1
        
        self._verbose = verbose
        
        mask = np.asarray(mask)
        self._MLLFILE  = "%s/mll_%d"  % (self._tmpdir,self._runnb)
        
        self._MASKFILE = []
        self._MASKFILE.append( "%s/mask_%d_0.fits" % (self._tmpdir,self._runnb))
        hp.write_map( self._MASKFILE[0], mask)
        if mask2 is not None:
            self._MASKFILE.append( "%s/mask_%d_1.fits" % (self._tmpdir,self._runnb))
            hp.write_map( self._MASKFILE[1], mask2)
        
        self._compute_mll()

        if not os.path.isfile( self._MLLFILE+"_0_0.fits"):
            raise ValueError('Mll not found.')
    
    def __del__(self):
        self._clean( "mask_%d_0.fits" % self._runnb)
        self._clean( "mask_%d_1.fits" % self._runnb)
        self._clean( "mll_%d_*.fits" % self._runnb)
        self._clean( "pseudo_%d_*.fits" % self._runnb)
        self._clean( "cross_%d_*.fits" % self._runnb)

    def _clean(self, tmpfile):
        os.system( "rm -f %s/%s" % (self._tmpdir,tmpfile))

    def _check_exe( self, exe, path=None):
        bindir = None

        if path is None:
            paths = os.environ['PATH'].split(os.pathsep)
        else:
            paths = [path]

        for p in paths:
            if os.path.isfile( p+"/"+exe): bindir = p

        if bindir is None:
            raise ValueError( "Cannot find executables")
        
        return bindir

    def _compute_mll(self,verbose=True):
#        lmax = min( [2*self.lmax,3*self.nside-1])
        f = open( "%s/xpol_create_mll_%d.par" % (self._tmpdir,self._runnb), "w")
        f.write(      "nside = %d\n" % self.nside    )
        f.write(    "nstokes = %d\n" % self.nstokes  )
        f.write(       "lmax = %d\n" % self.lmax     )
        f.write(      "nmaps = %d\n" %              2)
        f.write(   "weightI1 = %s\n" % self._MASKFILE[0])
        f.write(   "weightP1 = %s\n" % self._MASKFILE[0])
        if len(self._MASKFILE) == 2:
            f.write(   "weightI2 = %s\n" % self._MASKFILE[1])
            f.write(   "weightP2 = %s\n" % self._MASKFILE[1])
        f.write( "mlloutfile = %s\n" % self._MLLFILE )
        f.close()

        str_exe = "%s -n %d %s/xpol_create_mll %s/xpol_create_mll_%d.par" % (self.mpirun,self.nprocs,self.bindir,self._tmpdir,self._runnb)
        if not self._verbose:
            str_exe += " >& %s/xpol_create_mll_%d.out" % (self._tmpdir,self._runnb)
        err = os.system( str_exe)
        if err:
            raiseError( "Error create mll")
        self._clean( "xpol_create_mll_%d.par" % self._runnb)
        self._clean( "xpol_create_mll_%d.out" % self._runnb)


    def _compute_spectra( self, map1, map2, bell1, bell2):
        hp.write_map( "%s/map1_%d.fits" % (self._tmpdir,self._runnb), map1, overwrite=True)
        hp.write_map( "%s/map2_%d.fits" % (self._tmpdir,self._runnb), map2, overwrite=True)

        hp.write_cl( "%s/bell1_%d.fits"  % (self._tmpdir,self._runnb), bell1, overwrite=True)
        hp.write_cl( "%s/bell2_%d.fits"  % (self._tmpdir,self._runnb), bell2, overwrite=True)

        f = open( "%s/xpol_%d.par" % (self._tmpdir,self._runnb), "w")        
        f.write(   "nside = %d\n" % self.nside)
        f.write( "nstokes = %d\n" % self.nstokes)
        f.write(    "lmax = %d\n" %  self.lmax)
        f.write(   "nmaps = %d\n" %          2)        
        f.write( "mapfile1 = %s/map1_%s.fits\n" % (self._tmpdir,self._runnb))
        f.write( "mapfile2 = %s/map2_%s.fits\n" % (self._tmpdir,self._runnb))
        f.write( "weightI1 = %s\n" % self._MASKFILE[0])
        f.write( "weightP1 = %s\n" % self._MASKFILE[0])
        if len(self._MASKFILE) == 2:
            f.write(   "weightI2 = %s\n" % self._MASKFILE[1])
            f.write(   "weightP2 = %s\n" % self._MASKFILE[1])
    
        f.write( "mllinfile = %s\n" % self._MLLFILE)

        f.write( "bell1 = %s/bell1_%d.fits\n" % (self._tmpdir,self._runnb))
        f.write( "bell2 = %s/bell2_%d.fits\n" % (self._tmpdir,self._runnb))
    
        f.write(  "pseudo = %s/pseudo_%d\n"  % (self._tmpdir,self._runnb))    
        f.write(  "cross  = %s/cross_%d\n"  % (self._tmpdir,self._runnb))    
        f.write(  "no_error = 1\n")
    
        f.close()
        
        str_exe = "%s -n %d %s/xpol %s/xpol_%d.par" % (self.mpirun,self.nprocs,self.bindir,self._tmpdir,self._runnb)
        if not self._verbose:
            str_exe += " >& %s/xpol_%d.out" % (self._tmpdir,self._runnb)
        os.system( str_exe)
        
        #clean
        self._clean( "map1_%d.fits" % self._runnb)
        self._clean( "map2_%d.fits" % self._runnb)
        self._clean( "bell1_%d.fits" % self._runnb)
        self._clean( "bell2_%d.fits" % self._runnb)
        self._clean( "xpol_%d.par" % self._runnb)
        self._clean( "xpol_%d.out" % self._runnb)
    

    def get_spectra(self, map1, map2=None, bell1=None, bell2=None):

        #launch xpol
        if map2 is None: map2=map1
        if bell1 is None: bell1 = np.ones(self.lmax+1)
        if bell2 is None: bell2 = bell1
        self._compute_spectra( map1, map2, bell1, bell2)
        
        #set in one fits file
        pcl = np.zeros( (6, self.lmax+1))
        cltmp1 = hp.read_cl( "%s/pseudo_%d_0_1.fits"  % (self._tmpdir,self._runnb))
        cltmp2 = hp.read_cl( "%s/pseudo_%d_1_0.fits"  % (self._tmpdir,self._runnb))
        pcl = cltmp1+cltmp2
        
        #set in one fits file
        cl  = np.zeros( (6, self.lmax+1))
        err = np.zeros( (6, self.lmax+1))
        for t in range(6):
            cltmp1 = fits.getdata( "%s/cross_%d_0_1.fits"  % (self._tmpdir,self._runnb), t+1)
            cltmp2 = fits.getdata( "%s/cross_%d_1_0.fits"  % (self._tmpdir,self._runnb), t+1)
            l = np.array(cltmp1.field(0),int)
            cl[t,l]  = (cltmp1.field(1)+cltmp2.field(1))/2./(l*(l+1)/2./np.pi)
            err[t,l] = np.sqrt((cltmp1.field(1)**2+cltmp2.field(1)**2)/2.)/(l*(l+1)/2./np.pi)
        
        #clean
        self._clean( "pseudo_%d_0_0.fits" % self._runnb)
        self._clean( "pseudo_%d_0_1.fits" % self._runnb)
        self._clean( "pseudo_%d_1_0.fits" % self._runnb)
        self._clean( "pseudo_%d_1_1.fits" % self._runnb)
        self._clean( "cross_%d_0_0.fits" % self._runnb)
        self._clean( "cross_%d_0_1.fits" % self._runnb)
        self._clean( "cross_%d_1_0.fits" % self._runnb)
        self._clean( "cross_%d_1_1.fits" % self._runnb)

        return pcl, cl, err

