# Copyright (c) 2014, RSN#86. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 of the
# License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301  USA

# MySQL Workbench Plugin - Written in MySQL Workbench 6.2.3

# An utility to generate data dictionaries (DBDoc)

# Install it through Scripting/Install Plugin/Module menu
# select DBDocPy_grt.py file, restart MWB for the change to take effect.

# It can be accessed through Tools/Catalog menu, there are 2 options:
# A text version, displayed at MWB console
# An HTML version, exported to a file

# Notes: I've never programmed in Python before, take it in mind and please be kind.
# Any suggestions are welcome. You can leave your contribution, or check, for updates at:
# https://github.com/rsn86/MWB-DBDocPy

from wb import *
import grt
from mforms import FileChooser
import mforms

ModuleInfo = DefineModule(name="DBDocPy", author="Rodrigo Schmidt Nurmberg", version="1.0", description="Data Dictionary")

@ModuleInfo.plugin("rsn86.DBDocPy.htmlDataDictionary", caption="DBDoc: As HTML File", description="Data Dictionary as HTML", input=[wbinputs.currentCatalog()], pluginMenu="Catalog")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def htmlDataDictionary(catalog):
  # Put plugin contents here
  htmlOut = ""
  filechooser = FileChooser(mforms.SaveFile)
  if filechooser.run_modal():
    htmlOut = filechooser.get_path()
    print "HTML File: %s" % (htmlOut)
  if len(htmlOut) <= 1:
    return 1

  # iterate through columns from schema
  schema = catalog.schemata[0]
  htmlFile = open(htmlOut, "w")
  print >>htmlFile, "<html><head>"
  print >>htmlFile, "<title>Data dictionary: %s</title>" % (schema.name)
  print >>htmlFile, """<style>
    td,th {
      text-align:center; 
      vertical-align:middle;
    }
    table {
      border-collapse: collapse;
    }
    caption, th, td {
      padding: .2em .8em;
      border: 1px solid #fff;
    }
    caption {
      background: #dbb768;
      font-weight: bold;
      font-size: 1.1em;
    }
    th {
      font-weight: bold;
      background: #f3ce7d;
    }
    td {
      background: #ffea97;
    }
  </style>
</head>
<body>"""
  for table in schema.tables:
    print >>htmlFile, "<table><caption>Table: %s - %s</caption>" % (table.name, table.comment)
    print >>htmlFile, """<tr><td colspan=\"7\">Attributes</td></tr>
<tr>
<th>Name</th>
<th>Type</th>
<th>Not Null</th>
<th>PK</th>
<th>FK</th>
<th>Default</th>
<th>Comment</th>
</tr>"""
    for column in table.columns:
      pk = ('No', 'Yes')[bool(table.isPrimaryKeyColumn(column))]
      fk = ('No', 'Yes')[bool(table.isForeignKeyColumn(column))]
      nn = ('No', 'Yes')[bool(column.isNotNull)]
      print >>htmlFile, "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (column.name,column.formattedType,nn,pk,fk,column.defaultValue,column.comment)
    print >>htmlFile, "</table></br>"
  print >>htmlFile, "</body></html>"
  return 0

@ModuleInfo.plugin("rsn86.DBDocPy.consoleDataDictionary", caption="DBDoc: Output to console", description="Data Dictionary as Text", input=[wbinputs.currentCatalog()], pluginMenu="Catalog")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def consoleDataDictionary(catalog):
  # Put plugin contents here
  # iterate through columns from schema
  schema = catalog.schemata[0]
  print "Schema: %s" % (schema.name)
  for table in schema.tables:
    print "\tTable: %s - %s" % (table.name, table.comment)
    for column in table.columns:
      pk = ('No', 'Yes')[bool(table.isPrimaryKeyColumn(column))]
      fk = ('No', 'Yes')[bool(table.isForeignKeyColumn(column))]
      nn = ('No', 'Yes')[bool(column.isNotNull)]
      print "\t\tName: %s, Type: %s, NN: %s, PK: %s, FK: %s, Default: %s, Comment: %s" % (column.name, column.formattedType, nn, pk, fk, column.defaultValue, column.comment)
#      print "\t\t\tFormated Type: %s" % column.formattedType
#      print "\t\tFormated RAW Type: %s" % column.formattedRawType
#      print "\t\tSimple Type: %s" % column.simpleType
#      print "\t\tStructured Type: %s" % column.structuredType
#      print "\t\tUser Type: %s" % column.userType
  return 0

