#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:43:15 2018

@author: kaspar
"""

# This code attempts to retrieve literature photometry for a given star. 
# usage in ipython / spyder:  run photretrieval.py --target HD189733
# command line usage: python photretrieval.py --target HD189733

#########################

# imports

from astroquery.simbad import Simbad
from astroquery.vizier import Vizier
import argparse
import time
import getpass
#from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
#from astropy import units as u 
#import numpy as np

# 1: get info from SIMBAD, which also resolves name. Can outsource this into 
# separate function(s) later on. Need magnitudes plus references, distance 
# plus reference, plus can get general description and spectral type. 

# identify target in SIMBAD

#target = raw_input("input target star: ")
parser = argparse.ArgumentParser()
parser.add_argument('--target', help='input target name; use quotation marks')
args = parser.parse_args()


#IDs = Simbad.query_objectids(args.target)

#if IDs == None:
#    print (args.target, 'not found in SIMBAD.')
#    exit(1)
#else:
#   print (IDs)

# note: A list of all possible VOTable fileds can be found here: 
# http://simbad.u-strasbg.fr/simbad/sim-help?Page=sim-fscript#VotableFields
# or via Simbad.list_votable_fields()    
    
# retrieve mags, errors, bibcodes
    
# These are all the bands that are stored in SIMBAD (I think).
Simbad.add_votable_fields('flux(U)','flux_error(U)','flux_bibcode(U)')
Simbad.add_votable_fields('flux(B)','flux_error(B)','flux_bibcode(B)')
Simbad.add_votable_fields('flux(V)','flux_error(V)','flux_bibcode(V)')
Simbad.add_votable_fields('flux(R)','flux_error(R)','flux_bibcode(R)')
Simbad.add_votable_fields('flux(I)','flux_error(I)','flux_bibcode(I)')
Simbad.add_votable_fields('flux(J)','flux_error(J)','flux_bibcode(J)')
Simbad.add_votable_fields('flux(H)','flux_error(H)','flux_bibcode(H)')
Simbad.add_votable_fields('flux(K)','flux_error(K)','flux_bibcode(K)')
Simbad.add_votable_fields('flux(G)','flux_error(G)','flux_bibcode(G)')
Simbad.add_votable_fields('flux(u)','flux_error(u)','flux_bibcode(u)')
Simbad.add_votable_fields('flux(g)','flux_error(g)','flux_bibcode(g)')
Simbad.add_votable_fields('flux(r)','flux_error(r)','flux_bibcode(r)')
Simbad.add_votable_fields('flux(i)','flux_error(i)','flux_bibcode(i)')
Simbad.add_votable_fields('flux(z)','flux_error(z)','flux_bibcode(z)')
# can also simplify: 
# Simbad.add_votable_fields('fluxdata(v)')
# if no data exist in given filter, output is None:
# #if result_table['FLUX_I'][0] == None: 
#    print "No I magnitude found."
#
# to get results printed out: 
# print("M", result_table['FLUX_J'][0],result_table['FLUX_ERROR_J'][0]," # ",result_table['FLUX_BIBCODE_J'][0])

#retrieve coordinates
Simbad.add_votable_fields('coo')
# print("# Coords (2000):", result_table['RA'][0], result_table['DEC'][0])

#retrieve spectral type
Simbad.add_votable_fields('sptype')
# print(# "Spectral type", result_table['SP_TYPE'][0],result_table['SP_BIBCODE'][0])

#retrieve parallax and calculate distance, including bibcode
Simbad.add_votable_fields('parallax')
# print("P", result_table['PLX_VALUE'][0],result_table['PLX_ERROR'][0]," # ",result_table['PLX_BIBCODE'][0])

# before anything can be printed out, need to 
# assign all defined VOtable fields to an array containing the data. 
    
result_table = Simbad.query_object(args.target)

# debug
#print ('Columns retrieved:')
#print (result_table.colnames) # Print names of all columns retrieved
#print (' ')

# calculate distance from parallax
distance = 1000.0 / result_table['PLX_VALUE'][0]
distance_error = distance * (result_table['PLX_ERROR'][0] / result_table['PLX_VALUE'][0])
#print ("distance: %.2f \pm %.2f pc" % (distance, distance_error))

# format and print results: 
# for some reason I do not understand, any output that is a string is 
# preceded by a b' and has a ' at its end. Format to get rid of that. 
# Need to append .decode('utf-8') to end of whatever string is causing problem.

print("###", time.asctime())
print("### by", getpass.getuser())
print("### Object:", args.target)
print("### Coords (2000):", result_table['RA'][0], result_table['DEC'][0])
print("### Spectral Type: %.10s  ##  %.22s" % (result_table['SP_TYPE'][0].decode('utf-8'),
      result_table['SP_BIBCODE'][0].decode('utf-8')))
print("D", args.target, "%.3f %.3f ## Parallax %.3f [%.3f] %.22s" % 
      (distance, distance_error, result_table['PLX_VALUE'][0],
      result_table['PLX_ERROR'][0], result_table['PLX_BIBCODE'][0].decode('utf-8')))
print("#")
print("#")
print("# Photometry returned by SIMBAD by default")
print("#")
# print out magnitudes -- first check if there is a value
if result_table['FLUX_U'][0] != None:
    if result_table['FLUX_ERROR_U'][0] != None:
        print("M", args.target, "Johnson U", result_table['FLUX_U'][0],
              result_table['FLUX_ERROR_U'][0]," # ",
              result_table['FLUX_BIBCODE_U'][0].decode('utf-8'))
    else:
        print("M", args.target, "Johnson U", result_table['FLUX_U'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_U'][0].decode('utf-8'),"; e_mag set to 0.05")        

if result_table['FLUX_B'][0] != None:
    if result_table['FLUX_ERROR_B'][0] != None:
        print("M", args.target, "Johnson B", result_table['FLUX_B'][0],
              result_table['FLUX_ERROR_B'][0]," # ",
              result_table['FLUX_BIBCODE_B'][0].decode('utf-8'))
    else:
        print("M", args.target, "Johnson B", result_table['FLUX_B'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_B'][0].decode('utf-8'),"; e_mag set to 0.05") 
        
if result_table['FLUX_V'][0] != None:
    if result_table['FLUX_ERROR_V'][0] != None:
        print("M", args.target, "Johnson V", result_table['FLUX_V'][0],
              result_table['FLUX_ERROR_V'][0]," # ",
              result_table['FLUX_BIBCODE_V'][0].decode('utf-8'))
    else:
        print("M", args.target, "Johnson V", result_table['FLUX_V'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_V'][0].decode('utf-8'),"; e_mag set to 0.05") 

if result_table['FLUX_R'][0] != None:
    if result_table['FLUX_ERROR_R'][0] != None:
        print("M", args.target, "Cousins Rc", result_table['FLUX_R'][0],
              result_table['FLUX_ERROR_R'][0]," # ",
              result_table['FLUX_BIBCODE_R'][0].decode('utf-8'))
    else:
        print("M", args.target, "Cousins Rc", result_table['FLUX_R'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_R'][0].decode('utf-8'),"; e_mag set to 0.05") 

if result_table['FLUX_I'][0] != None:
    if result_table['FLUX_ERROR_I'][0] != None:
        print("M", args.target, "Cousins Ic", result_table['FLUX_I'][0],
              result_table['FLUX_ERROR_I'][0]," # ",
              result_table['FLUX_BIBCODE_I'][0].decode('utf-8'))  
    else:
        print("M", args.target, "Cousins Ic", result_table['FLUX_I'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_I'][0].decode('utf-8'),"; e_mag set to 0.05") 

if result_table['FLUX_J'][0] != None:
    if result_table['FLUX_ERROR_J'][0] != None:
        print("M", args.target, "2MASS J", result_table['FLUX_J'][0],
              result_table['FLUX_ERROR_J'][0]," # ",
              result_table['FLUX_BIBCODE_J'][0].decode('utf-8'))
    else:
        print("M", args.target, "2MASS J", result_table['FLUX_J'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_J'][0].decode('utf-8'),"; e_mag set to 0.05")         

if result_table['FLUX_H'][0] != None:
    if result_table['FLUX_ERROR_H'][0] != None:
        print("M", args.target, "2MASS H", result_table['FLUX_H'][0],
              result_table['FLUX_ERROR_H'][0]," # ",
              result_table['FLUX_BIBCODE_H'][0].decode('utf-8'))
    else:
        print("M", args.target, "2MASS H", result_table['FLUX_H'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_H'][0].decode('utf-8'),"; e_mag set to 0.05")         

if result_table['FLUX_K'][0] != None:
    if result_table['FLUX_ERROR_K'][0] != None:
        print("M", args.target, "2MASS Ks", result_table['FLUX_K'][0],
              result_table['FLUX_ERROR_K'][0]," # ",
              result_table['FLUX_BIBCODE_K'][0].decode('utf-8'))  
    else:
        print("M", args.target, "2MASS Ks", result_table['FLUX_K'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_K'][0].decode('utf-8'),"; e_mag set to 0.05")         

if result_table['FLUX_u'][0] != None:
    if result_table['FLUX_ERROR_u'][0] != None:
        print("M", args.target, "SDSS u", result_table['FLUX_u'][0],
              result_table['FLUX_ERROR_u'][0]," # ",
              result_table['FLUX_BIBCODE_u'][0].decode('utf-8'))
    else:
        print("M", args.target, "SDSS u", result_table['FLUX_u'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_u'][0].decode('utf-8'),"; e_mag set to 0.05")         
          
if result_table['FLUX_g'][0] != None:
    if result_table['FLUX_ERROR_g'][0] != None:
        print("M", args.target, "SDSS g", result_table['FLUX_g'][0],
              result_table['FLUX_ERROR_g'][0]," # ",
              result_table['FLUX_BIBCODE_g'][0].decode('utf-8'))          
    else:
        print("M", args.target, "SDSS g", result_table['FLUX_g'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_g'][0].decode('utf-8'),"; e_mag set to 0.05")         
    
if result_table['FLUX_r'][0] != None:
    if result_table['FLUX_ERROR_r'][0] != None:
        print("M", args.target, "SDSS r", result_table['FLUX_r'][0],
              result_table['FLUX_ERROR_r'][0]," # ",
              result_table['FLUX_BIBCODE_r'][0].decode('utf-8'))    
    else:
        print("M", args.target, "SDSS r", result_table['FLUX_r'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_r'][0].decode('utf-8'),"; e_mag set to 0.05")         

if result_table['FLUX_i'][0] != None:
    if result_table['FLUX_ERROR_i'][0] != None:
        print("M", args.target, "SDSS i", result_table['FLUX_i'][0],
              result_table['FLUX_ERROR_i'][0]," # ",
              result_table['FLUX_BIBCODE_i'][0].decode('utf-8'))
    else:
        print("M", args.target, "SDSS i", result_table['FLUX_i'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_i'][0].decode('utf-8'),"; e_mag set to 0.05")         

if result_table['FLUX_z'][0] != None:
    if result_table['FLUX_ERROR_z'][0] != None:
        print("M", args.target, "SDSS z", result_table['FLUX_z'][0],
              result_table['FLUX_ERROR_z'][0]," # ",
              result_table['FLUX_BIBCODE_z'][0].decode('utf-8'))
    else:
        print("M", args.target, "SDSS z", result_table['FLUX_z'][0], "0.05 # ",
              result_table['FLUX_BIBCODE_z'][0].decode('utf-8'),"; e_mag set to 0.05")         

print("#")
    

#2: get Tycho magnitudes from vizier (Tycho2 catalog and supplements)
    
# need to request all columns since by default, no error columns are returned.    
vquery=Vizier(columns=["**"])

# query catalogs
res = vquery.query_object(args.target,catalog=["I/259/tyc2",
                                               "I/259/suppl_1",
                                               "I/259/suppl_2"])

# some weird but necessary type conversion stuff
for table_name in res.keys(): tyc2table = res[table_name]

# print results
if len(res) > 0: # to make sure star is in the catalog; fails otherwise
    print("#")
    print("# Tycho 2")
    print("#")
    if tyc2table['BTmag'][0] != None:
        print("M", args.target, "Tycho Bt", tyc2table['BTmag'][0],
              tyc2table['e_BTmag'][0]," # ",
              "2000A&A...355L..27H")
    
    if tyc2table['VTmag'][0] != None:
        print("M", args.target, "Tycho Vt", tyc2table['VTmag'][0],
              tyc2table['e_VTmag'][0]," # ",
              "2000A&A...355L..27H")
    print("#")

    
#3: get Hipparcos magnitude from vizier (Hipparcos 2 catalog from 2007)
  
hipres = vquery.query_object(args.target,catalog=["I/311/hip2"])

for hiptable_name in hipres.keys(): hip2table = hipres[hiptable_name]

if len(hipres) > 0:
    print("#")
    print("# Hipparcos")
    print("#")
    if hip2table['Hpmag'][0] != None:
        print("M", args.target, "Hipparcos Hp", hip2table['Hpmag'][0],
              hip2table['e_Hpmag'][0]," # ",
              "2007A&A...474..653V")
    print("#")


#4: get 13-color magnitudes from vizier (Johnson+1975)
  
tcres = vquery.query_object(args.target,catalog=["II/84/catalog"])

for tctable_name in tcres.keys(): tctable = tcres[tctable_name]

if len(tcres) > 0: 
    print("#")
    print("# 13-color photometry: 1975RMxAA...1..299J")
    print("#")
    if tctable['_52'][0] != None:
        print("M", args.target, "13color m52", tctable['_52'][0],
              "0.05"," # ","e_mag set to 0.05")
    if tctable['_33-52'][0] != None:
        m33 = tctable['_33-52'][0] + tctable['_52'][0]
        print("M %.22s 13color m33 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m33))      
    if tctable['_35-52'][0] != None:
        m35 = tctable['_35-52'][0] + tctable['_52'][0]
        print("M %.22s 13color m35 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m35))     
    if tctable['_37-52'][0] != None:
        m37 = tctable['_37-52'][0] + tctable['_52'][0]
        print("M %.22s 13color m37 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m37))  
    if tctable['_40-52'][0] != None:
        m40 = tctable['_40-52'][0] + tctable['_52'][0]
        print("M %.22s 13color m40 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m40))  
    if tctable['_45-52'][0] != None:
        m45 = tctable['_45-52'][0] + tctable['_52'][0]
        print("M %.22s 13color m45 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m45))  
    if tctable['_52-58'][0] != None:
        m58 = -1.0 * (tctable['_52-58'][0] - tctable['_52'][0])
        print("M %.22s 13color m58 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m58))  
    if tctable['_52-63'][0] != None:
        m63 = -1.0 * (tctable['_52-63'][0] - tctable['_52'][0])
        print("M %.22s 13color m63 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m63)) 
    if tctable['_52-72'][0] != None:
        m72 = -1.0 * (tctable['_52-72'][0] - tctable['_52'][0])
        print("M %.22s 13color m72 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m72)) 
    if tctable['_52-80'][0] != None:
        m80 = -1.0 * (tctable['_52-80'][0] - tctable['_52'][0])
        print("M %.22s 13color m80 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m80))         
    if tctable['_52-86'][0] != None:
        m86 = -1.0 * (tctable['_52-86'][0] - tctable['_52'][0])
        print("M %.22s 13color m86 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m86))        
    if tctable['_52-99'][0] != None:
        m99 = -1.0 * (tctable['_52-99'][0] - tctable['_52'][0])
        print("M %.22s 13color m99 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m99))         
    if tctable['_52-110'][0] != None:
        m110 = -1.0 * (tctable['_52-110'][0] - tctable['_52'][0])
        print("M %.22s 13color m110 %.3f 0.05  #  e_mag set to 0.05" 
              % (args.target, m110))
    print("#")


#5: get IRAS fluxes
        
irres = vquery.query_object(args.target,catalog=["II/125/main"])

for irtable_name in irres.keys(): irtable = irres[irtable_name]

if len(irres) > 0: 
    print("#")
    print("# IRAS Fluxes: 1988IRASP.C......0J and 1988NASAR1190....1B")
    print("#")
    if irtable['Fnu_12'][0] != None:
        if irtable['q_Fnu_12'][0] > 1.0:
            e_Fnu_12 = irtable['Fnu_12'][0] * irtable['e_Fnu_12'][0] / 100.0
            print("Fn %.22s 12000 2000 %.3f %.3f  #  IRAS" 
                  % (args.target, irtable['Fnu_12'][0], e_Fnu_12))
    if irtable['Fnu_25'][0] != None:
        if irtable['q_Fnu_25'][0] > 1.0:
            e_Fnu_25 = irtable['Fnu_25'][0] * irtable['e_Fnu_25'][0] / 100.0
            print("Fn %.22s 25000 8000 %.3f %.3f  #  IRAS" 
                  % (args.target, irtable['Fnu_25'][0], e_Fnu_25))
    if irtable['Fnu_60'][0] != None:
        if irtable['q_Fnu_60'][0] > 1.0:
            e_Fnu_60 = irtable['Fnu_60'][0] * irtable['e_Fnu_60'][0] / 100.0
            print("Fn %.22s 60000 12000 %.3f %.3f  #  IRAS" 
                  % (args.target, irtable['Fnu_60'][0], e_Fnu_60))
    print("#")
            

#6: get Caltech Infrared Observations (CIO)

ciores = vquery.query_object(args.target,catalog=["II/225/catalog"])

for ciotable_name in ciores.keys(): ciotable = ciores[ciotable_name]  

# the catalog contains many different IR observations at different 
# wavelengths. Need to sort out flux values from IRAS (already obtained, see
# above; from the "actual" source). 


if len(ciores) > 0: 
    print("#")
    print("# CIO data: 1999yCat.2225....0G and 1993cio..book.....G")
    print("e_mag set to 0.05")
    print("#")
    for n in range(len(ciotable)):
        if (ciotable['x_F_IR_'][n] == "M") or (ciotable['x_F_IR_'][n] == "C"):
            wavelength = 1000.0 * ciotable['lambda'][n] # convert to nm
            fakefilterwidth = 200. * ciotable['lambda'][n] # actual number 
                                                          # impossible to get
            fakeerror = 0.05 # no actual errors given, similar to above
            print("M %.22s %d %d %.2f %.2f" 
                  % (args.target, wavelength, fakefilterwidth, ciotable['F_IR_'][n],
                     fakeerror))
    print("#")
       
        
#7: get COBE/DIRBE point source catlog data -- 
# these data previously came from the MSX text file. 
    
dirberes = vquery.query_object(args.target,catalog=["J/ApJS/154/673/DIRBE"])
for dirbetable_name in dirberes.keys(): dirbetable = dirberes[dirbetable_name]

if len(dirberes) > 0:
    print("#")
    print("# COBE / DIRBE Point Source Catalog Data: 2004ApJS..154..673S")
    print("#")
    if dirbetable['F1.25'][0] != None:
        print("F %.22s 1250 310 %.1f %.1f  #  COBE/DIRBE" 
              % (args.target, dirbetable['F1.25'][0], dirbetable['e_F1.25'][0]))
    if dirbetable['F2.2'][0] != None:
        print("F %.22s 2200 361 %.1f %.1f  #  COBE/DIRBE" 
              % (args.target, dirbetable['F2.2'][0], dirbetable['e_F2.2'][0]))
    if dirbetable['F3.5'][0] != None:
        print("F %.22s 3500 898 %.1f %.1f  #  COBE/DIRBE" 
              % (args.target, dirbetable['F3.5'][0], dirbetable['e_F3.5'][0]))
    if dirbetable['F4.9'][0] != None:
        print("F %.22s 4900 712 %.1f %.1f  #  COBE/DIRBE" 
              % (args.target, dirbetable['F4.9'][0], dirbetable['e_F4.9'][0]))
    if dirbetable['F12'][0] != None and dirbetable['F12'][0] > 0.0:
        print("F %.22s 12000 6348 %.1f %.1f  #  COBE/DIRBE" 
              % (args.target, dirbetable['F12'][0], dirbetable['e_F12'][0]))
    print ("#")
           
        
# COMMENTS FOR FUTURE WORK           
           
# to do if possible: 
# query the following vizier catalogs in the absence of GCPD accessibility: 
        
#http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=II/168&-to=3
#http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=II/122B&-to=3
#http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=II/164&-to=3
#http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=II/193&-to=3
#http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=II/215&-to=3
      
# The following lines identify which systems we used to obtain via GCPD
#python ./GCPD3.py --target $1 --system UBV >> $2
#python ./GCPD3.py --target $1 --system DDO >> $2
#python ./GCPD3.py --target $1 --system uvby >> $2
#python ./GCPD3.py --target $1 --system Vilnius >> $2
#python ./GCPD3.py --target $1 --system Straizys >> $2
#python ./GCPD3.py --target $1 --system Geneva >> $2
#python ./GCPD3.py --target $1 --system Oja >> $2
#python ./GCPD3.py --target $1 --system WBVR >> $2
#python ./GCPD3.py --target $1 --system UBVRI >> $2
#python ./GCPD3.py --target $1 --system IJHKLMN >> $2
#python ./GCPD3.py --target $1 --system Alexander >> $2
           
# abandoned idea:  
# get stellar photometry from exoplanet archive.
# This is tedious since (a) it can only search for planets, and (b) it does 
# not resolve names, so we have to search for the default name, which is not 
# necessarily the HD number. 
    
# we can get the default alias by accessing the file returned by 
# https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=aliastable&objname=bet Pic
# where the end of the line is the star name. 
# The returned file contains the default alias in line 2.
# use wget or curl to get this, but i have to figure out how.

# download into memory the confirmed planets table

#exoplanet_archive_table = NasaExoplanetArchive.get_confirmed_planets_table()

# modify our search term and add 'b' to its name to make it seem like a planet
    # note: need to first check whether star is in database, will crash otherwise.

#planetdummy = ' b'
#epa_star = args.target + planetdummy

#print (epa_star)

#epa_target = NasaExoplanetArchive.query_planet(epa_star)


    