'''
    QC-DMET: a python implementation of density matrix embedding theory for ab initio quantum chemistry
    Copyright (C) 2015 Sebastian Wouters
    
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import sys
sys.path.append('src')
import localintegrals, dmet
from pyscf import gto
import numpy as np
import math as m

b1 = 1.2
b2 = 1.2
nat = 10
mol = gto.Mole()
mol.verbose = 0
mol.atom = []

r = b1/2 / np.sin(np.pi/nat)
for i in range(nat):
    theta = i * (2*np.pi/nat)
    mol.atom.append(('Li', (r*np.cos(theta), r*np.sin(theta), 0)))

mol.basis = {'Li': gto.basis.parse('''
Li    S
    642.4189200              0.0021426        
     96.7985150              0.0162089        
     22.0911210              0.0773156        
      6.2010703              0.2457860        
      1.9351177              0.4701890        
      0.6367358              0.3454708        
Li    S
      2.3249184             -0.0350917
      0.6324306             -0.1912328
      0.0790534              1.0839878
Li    S
      0.0359620              1.0000000
''')}
mol.build()

myInts = localintegrals.localintegrals( mol )
myInts.molden( 'qiming_li.molden' )

#Imp size : 1 Li
atoms_per_imp = 1

impurityClusters = []
for cluster in range( nat / atoms_per_imp ):
    impurities = np.zeros( [ myInts.mol.nao_nr() ], dtype=int )
    for orb in range(3*atoms_per_imp):
        impurities[ 3*atoms_per_imp*cluster + orb ] = 1
    impurityClusters.append( impurities )
isTranslationInvariant = True
theDMET = dmet.dmet( myInts, impurityClusters, isTranslationInvariant )
theDMET.doselfconsistent()


