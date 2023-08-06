###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #r
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = "Donovan Parks"
__copyright__ = "Copyright 2017"
__credits__ = ["Donovan Parks"]
__license__ = "GPL3"
__maintainer__ = "Donovan Parks"
__email__ = "donovan.parks@gmail.com"
__status__ = "Development"

import argparse
import logging
import ntpath
import os
import sys
from biolib.common import make_sure_path_exists
from biolib.misc.custom_help_formatter import CustomHelpFormatter

from gtdb_validation_tk import __version__
from gtdb_validation_tk.main import OptionsParser


def print_help():
    """Help menu."""

    print('')
    print('                ...::: GTDB Validation Toolkit v' + __version__ + ' :::...''')
    print('''\

    Taxonomy validation:
      check_file      -> Verify formatting of taxonomy file and check taxon names
      check_tree      -> Verify taxonomy of decorated tree and check for polyphyletic groups
      red_check       -> Report taxa with unexpected RED values
      missing_genera  -> Report lineages that may represent missing genus names
      merge_genera    -> Report polyphyletic genera that are candidates for merging
      support         -> Report taxa with low support values 
      check_spelling  -> Report taxa with potential typos based on previous taxonomy

    Tree validation
      branch_len -> Calculate the mean branch length from root to extant taxa (expected to be ~1.0)

    Species validation:
      check_generic    -> Verify that generic name of species is valid
      check_specific   -> Verify that specific name of species is valid
      species_clusters -> Verify classification of genomes assigned to the same species cluster
      type_strains     -> Compare GTDB to type strain of species designations at NCBI, LPSN, DSMZ, and/or StrainInfo
      type_species     -> Compare GTDB to type species of genus designations at NCBI, LPSN, DSMZ, and/or StrainInfo

    Taxonomy finalization:
      backfill -> Fill in missing rank information and finalize species names

    Species comparison:
      ncbi_species      -> Report differences between GTDB and NCBI species names
      gtdb_cluster_ncbi -> Report NCBI species within each GTDB-defined cluster

    RED comparison:
      red_diff  -> Report RED values accross 2 GTDB releases

    Taxonomy comparison:
      check_distrib -> Report changes of genomes distribution between different taxonomies
      tax_diff      -> Determine differences between two taxonomy files
      tree_diff     -> Report bootstrap supported topological differences between trees
      retired_taxa  -> Report all taxa that have been retired (lost?) between two taxonomy files

    Curation tree methods:
      add_dummy     -> Add a zero branch length sister node to each current leaf node
      remove_dummy  -> Remove dummy nodes from curation tree

    General curation methods:
      val_table     -> Validation table containing useful information for all representative genomes
      suffix_table  -> Create table indicating last polyphyly suffix used for each taxon
      ncbi_tax_diff -> Establish changes in NCBI taxonomy that may impact GTDB taxonomy

  Use: gtdb_validation_tk <command> -h for command specific help.

  Feature requests or bug reports can be sent to Donovan Parks (donovan.parks@gmail.com)
    or posted on GitHub (https://github.com/Ecogenomics/gtdb_validation_tk).
    ''')


def logger_setup(output_dir, silent):
    """Set logging for application.

    Parameters
    ----------
    output_dir : str
        Output directory for log file.
    silent : boolean
        Flag indicating if output to stdout should be suppressed.
    """

    # setup general properties of logger
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter(fmt="[%(asctime)s] %(levelname)s: %(message)s",
                                   datefmt="%Y-%m-%d %H:%M:%S")

    # setup logging to console
    if not silent:
        stream_logger = logging.StreamHandler(sys.stdout)
        stream_logger.setFormatter(log_format)
        stream_logger.setLevel(logging.DEBUG)
        logger.addHandler(stream_logger)

    if output_dir:
        make_sure_path_exists(output_dir)
        file_logger = logging.FileHandler(os.path.join(output_dir, 'gtdb_validation_tk.log'), 'a')
        file_logger.setFormatter(log_format)
        logger.addHandler(file_logger)

    logger.info('GTDB Validation Toolkit v%s' % __version__)
    logger.info(ntpath.basename(sys.argv[0]) + ' ' + ' '.join(sys.argv[1:]))


