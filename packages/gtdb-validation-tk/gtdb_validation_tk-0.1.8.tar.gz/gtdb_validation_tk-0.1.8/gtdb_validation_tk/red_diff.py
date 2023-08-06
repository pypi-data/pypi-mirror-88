###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################


import os
import sys
import logging
import re
import ast

import dendropy


class Taxa(object):
    def __init__(self, name, r=1):
        self.name = name
        self.reds = ['N/A'] * r
        self.distances = ['N/A'] * r
        self.medians = ['N/A'] * r


class RedDiff(object):
    """Class listing functions for RED analysis.

    """

    def __init__(self):
        """Initialize."""
        self.logger = logging.getLogger()
        self.order_rank = ["d__", "p__", "c__", "o__", 'f__', 'g__', 's__']
        self.oneletter = {"domain": "d__",
                          "phylum": "p__",
                          "class": "c__",
                          "order": "o__",
                          "family": 'f__',
                          "genus": 'g__',
                          "species": 's__'}

    def reddiff(self, releases, output_file):
        outf = open(output_file, 'w')
        rank_dict = {k: {} for k in self.order_rank}
        number_or_releases = len(releases)
        versions = []

        header = ['Taxa']
        red_header = ['N/A'] * number_or_releases
        distance_header = ['N/A'] * number_or_releases
        median_header = ['N/A'] * number_or_releases
        for i, release in enumerate(releases):

            version, red_file, dict_file = release
            red_header[i] = 'RED value for release {}'.format(version)
            distance_header[i] = 'RED to median for release {}'.format(version)
            median_header[i] = 'rank median for release {}'.format(version)
            versions.append(version)
            dict_red = self.parse_dictfile(dict_file)

            with open(red_file, 'r') as rf:
                rf.readline()
                for line in rf:
                    taxa, taxonomy, red, meddiff = line.strip('\n').split('\t')[
                        0:4]
                    rk = taxa[0:3]
                    if taxa in rank_dict.get(rk):
                        taxtoupdate = rank_dict.get(rk).get(taxa)
                        taxtoupdate.reds[i] = red
                        taxtoupdate.distances[i] = meddiff
                        taxtoupdate.medians[i] = dict_red.get(rk)
                    else:
                        newtaxa = Taxa(taxa, number_or_releases)
                        newtaxa.reds[i] = red
                        newtaxa.distances[i] = meddiff
                        newtaxa.medians[i] = dict_red.get(rk)
                        rank_dict[rk][taxa] = newtaxa

        header.extend(red_header)
        header.extend(distance_header)
        header.extend(median_header)
        outf.write('{}\n'.format('\t'.join(header)))
        for rankletter in self.order_rank:
            if rankletter in rank_dict:
                for name, information in rank_dict.get(rankletter).items():
                    line_to_print = [name]
                    line_to_print.extend(information.reds)
                    line_to_print.extend(information.distances)
                    line_to_print.extend(information.medians)
                    outf.write('{}\n'.format(
                        '\t'.join([str(x) for x in line_to_print])))

    def parse_dictfile(self, dict_file):
        s = open(dict_file, 'r').read()
        temp_dict = ast.literal_eval(s)
        result = {self.oneletter.get(k): v for k, v in temp_dict.items()}
        return result
