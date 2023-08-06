# -*- coding: utf-8 -*-

"""Functions for manipulating OSC files.  These are provided through
the **OSC** object and a module function to read an **OSC** object
from a file.

"""

import numpy as np
import warnings
from .constants import G_DEFAULT
from .utils import integrate, tomso_open, regularize
from .utils import FullStellarModel


def load_osc(filename, return_comment=False,
             return_object=True, G=None, encoding='utf-8'):
    """Given an OSC file, returns NumPy arrays `glob` and `var` that
    correspond to the scalar and point-wise variables, as specified in
    the `OSC format`_, as well as a list of strings `abund` with the
    names of the species being followed.

    .. _OSC format: https://www.astro.up.pt/corot/ntools/docs/CoRoT_ESTA_Files.pdf

    Also returns the first four lines of the file as a `comment`, if
    desired.

    If `return_object` is `True`, instead returns an :py:class:`OSC`
    object.  This is the default behaviour as of v0.0.12.  The old
    behaviour will be dropped completely from v0.1.0.

    Parameters
    ----------
    filename: str
        Name of the FGONG file to read.
    return_comment: bool, optional
        If ``True``, return the first four lines of the FGONG file.
        These are comments that are not used in any calculations.

    Returns
    -------
    glob: NumPy array
        The scalar (or global) variables for the stellar model.
    var: NumPy array
        The point-wise variables for the stellar model. i.e. things
        that vary through the star like temperature, density, etc.
    abund: list of strs
        Names of the chemical species followed in the point-wise data
        after the data in ``var``.
    comment: list of strs, optional
        The first four lines of the FGONG file.  These are comments
        that are not used in any calculations.  Only returned if
        ``return_comment=True``.

    """
    with tomso_open(filename, 'rb') as f:
        comment = [f.readline().decode(encoding).strip() for i in range(4)]
        abund = [s.decode(encoding) for s in f.readline().split()[1:]]
        nn, iconst, ivar, iabund, ivers = [int(i) for i in f.readline().decode('utf-8').split()]
        # lines = f.readlines()
        lines = [line.decode('utf-8').lower().replace('d', 'e')
                 for line in f.readlines()]

    tmp = []
    N = 19

    for line in lines:
        for i in range(len(line)//N):
            s = line[i*N:i*N+N]
            # print(s)
            if s[-9:] == '-Infinity':
                s = '-Inf'
            elif s[-9:] == ' Infinity':
                s = 'Inf'
            elif s.lower().endswith('nan'):
                s = 'nan'
            elif 'd' in s.lower():
                s = s.lower().replace('d','e')

            tmp.append(float(s))

    glob = np.array(tmp[:iconst])
    var = np.array(tmp[iconst:]).reshape((-1, ivar+iabund))

    if return_object:
        return OSC(glob, var, abund, ivers=ivers, G=G,
                   description=comment)
    else:
        warnings.warn("From tomso 0.1.0+, `fgong.load_osc` will only "
                      "return an `OSC` object: use `return_object=True` "
                      "to mimic future behaviour",
                      FutureWarning)
        if return_comment:
            return glob, var, abund, comment
        else:
            return glob, var, abund


def save_osc(filename, glob, var, abund, ivers=-1,
             comment=['','','','']):
    """Given data for an OSC file in the format returned by
    :py:meth:`~tomso.osc.load_osc` (i.e. two NumPy arrays, a list of
    strings and a possible header), writes the data to a file.

    This function will be dropped from v0.1.0 in favour of the `to_file`
    function of the :py:class:`OSC` object.

    Parameters
    ----------
    filename: str
        Filename to which OSC data is written.
    glob: NumPy array
        The global variables for the stellar model.
    var: NumPy array
        The point-wise variables for the stellar model. i.e. things
        that vary through the star like temperature, density, etc.
    abund: list of strs
        Names of the chemical species followed in the point-wise data
        after the data in ``var``.
    ivers: int, optional
        The integer indicating the version number of the file.
        (default=0)
    comment: list of strs, optional
        The first four lines of the OSC file, which usually contain
        notes about the stellar model.

    """
    nn = len(var)
    iabund = len(abund)
    ivar = len(var[0])-iabund
    iconst = len(glob)

    fmt = '%19.12E'

    with open(filename, 'wt') as f:
        f.write('\n'.join(comment) + '\n')

        f.write('%3i' % iabund)
        for i, val in enumerate(abund):
            f.write(' %4s' % val)

        f.write('\n')

        line = '%10i'*5 % (nn, iconst, ivar, iabund, ivers) + '\n'
        f.write(line)

        for i, val in enumerate(glob):
            f.write(fmt % val)
            if i % 5 == 4:
                f.write('\n')

        if i % 5 != 4:
            f.write('\n')

        for row in var:
            for i, val in enumerate(row):
                print(i)
                f.write(fmt % val)
                if i % 5 == 4:
                    f.write('\n')

        if i % 5 != 4:
            f.write('\n')


class OSC(FullStellarModel):
    """A class that contains and allows one to manipulate the data in a
    stellar model stored in the `OSC format`_.

    .. _OSC format: https://www.astro.up.pt/corot/ntools/docs/CoRoT_ESTA_Files.pdf

    The main attributes are the **glob** and **var** arrays, which
    follow the definitions in the OSC standard.  The data in these
    arrays can be accessed via the attributes with more
    physically-meaningful names (e.g. the radius is ``OSC.r``).

    Some of these values can also be set via the attributes if doing
    so is unambiguous. For example, the fractional radius **x** is not a
    member of the **var** array but setting **x** will assign the actual
    radius **r**, which is the first column of **var**.  Values that are
    settable are indicated in the list of parameters.

    Parameters
    ----------
    glob: NumPy array
        The global variables for the stellar model.
    var: NumPy array
        The point-wise variables for the stellar model. i.e. things
        that vary through the star like temperature, density, etc.
    abund: list of strs
        Names of the chemical species followed in the point-wise data
        after the data in ``var``.
    ivers: int, optional
        The integer indicating the version number of the file.
        (default=0)
    G: float, optional
        Value for the gravitational constant.
    description: list of 4 strs, optional
        The first four lines of the OSC file, which usually contain
        notes about the stellar model.

    Attributes
    ----------
    iconst: int
        number of global data entries (i.e. length of **glob**)
    nn: int
        number of points in stellar model (i.e. number of rows in **var**)
    ivar: int
        number of variables recorded at each point in stellar model
        (i.e. number of columns in **var**)
    iabund: int
        number of abundances recorded at each point in stellar model
        (i.e. number of species in **abund**)
    """

    def __init__(self, glob, var, abund, ivers=-1, G=G_DEFAULT,
                 description=['', '', '', '']):
        self.ivers = ivers
        self.glob = glob
        self.var = var
        self.abund = abund
        self.description = description
        self.G = G

    def __len__(self):
        return len(self.var)

    def __repr__(self):
        with np.printoptions(threshold=10):
            return('OSC(\nabund=[%s],\nglob=\n%s,\nvar=\n%s,\ndescription=\n%s)' % (','.join(self.abund), self.glob, self.var, '\n'.join(self.description)))

    def to_fgong(self, ivers=1300):
        """Convert the model to an ``FGONG`` object.

        Parameters
        ----------
        ivers: int, optional
            The integer indicating the version number of the file.
            (default=1300)
        """
        from .fgong import FGONG

        glob = np.zeros(15)
        glob[0] = self.M
        glob[1] = self.R
        glob[2] = self.L
        glob[10:13] = self.glob[8:11] # (R²/P) (d²P/dr²), (R²/ρ) (d²ρ/dr²) and age
        glob[14] = self.G
        
        var = np.zeros((len(self.var), 40))
        var[:,0] = self.r
        var[:,1] = self.lnq
        var[:,2] = self.T
        var[:,3] = self.P
        var[:,4] = self.rho
        var[:,6] = self.L_r
        var[:,7] = self.kappa
        var[:,9] = self.Gamma_1
        var[:,12] = self.cp
        var[:,14] = self.AA

        return FGONG(glob, var, ivers=ivers, G=self.G,
                     description=self.description)

    # OSC parameters that can be derived from data
    @property
    def iconst(self): return len(self.glob)

    @property
    def nn(self): return self.var.shape[0]

    @property
    def ivar(self): return self.var.shape[1]-self.iabund

    @property
    def iabund(self): return len(self.abund)

    @property
    def M(self): return self.glob[0]

    @M.setter
    def M(self, val): self.glob[0] = val

    @property
    def R(self): return self.glob[1]

    @R.setter
    def R(self, val): self.glob[1] = val

    @property
    def L(self): return self.glob[2]

    @L.setter
    def L(self, val): self.glob[2] = val

    @property
    def r(self): return self.var[:,0]

    @r.setter
    def r(self, val): self.var[:,0] = val

    @property
    def lnq(self): return self.var[:,1]

    @lnq.setter
    def lnq(self, val): self.var[:,1] = val

    @property
    def T(self): return self.var[:,2]

    @T.setter
    def T(self, val): self.var[:,2] = val

    @property
    def P(self): return self.var[:,3]

    @P.setter
    def P(self, val): self.var[:,3] = val

    @property
    def rho(self): return self.var[:,4]

    @rho.setter
    def rho(self, val): self.var[:,4] = val

    @property
    def L_r(self): return self.var[:,6]

    @L_r.setter
    def L_r(self, val): self.var[:,6] = val

    @property
    def kappa(self): return self.var[:,7]

    @kappa.setter
    def kappa(self): self.var[:,7] = val

    @property
    def epsilon(self): return self.var[:,8]

    @epsilon.setter
    def epsilon(self, val): self.var[:,8] = val

    @property
    def Gamma_1(self): return self.var[:,9]

    @Gamma_1.setter
    def Gamma_1(self, val): self.var[:,9] = val

    @property
    def G1(self): return self.var[:,9]

    @G1.setter
    def G1(self, val): self.var[:,9] = val

    @property
    def cp(self): return self.var[:,12]

    @cp.setter
    def cp(self, val): self.var[:,12] = val

    @property
    def AA(self): return self.var[:,14]

    @AA.setter
    def AA(self, val): self.var[:,14] = val

    # Some convenient quantities derived from `glob` and `var`.
    @property
    def x(self): return self.r/self.R

    @x.setter
    def x(self, val): self.r = val*self.R

    @property
    def q(self): return np.exp(self.lnq)

    @q.setter
    def q(self, val): self.lnq = np.log(val)

    @property
    def m(self): return self.q*self.M

    @m.setter
    def m(self, val): self.q = val/self.M

    @property
    @regularize()
    def N2(self): return self.AA*self.g/self.r

    @property
    @regularize(y0=3)
    def U(self): return 4.*np.pi*self.rho*self.r**3/self.m

    @property
    @regularize()
    def V(self): return self.G*self.m*self.rho/self.P/self.r

    @property
    def Vg(self): return self.V/self.Gamma_1

    @property
    def tau(self):
        if np.all(np.diff(self.x) < 0):
            return -integrate(1./self.cs, self.r)
        else:
            tau = integrate(1./self.cs[::-1], self.r[::-1])[::-1]
            return np.max(tau)-tau
