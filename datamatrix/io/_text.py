# -*- coding: utf-8 -*-

"""
This file is part of datamatrix.

datamatrix is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

datamatrix is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with datamatrix.  If not, see <http://www.gnu.org/licenses/>.
"""

from datamatrix.py3compat import *
from datamatrix import DataMatrix, MixedColumn
import os
import csv
import collections


def readtxt(path, delimiter=',', quotechar='"', default_col_type=MixedColumn):

	"""
	desc:
		Reads a DataMatrix from a csv file.

	arguments:
		path:	The path to the pickle file.

	keywords:
		delimiter:			The delimiter characer.
		quotechar:			The quote character.
		default_col_type:	The default column type.

	returns:
		A DataMatrix.
	"""

	d = collections.OrderedDict()
	with open(path, u'Ur') as csvfile:
		reader = csv.reader(csvfile, delimiter=delimiter,
			quotechar=quotechar)
		for column in next(reader):
			d[column] = []
		for row in reader:
			all_columns = list(d.keys())
			for column, val in zip(d.keys(), row):
				all_columns.remove(column)
				d[column].append(val)
			for column in all_columns:
				warn(u'Some rows miss column %s' % column)
				d[column].append(u'')
	dm = DataMatrix(default_col_type=default_col_type)._fromdict(d)
	return dm


def writetxt(dm, path, delimiter=',', quotechar='"'):

	"""
	desc:
		Writes a DataMatrix to a csv file.

	arguments:
		dm:		The DataMatrix to write.
		path:	The path to the pickle file.

	keywords:
		delimiter:			The delimiter characer.
		quotechar:			The quote character.
	"""

	if not dm.is_2d:
		raise TypeError('Can only write 2D DataMatrix objects to csv')
	try:
		os.makedirs(os.path.dirname(path))
	except:
		pass
	with open(path, 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
		writer.writerow([safe_str(colname) for colname in dm.column_names])
		for row in dm:
			writer.writerow([safe_str(value) for colname, value in row])
