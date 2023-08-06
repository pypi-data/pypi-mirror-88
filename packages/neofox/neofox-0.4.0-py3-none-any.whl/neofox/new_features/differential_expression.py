#!/usr/bin/python
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

import math


def mean_of_list(list_numbs):
    '''
    This function takes a list of numbers as neofox and calculates the mean
    '''
    mean_list = float(sum(list_numbs) / len(list_numbs))
    return mean_list


def sd_of_list(list_numbs):
    '''
    This function takes a list of numbers as neofox and calculates the standard deviation
    '''
    mean = mean_of_list(list_numbs)
    sd_list = float((sum([((x - mean) ** 2) for x in list_numbs]) / len(list_numbs)) ** 0.5)
    return (sd_list)


def fold_change(expression_tumor, expression_reference):
    """
    This function determines the classical fold change between tumour and reference transcript expression.
    Log2(expr in tumor / expr in reference)
    """
    try:
        return str(math.log(float(expression_tumor) / float(expression_reference), 2))
    except (ValueError, ZeroDivisionError) as e:
        return "NA"


def percentile_calc(expression_tumor, expression_reference_sum):
    """
    This function calculates the expression difference between tumour and reference data in form of a percentile value.
    expr in tumor * 100 / (sum of expr in ref tissue + 1)
    """
    try:
        return str((float(expression_tumor) * 100) / (float(expression_reference_sum) + 1))
    except (ValueError, ZeroDivisionError) as e:
        return "NA"


def pepper_calc(expression_tumor, expression_reference, expression_reference_sd):
    """
    This function calculates the expression difference between tumour and reference data based on Pepper publication, in a z-score similar manner.
    expr in tumour - mean epxr in reference tissue / standard deviation of expression in refernce
    """
    try:
        return str((float(expression_tumor) - float(expression_reference)) / float(expression_reference_sd))
    except (ValueError, ZeroDivisionError) as e:
        return "NA"


# if __name__ == '__main__':
#     import sys
#     import data_import
#
#     ref_file = sys.argv[1]
#     # "/projects/CM27_IND_patients/GTEX_normal_tissue_data/Skin .csv"
#     ref_list = load_rna_expression_reference(ref_file)
#     f = sys.argv[2]
#     data = data_import.import_dat_icam(f)
#     dat_merged = merge_data_reference(data, ref_list)
#     print(wrapper_diff_expr(dat_merged)[0])
#
#     # write_ouptut_to_file(dat_epi,header)
