#!/usr/bin/env python
#
# Copyright (c) 2020-2030 Translational Oncology at the Medical Center of the Johannes Gutenberg-University Mainz gGmbH.
#
# This file is part of Neofox
# (see https://github.com/tron-bioinformatics/neofox).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.#


class DifferentialBinding:

    def dai(self, score_mutation, score_wild_type, affin_filtering=False):
        """
        Calculates DAI: Returns difference between wt and mut MHC binding score.
        """
        # TODO: these conversions to float need to go away from here
        score = "NA"
        try:
            if affin_filtering:
                if score_mutation < 500.0:
                    score = score_wild_type - score_mutation
            else:
                score = score_wild_type - score_mutation
        except TypeError:
            score = "NA"
        return score

    def diff_number_binders(self, num_mutation, num_wild_type):
        """
        returns difference of potential candidate epitopes between mutated and wt epitope
        """
        try:
            difference = num_mutation - num_wild_type
        except TypeError:
            difference = "NA"
        return difference

    def ratio_number_binders(self, num_mutation, num_wild_type):
        """
        returns ratio of number of potential candidate epitopes between mutated and wt epitope. if no WT candidate epitopes, returns number of mutated candidate epitopes per mps
        """
        try:
            ratio = num_mutation / num_wild_type
        except ZeroDivisionError:
            ratio = "NA"
        except TypeError:
            ratio = "NA"
        return ratio

    def classify_adn_cdn(self, score_mutation, amplitude, bdg_cutoff_classical, bdg_cutoff_alternative, amplitude_cutoff,
                         category):
        """
        returns if an epitope belongs to classically and alternatively defined neoepitopes (CDN vs ADN)
        (indicate which category to examine by category)--> Rech et al, 2018
        grouping is based on affinity and affinitiy foldchange between wt and mut
        """
        group = "NA"
        try:
            if category == "CDN":
                group = str(float(score_mutation) < bdg_cutoff_classical)
            elif category == "ADN":
                group = str(float(score_mutation) < bdg_cutoff_alternative and float(amplitude) > amplitude_cutoff)
        except ValueError:
            group = "NA"
        return group


