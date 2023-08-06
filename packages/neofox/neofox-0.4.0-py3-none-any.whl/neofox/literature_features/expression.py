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


class Expression:

    def rna_expression_mutation(self, transcript_expression, vaf_rna):
        """
        This function calculates the product of VAF in RNA and transcript expression
        to reflect the expression of the mutated transcript
        """
        try:
            expression_mut = transcript_expression * float(vaf_rna) if float(vaf_rna) >= 0.0 else "NA"
        except ValueError:
            expression_mut = "NA"
        return expression_mut

    def rna_expression_mutation_tc(self, expression_mutation, tumor_content):
        """
        calculated expression of mutation corrected by tumour content
        """
        try:
            expression_mut_tc = expression_mutation / tumor_content
        except (TypeError, ZeroDivisionError) as e:
            expression_mut_tc = "NA"
        return expression_mut_tc

