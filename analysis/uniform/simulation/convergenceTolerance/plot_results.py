#!/usr/bin/env python

import os
import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pylab

sys.path.insert( 0, os.path.abspath( os.path.join( __file__, '..', '..', '..', '..' )))
import common.mpl_rc_settings as settings

class PlotResults( object ):

    def __init__( self ):
        self.fig_num = 1
        self.markers = [ '+' , '*' , ',' , '.' , '1' , '2' , '3' , '4' , 'h' ,
                'o' , 'p' , 's' , 'v' , 'x' , '<' , '>' , 'D' , 'H' , '^' , '_',
                'd', 'h', 'o', 'p', 's', 'v', 'x' ]
        self.iden_index = 0
        self.regs = dict(  {' regularization' : 'Regulation', ' no_regularization' : 'No Regulation' })
        self.snre_records = dict( axial_strain_snre = 'Axial $SNR_e$',
                lateral_strain_snre = 'Lateral $SNR_e$' )
        self.logplot = True

    def plot_snre_curves( self, curve, curve_name, val_min, val_max, r ):
        self.r = r
        self.val_min = val_min
        self.val_max = val_max
        fig_num = 1
        regs = set( r['regularization'] )
        for reg, reg_name in self.regs.iteritems():
            for snre_record, snre_record_name in self.snre_records.iteritems():
                plt.figure( fig_num )
                fig_num += 1
                self._plot_snre_curve( curve, curve_name, reg, reg_name,
                        snre_record, snre_record_name )

    def _plot_snre_curve( self, curve, curve_name, reg, reg_name, snre_record,
            snre_record_name ):

        variable_values = list( set( self.r[curve.lower()] ) )
        variable_values.sort()
        self.iden_index = 0
        for v in variable_values:
            if v >= val_min and v <= val_max:
                index_is_variable = self.r[curve.lower()] == v
                index_is_reg = self.r['regularization'] == reg
                strains = list( set( self.r['strain_percent'] ) )
                strains.sort()
                strains = strains[:5]
                s = np.ones( len( strains )) * 10**-5
                m = np.ones( len( strains )) * 10**-5
                e = np.ones( len( strains )) * 10**-5
                for si, strain in enumerate( strains ):
                    index_is_strain = self.r['strain_percent'] == strain
                    strain_indices = np.arange( len( self.r ) )[ np.nonzero(
                        np.logical_and( index_is_variable, np.logical_and(
                            index_is_strain, index_is_reg )))]
                    if snre_record.find( 'lateral' ) == -1:
                        s[si] = strain
                    else:
                        s[si] = strain / 2.0
                    trials = self.r[snre_record][strain_indices]
                    if len( trials ) > 0:
                        m[si] = np.mean( trials )
                        e[si] = 2*np.std( trials )/np.sqrt( len( trials ))

                plt.errorbar( s, m, e, label='1e-' + str( v ),
                        marker=self.markers[self.iden_index],
                        markeredgewidth=1.0, markevery=1, ms=9.0, alpha=0.5 )
                plt.xlabel( 'Strain Percent' )
                plt.ylabel( snre_record_name + ', ' + reg_name )
                #plt.title( str( variable_name ))
                plt.legend( loc='best' )
                if self.logplot:
                    plt.gca().set_yscale( 'log' )
                #plt.ylim( (10**-2, 10**2 ) )
                plt.ylim( (10**-1.2, 10**1.5 ) )
                plt.xlim( (0.0, s[-1]+0.5) )

                self.iden_index += 1


plot_results = PlotResults()
curves = dict( convergenceTolerance_sim = 'Convergence Tolerance' )
val_min = 1
val_max = 8
for curve, curve_name in curves.iteritems():
    r = pylab.csv2rec( 'SNRe_' + curve + '.csv' )
    plot_results.plot_snre_curves( curve, curve_name, val_min, val_max, r )

plt.figure( 1 )
plt.savefig( '../../../../doc/images/convergenceTolerance_simulation_regularization_axial.png' )
plt.savefig( '../../../../doc/images/convergenceTolerance_simulation_regularization_axial.eps' )
plt.figure( 2 )
plt.savefig( '../../../../doc/images/convergenceTolerance_simulation_regularization_lateral.png' )
plt.savefig( '../../../../doc/images/convergenceTolerance_simulation_regularization_lateral.eps' )
plt.figure( 3 )
plt.savefig( '../../../../doc/images/convergenceTolerance_simulation_no_regularization_axial.png' )
plt.savefig( '../../../../doc/images/convergenceTolerance_simulation_no_regularization_axial.eps' )
plt.figure( 4 )
plt.savefig( '../../../../doc/images/convergenceTolerance_simulation_no_regularization_lateral.png' )
plt.savefig( '../../../../doc/images/convergenceTolerance_simulation_no_regularization_lateral.eps' )

plt.show()
