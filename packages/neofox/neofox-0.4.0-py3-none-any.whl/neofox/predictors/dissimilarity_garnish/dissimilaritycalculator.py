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

import os
import os.path

from neofox.helpers import intermediate_files
from neofox.helpers.blastp_runner import BlastpRunner


class DissimilarityCalculator(BlastpRunner):

    def __init__(self, runner, configuration, proteome_db):
        """
        :type runner: neofox.helpers.runner.Runner
        :type configuration: neofox.references.DependenciesConfiguration
        """
        super().__init__(runner=runner, configuration=configuration)
        self.proteome_db = proteome_db

    def _calc_dissimilarity(self, fasta_file):
        """
        This function determines the dissimilarity to self-proteome of epitopes as described in Richman et al
        """
        outfile = self.run_blastp(
            fasta_file=fasta_file, database=os.path.join(self.proteome_db, "homo_sapiens.mod"))
        similarity = self.parse_blastp_output(blastp_output_file=outfile, a=32)
        dissimilarity = 1 - similarity
        os.remove(outfile)
        return dissimilarity

    def calculate_dissimilarity(self, mhc_mutation, mhc_affinity, filter_binder=False):
        """
        wrapper for dissimilarity calculation
        """
        fastafile = intermediate_files.create_temp_fasta(sequences=[mhc_mutation], prefix="tmp_dissimilarity_", comment_prefix='M_')
        dissim = self._calc_dissimilarity(fastafile)
        os.remove(fastafile)
        sc = dissim
        if filter_binder and float(mhc_affinity) >= 500:
            sc = "NA"
        return sc
