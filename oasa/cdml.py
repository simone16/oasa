#--------------------------------------------------------------------------
#     This file is part of OASA - a free chemical python library
#     Copyright (C) 2004 Beda Kosata <beda@zirael.org>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file gpl.txt in the
#     main directory of the program

#--------------------------------------------------------------------------

from plugin import plugin
from molecule import molecule
from atom import atom
from bond import bond
from xml import xpath
import xml.dom.minidom as dom



def read_cdml( text):
  """returns the last molecule for now"""
  doc = dom.parseString( text)
  #if doc.childNodes()[0].nodeName == 'svg':
  #  path = "/svg/cdml/molecule"
  #else:
  #  path = "/cdml/molecule"
  path = "//molecule"
  do_not_continue_this_mol = 0
  for mol_el in xpath.Evaluate( path, doc):
    atom_id_remap = {}
    mol = molecule()
    for atom_el in xpath.Evaluate( "atom", mol_el):
      name = atom_el.getAttribute( 'name')
      if not name:
        print "this molecule has an invalid symbol"
        do_not_continue_this_mol = 1
        break
      pos = xpath.Evaluate( 'point', atom_el)[0]
      z = pos.getAttribute( 'z') or 0
      a = atom( symbol=name,
                charge=atom_el.getAttribute( 'charge') or 0,
                coords=(pos.getAttribute('x'),pos.getAttribute('y'),z))
      mol.add_vertex( v=a)
      atom_id_remap[ atom_el.getAttribute( 'id')] = a

    if do_not_continue_this_mol:
      break

    for bond_el in xpath.Evaluate( "bond", mol_el):
      v1 = atom_id_remap[ bond_el.getAttribute( 'start')]
      v2 = atom_id_remap[ bond_el.getAttribute( 'end')]
      type = bond_el.getAttribute( 'type')
      e = bond( order=int( type[1]), type=type[0])
      mol.add_edge( v1, v2, e=e)

  return mol
      

##################################################
# MODULE INTERFACE

from StringIO import StringIO

reads_text = 1
reads_files = 1
writes_text = 0
writes_files = 0

def file_to_mol( f):
  return text_to_mol( f.read())

def text_to_mol( text):
  return read_cdml( text)

#
##################################################
  

##################################################
# DEMO

if __name__ == '__main__':

  import sys
  import smiles

  if len( sys.argv) < 1:
    print "you must supply a filename"
    sys.exit()

  # parsing of the file

  file_name = sys.argv[1]
  f = file( file_name, 'r')

  mol = file_to_mol( f)

  f.close()

  print mol
  print smiles.mol_to_text( mol)