def main():
    # initialize the options parser
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(help="--", dest='subparser_name')

    # validate taxonomy file
    check_file_parser = subparsers.add_parser('check_file',
                                              formatter_class=CustomHelpFormatter,
                                              description='Verify taxonomy file is formatted as expected.')
    check_file_parser.add_argument('input_taxonomy', help='input taxonomy file')
    check_file_parser.add_argument('--include_species', help="include species in validation checks",
                                   action='store_true')
    check_file_parser.add_argument('--silent', help="suppress output", action='store_true')

    # validate decorated tree
    check_tree_parser = subparsers.add_parser('check_tree',
                                              formatter_class=CustomHelpFormatter,
                                              description='Verify taxonomy of decorated tree and check for polyphyletic groups.')
    check_tree_parser.add_argument('decorated_tree', help='decorated tree to validate')
    check_tree_parser.add_argument('--taxonomy_file',
                                   help='alternative taxonomy to validate with respect to the input tree')
    check_tree_parser.add_argument('--include_species', help="include species in validation checks",
                                   action='store_true')
    check_tree_parser.add_argument('--silent', help="suppress output", action='store_true')

    # check polyphyly suffix
    check_suffix_parser = subparsers.add_parser('check_suffix',
                                                formatter_class=CustomHelpFormatter,
                                                description='Report taxa with potentially erroneous polyphyly suffix designations.')
    check_suffix_parser.add_argument('input_taxonomy', help='input taxonomy file')
    check_suffix_parser.add_argument('--include_species', help="include species in validation checks",
                                     action='store_true')
    check_suffix_parser.add_argument('--silent', help="suppress output", action='store_true')

    # report taxa with unexpected RED values
    red_check_parser = subparsers.add_parser('red_check',
                                             formatter_class=CustomHelpFormatter,
                                             description='Report taxa with unexpected RED values.')
    red_check_parser.add_argument('scaled_tree',
                                  help='scaled and decorated validation tree to check for missing genus names')
    red_check_parser.add_argument('red_dictionary',
                                  help='file with RED values for validation tree (*.dict file from phylorank outlier)')
    red_check_parser.add_argument('output_file', help='output file')
    red_check_parser.add_argument('--silent', help="suppress output", action='store_true')

    # check for potentially missing genera
    missing_genera_parser = subparsers.add_parser('missing_genera',
                                                  formatter_class=CustomHelpFormatter,
                                                  description='Report lineages that may represent missing genus names.')
    missing_genera_parser.add_argument('scaled_tree', help='scaled and decorated tree to check for missing genus names')
    missing_genera_parser.add_argument('red_dictionary',
                                       help='file with RED values (*.dict file from phylorank outlier)')
    missing_genera_parser.add_argument('gtdb_prev_taxonomy', help='GTDB taxonomy file for previous GTDB release')
    missing_genera_parser.add_argument('ncbi_taxonomy', help='NCBI taxonomy file for current GTDB release')
    missing_genera_parser.add_argument('output_file', help='output file')
    missing_genera_parser.add_argument('--silent', help="suppress output", action='store_true')

    # check for sister genera that could be merged
    merge_genera_parser = subparsers.add_parser('merge_genera',
                                                formatter_class=CustomHelpFormatter,
                                                description='Report polyphyletic genera that are candidates for merging.')
    merge_genera_parser.add_argument('scaled_tree', help='scaled and decorated tree to check for missing genus names')
    merge_genera_parser.add_argument('red_dictionary', help='file with RED values (*.dict file from phylorank outlier)')
    merge_genera_parser.add_argument('output_file', help='output file')
    merge_genera_parser.add_argument('--silent', help="suppress output", action='store_true')

    # report taxa with low support values
    support_parser = subparsers.add_parser('support',
                                           formatter_class=CustomHelpFormatter,
                                           description='Report taxa with low support values.')
    support_parser.add_argument('decorated_tree', help='decorated tree to validate')
    support_parser.add_argument('--min_support', help='report all taxa below this support value', type=int, default=70)
    support_parser.add_argument('--silent', help="suppress output", action='store_true')

    # report RED values for 2 GTDB releases
    red_diff_parser = subparsers.add_parser('red_diff',
                                            formatter_class=CustomHelpFormatter,
                                            description='Report RED values for 2+ GTDB releases.')
    red_diff_parser.add_argument('-r', '--release', nargs=3, action='append',
                                 help='--release <version> <RED values> <dictionary>')
    red_diff_parser.add_argument('-o', '--output_file', help='Output file.')
    red_diff_parser.add_argument('--silent', help="suppress output", action='store_true')

    # difference between two taxonomy files
    tax_diff_parser = subparsers.add_parser('tax_diff',
                                            formatter_class=CustomHelpFormatter,
                                            description='Determine differences between two taxonomy files.')
    tax_diff_parser.add_argument('input_taxonomy1', help='first taxonomy file')
    tax_diff_parser.add_argument('input_taxonomy2', help='second taxonomy file')
    tax_diff_parser.add_argument('output_dir', help="output directory")
    tax_diff_parser.add_argument('--gtdb_metadata_file',
                                 help='file specifying GTDB metadata (TSV) if type material fields are desired')
    tax_diff_parser.add_argument('--silent', help="suppress output", action='store_true')

    # quanitify differences between two trees
    tree_diff_parser = subparsers.add_parser('tree_diff',
                                             formatter_class=CustomHelpFormatter,
                                             description='Quantify bootstrap supported topological differences between trees.')

    tree_diff_parser.add_argument('input_tree1', help="first decorated input tree")
    tree_diff_parser.add_argument('input_tree2', help="second decorated input tree")
    tree_diff_parser.add_argument('output_dir', help="output directory")
    tree_diff_parser.add_argument('--min_support', help="minimum value to consider a lineage well supported",
                                  type=float, default=90.0)
    tree_diff_parser.add_argument('--min_taxa', help="only consider lineage with sufficient number of taxa", type=int,
                                  default=2)
    tree_diff_parser.add_argument('--silent', help="suppress output", action='store_true')

    # difference between two taxonomy files
    retired_taxa_parser = subparsers.add_parser('retired_taxa',
                                                formatter_class=CustomHelpFormatter,
                                                description='Report all taxa that have been retired (lost?) between two taxonomy files.')
    retired_taxa_parser.add_argument('new_taxonomy_file', help='file with new taxonomy')
    retired_taxa_parser.add_argument('prev_taxonomy_file', help='file with previous taxonomy')
    retired_taxa_parser.add_argument('output_table', help="output table")
    retired_taxa_parser.add_argument('--silent', help="suppress output", action='store_true')

    # calculate mean root to tip branch length
    branch_len_parser = subparsers.add_parser('branch_len',
                                              formatter_class=CustomHelpFormatter,
                                              description='Calculate the mean branch length from root to extant taxa.')

    branch_len_parser.add_argument('input_tree', help="tree to interest")
    branch_len_parser.add_argument('--silent', help="suppress output", action='store_true')

    # check taxonomy for spelling mistakes
    check_spelling_parser = subparsers.add_parser('check_spelling',
                                                  formatter_class=CustomHelpFormatter,
                                                  description='Report taxa with potential typos based on previous taxonomy.')
    check_spelling_parser.add_argument('input_taxonomy1', help='current taxonomy file')
    check_spelling_parser.add_argument('input_taxonomy2', help='previous, or otherwise trusted, taxonomy file')
    check_spelling_parser.add_argument('output_file', help="output directory")
    check_spelling_parser.add_argument('--dist', help='Levenshtein distance threshold', default=95)
    check_spelling_parser.add_argument('--silent', help="suppress output", action='store_true')

    # list which group has been split/modified between gtdb iterations
    check_dist_parser = subparsers.add_parser('check_distrib',
                                              formatter_class=CustomHelpFormatter,
                                              description='Check genome distribution changes between 2 taxonomies.')
    check_dist_parser.add_argument('input_taxonomy1', help='current taxonomy file')
    check_dist_parser.add_argument('input_taxonomy2', help='previous taxonomy file')
    check_dist_parser.add_argument('output_dir', help="output directory")
    check_dist_parser.add_argument('--keep_no_change',
                                   help="keep all ranks regardless of whether they are the same in both taxonomies",
                                   action='store_false', default='store_true')
    check_dist_parser.add_argument('--keep_placeholder_name',
                                   help='keep ranks that have a placeholder name->no name in the taxonomies',
                                   action='store_false', default='store_true')
    check_dist_parser.add_argument('--top_change', help='keep only top change', action='store_true',
                                   default='store_false')
    check_dist_parser.add_argument('--silent', help="suppress output", action='store_true')

    # general validation table
    val_table_parser = subparsers.add_parser('val_table',
                                             formatter_class=CustomHelpFormatter,
                                             description='Validation table containing useful information for all representative genomes.')
    val_table_parser.add_argument('input_taxonomy', help='input taxonomy file')
    val_table_parser.add_argument('gtdb_metadata_file', help='file specifying GTDB metadata (TSV)')
    val_table_parser.add_argument('output_table', help='output table')
    val_table_parser.add_argument('--silent', help="suppress output", action='store_true')

    # suffix table
    suffix_table_parser = subparsers.add_parser('suffix_table',
                                                formatter_class=CustomHelpFormatter,
                                                description='Create table indicating last polyphyly suffix used for each taxon.')
    suffix_table_parser.add_argument('output_table', help="output directory")
    suffix_table_parser.add_argument('--input_taxonomy',
                                     help="additional taxonomy table to use for establishing suffix table")
    suffix_table_parser.add_argument('--silent', help="suppress output", action='store_true')

    # establish changes in NCBI taxonomy that may impact GTDB taxonomy
    ncbi_tax_diff_parser = subparsers.add_parser('ncbi_tax_diff',
                                                 formatter_class=CustomHelpFormatter,
                                                 description='Establish changes in NCBI taxonomy that may impact GTDB taxonomy.')
    ncbi_tax_diff_parser.add_argument('prev_ncbi_taxonomy', help='NCBI taxonomy for previous GTDB release')
    ncbi_tax_diff_parser.add_argument('cur_ncbi_taxonomy', help='NCBI taxonomy for current GTDB release')
    ncbi_tax_diff_parser.add_argument('gtdb_taxonomy', help='GTDB taxonomy for current release')
    ncbi_tax_diff_parser.add_argument('output_dir', help="output directory")
    ncbi_tax_diff_parser.add_argument('--silent', help="suppress output", action='store_true')

    # verify generic species names
    check_generic_parser = subparsers.add_parser('check_generic',
                                                 formatter_class=CustomHelpFormatter,
                                                 description='Verify that generic name of species is valid')
    check_generic_parser.add_argument('input_taxonomy', help='input taxonomy file')
    check_generic_parser.add_argument('gtdb_metadata_file', help='file specifying GTDB metadata (TSV)')
    check_generic_parser.add_argument('sp_classification_ledger',
                                      help='file indicating desired species names for specific genomes')
    check_generic_parser.add_argument('genus_ledger', help='file indicating desired genus names for specific genomes')
    check_generic_parser.add_argument('gtdb_synonym_file', help='file specifying GTDB declared synonyms')
    check_generic_parser.add_argument('user_genome_id_table',
                                      help='table specifying mapping between GTDB user, UBA, and GenBank IDs (TSV)')
    check_generic_parser.add_argument('output_dir', help="output directory")
    check_generic_parser.add_argument('--silent', help="suppress output", action='store_true')

    # verify specific species names
    check_specific_parser = subparsers.add_parser('check_specific',
                                                  formatter_class=CustomHelpFormatter,
                                                  description='Verify that specific name of species is valid')
    check_specific_parser.add_argument('input_taxonomy', help='input taxonomy file')
    check_specific_parser.add_argument('gtdb_metadata_file', help='file specifying GTDB metadata (TSV)')
    check_specific_parser.add_argument('sp_classification_ledger',
                                       help='file indicating desired species names for specific genomes')
    check_specific_parser.add_argument('gtdb_synonym_file', help='file specifying GTDB declared synonyms')
    check_specific_parser.add_argument('user_genome_id_table',
                                       help='table specifying mapping between GTDB user, UBA, and GenBank IDs (TSV)')
    check_specific_parser.add_argument('output_dir', help="output directory")
    check_specific_parser.add_argument('--silent', help="suppress output", action='store_true')

    # check species clusters
    sp_clusters_parser = subparsers.add_parser('species_clusters',
                                               formatter_class=CustomHelpFormatter,
                                               description='Verify classification of genomes assigned to the same species cluster.')
    sp_clusters_parser.add_argument('input_taxonomy', help='input taxonomy file')
    sp_clusters_parser.add_argument('gtdb_metadata_file', help='file specifying GTDB metadata (TSV)')
    sp_clusters_parser.add_argument('output_dir', help="output directory")
    sp_clusters_parser.add_argument('--silent', help="suppress output", action='store_true')

    # check type strains
    type_strains_parser = subparsers.add_parser('type_strains',
                                                formatter_class=CustomHelpFormatter,
                                                description='Compare GTDB to type strain of species designations at NCBI, LPSN, DSMZ, and/or StrainInfo.')
    type_strains_parser.add_argument('input_taxonomy', help='input taxonomy file')
    type_strains_parser.add_argument('gtdb_metadata_file', help='file specifying GTDB metadata (TSV)')
    type_strains_parser.add_argument('sp_classification_ledger',
                                     help='file indicating desired species names for specific genomes')
    type_strains_parser.add_argument('gtdb_named_type_genomes',
                                     help='file explicitly indicating type genomes for named species (gtdb_type_genomes_final.tsv from select_type_genomes)')
    type_strains_parser.add_argument('gtdb_synonym_file', help='file specifying GTDB declared synonyms')
    type_strains_parser.add_argument('output_dir', help='output directory')
    type_strains_parser.add_argument('--show_synonyms', help="show modified type material resulting from GTDB synonyms",
                                     action='store_true')
    type_strains_parser.add_argument('--prefix', help="prefix for all output files", default='gvtk')
    type_strains_parser.add_argument('--silent', help="suppress output", action='store_true')

    # check type species
    type_species_parser = subparsers.add_parser('type_species',
                                                formatter_class=CustomHelpFormatter,
                                                description='Compare GTDB to type species of genus designations at NCBI, LPSN, DSMZ, and/or StrainInfo.')
    type_species_parser.add_argument('input_taxonomy', help='input taxonomy file')
    type_species_parser.add_argument('gtdb_metadata_file', help='file specifying GTDB metadata (TSV)')
    type_species_parser.add_argument('gtdb_synonym_file', help='file specifying GTDB declared synonyms')
    type_species_parser.add_argument('sp_classification_ledger',
                                     help='file indicating desired species names for specific genomes')
    type_species_parser.add_argument('genus_classification_ledger',
                                     help='file indicating desired genus names for specific genomes')
    type_species_parser.add_argument('output_dir', help='output directory')
    type_species_parser.add_argument('--show_synonyms', help="show modified type material resulting from GTDB synonyms",
                                     action='store_true')
    type_species_parser.add_argument('--prefix', help="prefix for all output files", default='gvtk')
    type_species_parser.add_argument('--silent', help="suppress output", action='store_true')

    # check type species
    backfill_parser = subparsers.add_parser('backfill',
                                            formatter_class=CustomHelpFormatter,
                                            description='Fill in missing rank information.')
    backfill_parser.add_argument('input_taxonomy', help='input taxonomy file to backfill')
    backfill_parser.add_argument('prev_taxonomy', help='taxonomy file for previous GTDB release')
    backfill_parser.add_argument('gtdb_metadata_file', help='file specifying GTDB metadata (TSV)')
    backfill_parser.add_argument('gtdb_named_type_genomes',
                                 help='file explicitly indicating type genomes for named species (gtdb_type_genomes_final.tsv from select_type_genomes)')
    backfill_parser.add_argument('gtdb_synonym_file', help='file specifying GTDB declared synonyms')
    backfill_parser.add_argument('sp_classification_ledger',
                                 help='file indicating desired species names for specific genomes')
    backfill_parser.add_argument('sp_placeholder_ledger',
                                 help='file indicating desired species placeholder names for specific genomes')
    backfill_parser.add_argument('genus_classification_ledger',
                                 help='file indicating desired genus names for specific genomes')
    backfill_parser.add_argument('user_genome_id_table',
                                 help='table specifying mapping between GTDB user, UBA, and GenBank IDs (TSV)')
    backfill_parser.add_argument('output_dir', help='output directory')
    backfill_parser.add_argument('--curation_tree_file', help='tree to modify for curating backfilling')
    backfill_parser.add_argument('--sp_cluster_file',
                                 help="file indicating species cluster to use instead of GTDB metadata")
    backfill_parser.add_argument('--prefix', help="prefix for all output files", default='gvtk')
    backfill_parser.add_argument('--silent', help="suppress output", action='store_true')

    # compare NCBI and GTDB species names
    ncbi_species_parser = subparsers.add_parser('ncbi_species',
                                                formatter_class=CustomHelpFormatter,
                                                description='Report differences between GTDB and NCBI species names.')
    ncbi_species_parser.add_argument('input_taxonomy', help='input taxonomy file')
    ncbi_species_parser.add_argument('gtdb_metadata_file', help='file specifying GTDB metadata (TSV)')
    ncbi_species_parser.add_argument('output_dir', help='output directory')
    ncbi_species_parser.add_argument('--silent', help="suppress output", action='store_true')

    # tabulate NCBI species in each GTDB-defined cluster
    gtdb_cluster_ncbi_parser = subparsers.add_parser('gtdb_cluster_ncbi',
                                                     formatter_class=CustomHelpFormatter,
                                                     description='Report NCBI species within each GTDB-defined cluster.')
    gtdb_cluster_ncbi_parser.add_argument('input_taxonomy', help='input taxonomy file')
    gtdb_cluster_ncbi_parser.add_argument('gtdb_metadata_file', help='file specifying GTDB metadata (TSV)')
    gtdb_cluster_ncbi_parser.add_argument('output_dir', help='output directory')
    gtdb_cluster_ncbi_parser.add_argument('--silent', help="suppress output", action='store_true')

    # check genome distribution changes between two GTDB releases
    check_change_parser = subparsers.add_parser('check_change',
                                                formatter_class=CustomHelpFormatter,
                                                description='Check genome distribution changes between two GTDB releases.')
    check_change_parser.add_argument('input_taxonomy1', help='current taxonomy file')
    check_change_parser.add_argument('input_taxonomy2', help='previous taxonomy file')
    check_change_parser.add_argument('output_dir', help='output directory')
    check_change_parser.add_argument('--silent', help='suppress output', action='store_true')

    # add a zero branch length sister node to each current leaf node
    add_dummy_parser = subparsers.add_parser('add_dummy',
                                             formatter_class=CustomHelpFormatter,
                                             description='Add a zero branch length sister node to each current leaf node.')
    add_dummy_parser.add_argument('input_tree', help='input tree file')
    add_dummy_parser.add_argument('--taxonomy_file', help='add dummy nodes to taxonomy file')
    add_dummy_parser.add_argument('--silent', help='suppress output', action='store_true')

    # remove dummy nodes from curation tree
    remove_dummy_parser = subparsers.add_parser('remove_dummy',
                                                formatter_class=CustomHelpFormatter,
                                                description='Remove dummy nodes from curation tree.')
    remove_dummy_parser.add_argument('input_tree', help='input tree file')
    remove_dummy_parser.add_argument('output_tree', help='output tree file')
    remove_dummy_parser.add_argument('--silent', help='suppress output', action='store_true')

    # get and check options
    args = None
    if len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv == '--help':
        print_help()
        sys.exit(0)
    else:
        args = parser.parse_args()

    try:
        logger_setup(args.output_dir, args.silent)
    except:
        logger_setup(None, args.silent)

    # do what we came here to do
    try:
        parser = OptionsParser()
        if False:
            # import pstats
            # p = pstats.Stats('prof')
            # p.sort_stats('cumulative').print_stats(10)
            # p.sort_stats('time').print_stats(10)
            import cProfile

            cProfile.run('parser.parse_options(args)', 'prof')
        elif False:
            import pdb

            pdb.run(parser.parse_options(args))
        else:
            parser.parse_options(args)
    except SystemExit:
        print("\n  Controlled exit resulting from an unrecoverable error or warning.")
    except:
        print("\nUnexpected error:", sys.exc_info()[0])
        raise


if __name__ == '__main__':
    main()
