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
from logzero import logger

from neofox.helpers import intermediate_files
from neofox.helpers.blastp_runner import BlastpRunner


class NeoantigenFitnessCalculator(BlastpRunner):

    def __init__(self, runner, configuration, iedb):
        """
        :type runner: neofox.helpers.runner.Runner
        :type configuration: neofox.references.DependenciesConfiguration
        """
        super().__init__(runner, configuration)
        self.iedb = iedb

    def _calc_pathogen_similarity(self, fasta_file):
        """
        This function determines the PATHOGENSIMILARITY of epitopes according to Balachandran et al. using a blast
        search against the IEDB pathogenepitope database
        """
        outfile = self.run_blastp(fasta_file=fasta_file, database=os.path.join(self.iedb, "iedb_blast_db"))
        similarity = self.parse_blastp_output(blastp_output_file=outfile)
        os.remove(outfile)
        return similarity

    def wrap_pathogen_similarity(self, mutation):
        fastafile = intermediate_files.create_temp_fasta(sequences=[mutation], prefix="tmpseq", comment_prefix='M_')
        try:
            pathsim = self._calc_pathogen_similarity(fastafile)
        except Exception as ex:
            # TODO: do we need this at all? it should not fail and if it fails we probably want to just stop execution
            logger.exception(ex)
            pathsim = 0
        os.remove(fastafile)
        logger.info("Peptide {} has a pathogen similarity of {}".format(mutation, pathsim))
        return str(pathsim)

    def calculate_amplitude_mhc(self, score_mutation, score_wild_type, apply_correction=False):
        """
        This function calculates the amplitude between mutated and wt epitope according to Balachandran et al.
        when affinity is used, use correction from Luksza et al. *1/(1+0.0003*aff_wt)
        """
        amplitude_mhc = "NA"
        try:
            candidate_amplitude_mhc = float(score_wild_type) / float(score_mutation)
            if apply_correction:  #nine_mer or affinity:
                amplitude_mhc = str(candidate_amplitude_mhc * (self._calculate_correction(score_wild_type)))
            else:
                amplitude_mhc = str(candidate_amplitude_mhc)
        except(ZeroDivisionError, ValueError) as e:
            pass
        return amplitude_mhc

    def _calculate_correction(self, score_wild_type):
        return 1 / (1 + 0.0003 * float(score_wild_type))

    def calculate_recognition_potential(
            self, amplitude, pathogen_similarity, mutation_in_anchor, mhc_affinity_mut=None):
        """
        This function calculates the recognition potential, defined by the product of amplitude and pathogensimiliarity of an epitope according to Balachandran et al.
        F_alpha = - max (A_i x R_i)

        Returns (A_i x R_i) value only for nonanchor mutation and epitopes of length 9; only considered by Balachandran
        """
        recognition_potential = "NA"
        try:
            candidate_recognition_potential = str(float(amplitude) * float(pathogen_similarity))
            if mhc_affinity_mut:
                if mutation_in_anchor == "0" and float(mhc_affinity_mut) < 500.0:
                    recognition_potential = candidate_recognition_potential
            else:
                if mutation_in_anchor == "0":
                    recognition_potential = candidate_recognition_potential
        except ValueError:
            pass
        return recognition_potential
