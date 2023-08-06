#!/usr/bin/env python3

# This is the main ruffus pipeline for ERVsearch.

from ruffus import follows, split, transform, mkdir, formatter, originate
from ruffus import collate, regex, subdivide, merge
from ruffus.combinatorics import product

import os
import pandas as pd
import numpy as np
import ruffus.cmdline as cmdline
import logging
import subprocess
import configparser
import pathlib
import math
import shutil
try:
    import ERVsearch.HelperFunctions as HelperFunctions
    import ERVsearch.Fasta as Fasta
    import ERVsearch.Bed as Bed
    import ERVsearch.Exonerate as Exonerate
    import ERVsearch.ORFs as ORFs
    import ERVsearch.Trees as Trees
    import ERVsearch.Summary as Summary
    import ERVsearch.Regions as Regions
    import ERVsearch.Errors as Errors
except ImportError:
    import HelperFunctions
    import Fasta
    import Bed
    import Exonerate
    import ORFs
    import Trees
    import Summary
    import Regions
    import Errors


parser = cmdline.get_argparse(description='ERVsearch pipeline to identify endogenous retrovirus like regions in a set of sequences')
options = parser.parse_args()

# Setup to read the ini config file
PARAMS = configparser.ConfigParser()

# Check the ini config file exists
if not os.path.exists("pipeline.ini"):
    Errors.raiseError(Errors.NoIniError)

# Read the parameters from the ini config file
PARAMS.read("pipeline.ini")

# Read the output file stem for the log file
outstem = PARAMS['output']['outfile_stem']

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Name the log file outstem_log.txt
logfile = "%s_log.txt" % outstem

handler = logging.FileHandler(logfile)
# Log from INFO level up (INFO, WARN and ERROR but not DEBUG)
handler.setLevel(logging.INFO)

# Output the time, level and message
formats = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formats)
log.addHandler(handler)

# Setup custom gene databases
genes = []
PARAMS['gene'] = {}

PARAMS['paths']['path_to_ervsearch'] = os.path.split(
    HelperFunctions.__file__)[0]
# The default is to use /ERV_db/gag.fasta /ERV_db/pol.fasta and
# /ERV_db/env.fasta in the pipeline directory but the user can
# also provide their own FASTA files.

usecustom = PARAMS['database']['use_custom_db'] == "True"

for gene in ['gag', 'pol', 'env']:
    if PARAMS['database'][gene] != "None" or not usecustom:
        if usecustom:
            # read the database path from the ini file if needed
            genedb = PARAMS['database'][gene]
        else:
            # otherwise use the default database
            genedb = "%s/ERV_db/%s.fasta" % (
                PARAMS['paths']['path_to_ERVsearch'], gene)
        if not os.path.exists(genedb):
            # if there's a custom database specified, check the file exists
            Errors.raiseError(Errors.DatabaseNotFoundError, genedb, log=log)

        # add this info to the parameter dictionary
        PARAMS['gene'][gene] = genedb
        # keep track of which genes have databases
        genes.append(gene)

# Write the parameters to file
PARAMS.write(open("%s_parameters.txt" % outstem, "w"))

# Store the plot format (as this is used in the ruffus calls)
plot_format = PARAMS['plots']['format']

# Set up the output files for the summariseScreen function (because there
# are lots)
screen_output = Summary.allScreenOutfiles(plot_format)
screen_output.append(["screen_results.dir/results.tsv",
                      "screen_results.dir/by_length.%s" % plot_format,
                      "screen_results.dir/by_genus.%s" % plot_format,
                      "screen_results.dir/by_group.%s" % plot_format,
                      "screen_results.dir/by_gene.%s" % plot_format])


@originate("init.txt")
def initiate(outfile):
    '''
    Initialises the pipeline and checks that the required parameters
    in the pipeline.ini are set and valid and that the required software
    is in your $PATH.

    Checks that:
    * The input genome file exists.
    * The correct path to ERVsearch is provided.
    * samtools, bedtools, FastTree and mafft are in the $PATH
    * The correct paths to usearch and exonerate are provided.

    `init.txt` is a placeholder to show that this step has been completed.
    '''
    HelperFunctions.quickCheck(PARAMS, log)

    # This is just a placeholder to tell ruffus that this function ran.
    out = open(outfile, "w")
    out.write("Passed initial checks")
    out.close()


@follows(initiate)
@follows(mkdir("host_chromosomes.dir"))
@split(PARAMS['genome']['file'], r"host_chromosomes.dir/*.fasta")
def genomeToChroms(infile, outfiles):
    '''
    Splits the host genome provided by the user into FASTA files of a suitable
    size to run Exonerate efficiently.

    If `genomesplits_split` in the pipeline.ini is False, the genome is split
    into one fasta file for each sequence - each chromosome, scaffold or
    contig.

    If `genomesplits_split` in the pipeline.ini is True, the genome is split
    into the number of batches specified by the `genomesplits_splitn`
    parameter, unless the total number of sequences in the input file is
    less than this number.

    The pipeline will fail if the number of sequences which would result
    from the genomesplits settings would result in >500 Exonerate runs,
    however it is possible to force the pipeline to run despite this by
    setting `genomesplits_force` to True.

    If the file keep_chroms.txt exists in the working directory only
    chromosomes listed in this file will be kept.

    An unzipped copy of zipped and gzipped fasta files will be created
    or a link to the file if it is already unzipped. this will be named
    `genome.fa` and be in the working directory.

    This function generates a series of fasta files which are stored in
    the host_chromosomes.dir directory.

    Input Files
    -----------
    *genome_file*
    `keep_chroms.txt`

    Output Files
    ------------
    `host_chromosomes.dir/*fasta`

    Parameters
    ----------
    [genome] file
    [genomesplits] split
    [genomesplits] split_n
    [genomesplits] force
    '''
    # unzip the file if needed
    Fasta.unZip(infile, log)

    # index with samtools faidx
    Fasta.indexFasta("genome.fa", log)

    # count the chromosomes (or sequences)
    nchroms = Fasta.countFasta("genome.fa", log)

    # how many files should the genome be split into
    nsplits = int(PARAMS['genomesplits']['split_n'])

    # if keep_chroms.txt exists only keep chromosomes in this file
    keepchroms = Fasta.readKeepChroms(log)
    if len(keepchroms) != 0:
        nchroms = len(keepchroms)

    # decide how many chromsomes (or sequences) need to go in each output
    # file

    if PARAMS['genomesplits']['split'] == "True" and nsplits < nchroms:
        # if the genome_splits_split parameter is set and there are less splits
        # specified than the total number of chromosomes, the number per
        # file is the number of chromsomes / number of splits
        n_per_split = math.ceil(nchroms / nsplits)
    else:
        # otherwise make one output file per chromosome
        nsplits = nchroms
        n_per_split = 1

    # Exonerate will run once per gene for each split file
    nruns = nsplits * len(genes)

    # Raise an error if Exonerate will run more than 500 time, unless the
    # user specifies genomesplits_force
    if nruns > 500 and PARAMS['genomesplits']['force'] == "True":
        Errors.raiseError(Errors.TooManyRunsWarn, nsplits, nruns, log=log)
    elif nruns > 500:
        Errors.raiseError(Errors.TooManyRunsError, nsplits, nruns, log=log)

    log.info("%s chromosomes will be written per file" % n_per_split)

    # Split the file and write the output to the host_chromosomes.dir directory
    Fasta.splitChroms("genome.fa", log, n=n_per_split)


@follows(mkdir("gene_databases.dir"))
@originate(["gene_databases.dir/%s.fasta" % gene
            for gene in PARAMS['gene'].keys()])
def prepDBS(outfile):
    '''
    Retrieves the gag, pol and env amino acid sequence database fasta files
    and puts a copy of each gene_databases.dir directory.

    If custom databases are used they are retrieved and named as gag.fasta,
    pol.fasta, env.fasta so the path doesn't need to be changed every time.

    Input_Files
    -----------
    None
    Output_Files
    ------------
    gene_databases.dir/GENE.fasta

    Parameters
    ----------
    [database] use_custom_db
    [database] gag
    [database] pol
    [database] env
    '''
    # check which gene it is
    gene = os.path.basename(outfile).split(".")[0]

    # find the appropriate file
    genedb = PARAMS['gene'][gene]

    # make a local copy
    statement = ['cp',
                 genedb,
                 "gene_databases.dir/%s.fasta" % gene]
    log.info("Making a copy of database %s: %s" % (genedb,
                                                   " ".join(statement)))
    subprocess.run(statement)
    Fasta.indexFasta(outfile, log)


@follows(mkdir("raw_exonerate_output.dir"))
@follows(mkdir("clean_exonerate_output.dir"))
@follows(genomeToChroms)
@product(genomeToChroms, formatter(),
         prepDBS,
         formatter(),
         r'raw_exonerate_output.dir/{basename[1][0]}_{basename[0][0]}.tsv')
def runExonerate(infiles, outfile):
    '''
    Runs the `protein2dna` algorithm in the Exonerate software package with
    the host chromosomes (or other regions) in `host_chromosomes.dir` as
    target sequences and the FASTA files from prepDBs as the query sequences.

    The raw output of Exonerate is stored in the raw_exonerate_output.dir
    directory, one file is created for each combination of query and target
    sequences.

    This step is carried out with low stringency as results are later filtered
    using UBLAST and Exonerate.

    Input_Files
    -----------
    gene_databases.dir/GENE.fasta
    host_chromosomes.dir/*fasta

    Output_Files
    ------------
    raw_exonerate_output.dir/GENE_*.tsv

    Parameters
    ----------
    [paths] path_to_exonerate
    '''

    log.info("Running Exonerate on %s vs %s" % (infiles[0], infiles[1]))

    Exonerate.runExonerate(infiles[1], infiles[0],
                           outfile, log,
                           PARAMS['paths']['path_to_exonerate'])


@transform(runExonerate, regex("raw_exonerate_output.dir/(.*).tsv"),
           [r'clean_exonerate_output.dir/\1_unfiltered.tsv',
            r'clean_exonerate_output.dir/\1_filtered.tsv',
            r'clean_exonerate_output.dir/\1.bed'])
def cleanExonerate(infile, outfiles):
    '''
    Filters and cleans up the Exonerate output.
    * Converts the raw Exonerate output files into dataframes -
      GENE_unfiltered.tsv
    * Filters out any regions containing introns (as defined by Exonerate)
    * Filters out regions less than `exonerate_min_hit_length` on the host
      sequence (in nucleotides).
    * Outputs the filtered regions to GENE_filtered.tsv
    * Converts this to bed format and outputs this to GENE.bed

    Input_Files
    -----------
    raw_exonerate_output.dir/GENE_*.tsv

    Output_Files
    ------------
    clean_exonerate_output.dir/GENE_*_unfiltered.tsv
    clean_exonerate_output.dir/GENE_*_filtered.tsv
    clean_exonerate_output.dir/GENE_*.bed

    Parameters
    ----------
    [exonerate] min_hit_length

    '''
    min_hit_length = int(PARAMS['exonerate']['min_hit_length'])
    Exonerate.filterExonerate(infile, outfiles, min_hit_length, log)


@follows(mkdir("gene_bed_files.dir"))
@collate(cleanExonerate,
         regex("clean_exonerate_output.dir/([a-z]+)_(.*)_unfiltered.tsv"),
         [r"gene_bed_files.dir/\1_all.bed",
          r"gene_bed_files.dir/\1_merged.bed"])
def mergeOverlaps(infiles, outfiles):
    '''
    Merges the output bed files for individual sections of the input genome
    into a single bed file.

    Overlapping regions or very close together regions of the genome detected
    by Exonerate with similarity to the same retroviral gene are then merged
    into single regions.  This is performed using bedtools merge
    https://bedtools.readthedocs.io/en/latest/content/tools/merge.html)
    on the bed files output by cleanExonerate.

    If there is a gap of less than `exonerate_overlap` between the regions
    they will be merged.

    Input Files
    -----------
    clean_exonerate_output.dir/GENE_*.bed

    Output_Files
    ------------
    gene_bed_files.dir/GENE_all.bed
    gene_bed_files.dir/GENE_merged.bed

    Parameters
    ----------
    [exonerate] overlap
    '''
    log.info("Generating combined bed file %s" % outfiles[0])
    beds = [inf[2] for inf in infiles]
    # combine the bed files into one file
    combined = Bed.combineBeds(beds)

    # sometimes no regions are identified - stops the pipeline failing
    if combined is not None:
        log.info("%i records identified in combined bed file %s" % (
            len(combined), outfiles[0]))
        combined.to_csv(outfiles[0], sep="\t", index=None, header=None)

        # merge close and overlapping regions
        merged = Bed.mergeBeds(outfiles[0],
                               PARAMS['exonerate']['overlap'],
                               log)

        # write this to file
        if merged is not None:
            log.info("Writing merged bed file %s with %i lines" % (
                outfiles[1], len(merged)))
            merged.to_csv(outfiles[1], sep="\t", index=None, header=None)
        else:
            log.info("No ERVs identified in %s" % outfiles[1])
            pathlib.Path(outfiles[1]).touch()
    else:
        # if there are no regions, just make placeholders
        log.info("No records identified in combined bed file %s" % outfiles[0])
        pathlib.Path(outfiles[0]).touch()
        pathlib.Path(outfiles[1]).touch()


@follows(mkdir("gene_fasta_files.dir"))
@transform(mergeOverlaps, regex("gene_bed_files.dir/(.*)_all.bed"),
           r'gene_fasta_files.dir/\1_merged.fasta')
def makeFastas(infiles, outfile):
    '''
    Fasta files are generated containing the sequences of the merged regions
    of the genome identified using mergeOverlaps.

    These are extracted from the host chromosomes using bedtools getfasta
    https://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html

    Input Files
    -----------
    gene_bed_files.dir/GENE_merged.bed
    genome.fa

    Output Files
    ------------
    gene_fasta_files.dir/GENE_merged.fasta

    Parameters
    ----------
    None
    '''
    infile = infiles[1]
    # Check the input file isn't empty
    if os.stat(infile).st_size == 0:
        pathlib.Path(outfile).touch()
    else:
        # make the FASTA file
        Bed.getFasta(infile, outfile, log)


@transform(makeFastas, regex("gene_fasta_files.dir/(.*)_merged.fasta"),
           r"gene_fasta_files.dir/\1_merged_renamed.fasta")
def renameFastas(infile, outfile):
    '''
    Renames the sequences in the fasta files of ERV-like regions identified
    with Exonerate so each record has a numbered unique ID (gag1, gag2 etc).
    Also removes ":" from sequence names as this causes problems later.

    Input Files
    -----------
    gene_fasta_files.dir/GENE_merged.fasta

    Output Files
    ------------
    gene_fasta_files.dir/GENE_merged_renamed.fasta

    Parameters
    ----------
    None
    '''
    # Check the input file isn't empty
    if os.stat(infile).st_size == 0:
        pathlib.Path(outfile).touch()
    else:
        out = open(outfile, "w")
        # Convert the FASTA file to a dictionary
        F = Fasta.makeFastaDict(infile)
        log.info("Generating gene IDs for %s" % infile)
        gene = os.path.basename(infile).split("_")[0]
        for i, nam in enumerate(F):
            # increment the ID number for each sequence in the file
            out.write(">%s%s_%s\n%s\n" % (gene, i+1, nam.replace(":", "-"),
                                          F[nam]))
        out.close()


@follows(mkdir("UBLAST_db.dir"))
@transform(prepDBS,
           formatter(),
           r'UBLAST_db.dir/{basename[0]}_db.udb')
def makeUBLASTDb(infile, outfile):
    '''
    USEARCH requires an indexed database of query sequences to run.
    This function generates this database for the three gene amino acid fasta
    files used to screen the genome.

    Input Files
    -----------
    gene_databases.dir/GENE.fasta

    Output Files
    ------------
    UBLAST_db.dir/GENE_db.udb

    Parameters
    ----------
    [paths] path_to_usearch
    '''
    usearch = PARAMS['paths']['path_to_usearch']

    statement = [usearch,
                 '-makeudb_ublast',
                 infile,
                 '-output',
                 outfile,
                 '-quiet']
    log.info("Building usearch database for %s: %s" % (infile,
                                                       " ".join(statement)))
    P = subprocess.run(statement,
                       stderr=subprocess.PIPE)
    if P.returncode != 0:
        log.error(P.stderr)
        Errors.raiseError(Errors.UBLASTDBError, outfile, log=log)


@follows(mkdir("ublast.dir"))
@collate((renameFastas, makeUBLASTDb), regex("(.*).dir/([a-z]+)_(.*)"),
         [r"ublast.dir/\2_UBLAST_alignments.txt",
          r"ublast.dir/\2_UBLAST.tsv",
          r"ublast.dir/\2_filtered_UBLAST.fasta"])
def runUBLASTCheck(infiles, outfiles):
    '''
    ERV regions in the fasta files generated by makeFasta are compared to the
    ERV amino acid database files for a second time, this time using USEARCH
    (https://www.drive5.com/usearch/). Using both of these tools reduces the
    number of false positives.

    This allows sequences with low similarity to known ERVs to be filtered
    out.  Similarity thresholds can be set in the pipeline.ini file
    (`usearch_min_id,` - minimum identity between query and target -
     `usearch_min_hit_length` - minimum length of hit on target sequence -
     and `usearch_min_coverage` - minimum proportion of the query sequence
     the hit should cover).

    The raw output of running UBLAST against the target sequences is saved
    in GENE_UBLAST_alignments.txt (equivalent to the BLAST default output) and
    GENE_UBLAST.tsv (equivalent to the BLAST -outfmt 6 tabular output) this
    is already filtered by passing the appropriate parameters to UBLAST.
    The regions which passed the filtering and are therefore in these
    output files are then output to a FASTA file GENE_filtered_UBLAST.fasta.

    Input Files
    -----------
    UBLAST_db.dir/GENE_db.udb
    gene_fasta_files.dir/GENE_merged.fasta

    Output Files
    ------------
    ublast.dir/GENE_UBLAST_alignments.txt
    ublast.dir/GENE_UBLAST.tsv
    ublast.dir/GENE_filtered_UBLAST.fasta

    Parameters
    ----------
    [paths] path_to_usearch
    [usearch] min_id
    [usearch] min_hit_length
    [usearch] min_coverage
    '''
    db, fasta_in = infiles
    alignments, tab, fasta_out = outfiles

    # Check the input FASTA file is not empty
    if os.stat(fasta_in).st_size == 0:
        pathlib.Path(alignments).touch()
        L = []
    else:
        # minimum hit identity to the query
        min_id = PARAMS['usearch']['min_id'].strip()

        # minimum proportion of the query sequence to be covered by the hit
        min_coverage = PARAMS['usearch']['min_coverage'].strip()

        # minimum hit length in nt
        min_length = PARAMS['usearch']['min_hit_length'].strip()

        # generate the UBLAST command
        statement = [PARAMS['paths']['path_to_usearch'],
                     '-ublast', fasta_in,
                     '-db', db,
                     "-query_cov", min_coverage,
                     "-id", min_id,
                     "-mincols", min_length,
                     '-top_hit_only',
                     '-evalue', "1",
                     '-blast6out', tab,
                     '-alnout', alignments,
                     '-quiet']
        log.info("Running UBLAST check on %s: %s" % (fasta_in,
                                                     " ".join(statement)))
        # Run the statement
        P = subprocess.run(statement, stderr=subprocess.PIPE)
        if P.returncode != 0:
            log.error(P.stderr)
            Errors.raiseError(Errors.SoftwareError, 'usearch', fasta_in)

        # Make a list of the regions which are present in the output
        # table - the regions which met the filtering requirements
        L = set([line.strip().split("\t")[0]
                 for line in open(tab).readlines()])
    # touch output files if nothing is found
    if len(L) == 0:
        pathlib.Path(tab).touch()
        pathlib.Path(fasta_out).touch()
    else:
        # Filter the Fasta file to keep only the regions which passed
        # the filtering step
        Fasta.filterFasta(L, fasta_in, fasta_out, log, split=False)


@follows(mkdir("exonerate_classification.dir"))
@transform(runUBLASTCheck, regex("ublast.dir/(.*)_UBLAST_alignments.txt"),
           [r"exonerate_classification.dir/\1_all_matches_exonerate.tsv",
            r"exonerate_classification.dir/\1_best_matches_exonerate.tsv",
            r"exonerate_classification.dir/\1_refiltered_exonerate.fasta"])
def classifyWithExonerate(infiles, outfiles):
    '''
    Runs the Exonerate ungapped algorithm with each ERV region
    in the fasta files generated by makeFasta as queries and the
    all_ERVs_nt.fasta fasta file as a target, to detect which known
    retrovirus is most similar to each newly identified ERV region. Regions
    which don't meet a minimum score threshold (exonerate_min_score) are
    filtered out.

    all_ERVs_nt.fasta contains nucleic acid sequences for many known
    endogenous and exogenous retroviruses with known classifications.

    First all seqeunces are compared to the database and the raw output is
    saved as exonerate_classification.dir/GENE_all_matches_exonerate.tsv.
    Results need a score greater than exonerate_min_score
    against one of the genes of the same type (gag, pol or env) in the
    database. The highest scoring result which meets these critera for
    each sequence is then identified and output to
    exonerate_classification.dir/GENE_best_matches_exonerate.tsv. The
    sequences which meet these critera are also output to a FASTA file
    exonerate_classification.dir/GENE_refiltered_exonerate.fasta.

    Input Files
    -----------
    ublast.dir/GENE_filtered_UBLAST.fasta
    ERVsearch/ERV_db/all_ERVs_nt.fasta

    Output Files
    ------------
    exonerate_classification.dir/GENE_all_matches_exonerate.tsv
    exonerate_classification.dir/GENE_best_matches_exonerate.tsv
    exonerate_classification.dir/GENE_refiltered_matches_exonerate.fasta

    Parameters
    ----------
    [paths] path_to_exonerate
    [exonerate] min_score
    '''
    gene = os.path.basename(infiles[0]).split("_")[0]
    fasta = infiles[2]

    # Check the input file isn't empty
    if os.stat(fasta).st_size == 0:
        for outfile in outfiles:
            pathlib.Path(outfile).touch()
    else:
        # get the Exonerate parmeters
        exonerate_path = PARAMS['paths']['path_to_exonerate']
        exonerate_minscore = PARAMS['exonerate']['min_score']

        # get the reference file
        reference_ERVs = "%s/ERV_db/all_ERVs_nt.fasta" % PARAMS[
            'paths']['path_to_ERVsearch']

        # Run Exonerate ungapped
        Exonerate.classifyWithExonerate(reference_ERVs,
                                        fasta, outfiles[0],
                                        exonerate_path,
                                        exonerate_minscore,
                                        log)

    # Read the raw Exonerate output into a table
    log.info("Converting raw exonerate output %s to a table" % outfiles[0])
    res = pd.read_csv(outfiles[0],
                      sep="\t", header=None, names=['id', 'match', 'score'])
    log.info("Finding the highest scoring hit for each putative ERV in \
             %s" % outfiles[0])
    # Find the highest scoring hit for each sequence
    # Filter out sequences which don't match the right gene
    res = Exonerate.findBestExonerate(res, gene)
    res.to_csv(outfiles[1], sep="\t", index=None)

    log.info("Generating a FASTA file for the results in %s" % outfiles[1])
    L = list(set(res['id']))

    # Filter the fasta file to keep only the sequences which met the
    # Exonerate criteria
    Fasta.filterFasta(L, fasta, outfiles[2], log, split=False)


@follows(mkdir("ORFs.dir"))
@transform(classifyWithExonerate,
           regex(
               "exonerate_classification.dir/(.*)_all_matches_exonerate.tsv"),
           [r"ORFs.dir/\1_orfs_raw.fasta",
            r"ORFs.dir/\1_orfs_nt.fasta",
            r"ORFs.dir/\1_orfs_aa.fasta"])
def getORFs(infiles, outfiles):
    '''
    Finds the longest open reading frame in each of the ERV regions in the
    filtered output table.

    This analysis is performed using EMBOSS revseq (to reverse complement,
    http://emboss.open-bio.org/rel/dev/apps/revseq.html) and EMBOSS transeq
    (to translate, http://emboss.open-bio.org/rel/dev/apps/transeq.html).

    The sequence is translated in all six frames using the user specified
    translation table. The longest ORF is then identified. ORFs shorter than
    orfs_min_orf_length are filtered out.

    The positions of the ORFs are also convered so that they can be extracted
    directly from the input sequence file, rather than using the
    co-ordinates relative to the original Exonerate regions.

    The raw transeq output, the nucleotide sequences of the ORFs and the
    amino acid sequences of the ORFs are written to the output FASTA files.

    Input Files
    ------------
    exonerate_classification.dir/GENE_refiltered_matches_exonerate.fasta

    Output Files
    ------------
    ORFs.dir/GENE_orfs_raw.fasta
    ORFs.dir/GENE_orfs_nt.fasta
    ORFs.dir/GENE_orfs_aa.fasta

    Parameters
    ----------
    [orfs] translation_table
    [orfs] min_orf_len

    '''
    fasta = infiles[2]
    # check the input is not empty
    if os.stat(fasta).st_size == 0:
        for outfile in outfiles:
            pathlib.Path(outfile).touch()
    else:
        log.info("Looking for ORFs in %s" % fasta)
        # run transeq to translate the sequence in all six frames.
        ORFs.runTranseq(fasta,
                        outfiles[0],
                        PARAMS['orfs']['translation_table'],
                        log)
        # filter and clean the transeq output
        ORFs.filterTranseq(fasta,
                           outfiles[0], outfiles[1], outfiles[2],
                           int(PARAMS['orfs']['min_orf_len']),
                           "genome.fa",
                           PARAMS['orfs']['translation_table'], log)


@follows(mkdir("ublast_orfs.dir"))
@collate((getORFs, makeUBLASTDb),
         regex("(.*).dir/([a-z]+)_(.*)"),
         [r"ublast_orfs.dir/\2_UBLAST_alignments.txt",
          r"ublast_orfs.dir/\2_UBLAST.tsv",
          r"ublast_orfs.dir/\2_filtered_UBLAST_nt.fasta",
          r"ublast_orfs.dir/\2_filtered_UBLAST_aa.fasta"])
def checkORFsUBLAST(infiles, outfiles):
    '''
    ERV ORFs in the fasta files generated by the ORFs function are compared
    to the original ERV amino acid files using UBLAST. This allows any
    remaining sequences with poor similarity to known ERVs to be filtered out.

    This allows ORFs with low similarity to known ERVs to be filtered out.
    Similarity thresholds can be set in the pipeline.ini file
    (`usearch_min_id,` - minimum identity between query and target -
     `usearch_min_hit_length` - minimum length of hit on target sequence -
     and `usearch_min_coverage` - minimum proportion of the query sequence the
     hit should cover).

    The raw output of running UBLAST against the target sequences is saved in
    GENE_UBLAST_alignments.txt (equivalent to the BLAST default output) and
    GENE_UBLAST.tsv (equivalent to the BLAST -outfmt 6 tabular output) this is
    already filtered by passing the appropriate parameters to UBLAST. The
    regions which passed the filtering and are therefore in these output files
    are then output to a FASTA file GENE_filtered_UBLAST.fasta.

    Input Files
    -----------
    ORFs.dir/GENE_orfs_nt.fasta
    UBLAST_dbs.dir/GENE_db.udb

    Output Files
    ------------
    ublast_orfs.dir/GENE_UBLAST_alignments.txt
    ublast_orfs.dir/GENE_UBLAST.tsv
    ublast_orfs.dir/GENE_filtered_UBLAST.fasta

    Parameters
    ----------
    [paths] path_to_usearch
    [usearch] min_id
    [usearch] min_hit_length
    [usearch] min_coverage
    '''
    db = infiles[0]
    fasta_nt, fasta_aa = infiles[1][1:]
    alignments, tab, fasta_out_nt, fasta_out_aa = outfiles
    # check the input file is not empty
    if os.stat(fasta_nt).st_size == 0:
        pathlib.Path(alignments).touch()
        L = []
    else:
        # set the minimum ublast criteria
        # minimum identity between query and target
        min_id = PARAMS['usearch']['min_id'].strip()
        # minimum % of query covered by hit
        min_coverage = PARAMS['usearch']['min_coverage'].strip()
        # minimum hit length in amino acids
        min_length = PARAMS['usearch']['min_hit_length'].strip()

        # generate the UBLAST statement
        statement = [PARAMS['paths']['path_to_usearch'],
                     '-ublast', fasta_nt,
                     '-db', db,
                     "-query_cov", min_coverage,
                     "-id", min_id,
                     "-mincols", min_length,
                     '-top_hit_only',
                     '-evalue', "1",
                     '-blast6out', tab,
                     '-alnout', alignments,
                     '-quiet']
        log.info("Running UBLAST check on %s: %s" % (fasta_nt,
                                                     " ".join(statement)))

        # Run UBLAST
        P = subprocess.run(statement, stderr=subprocess.PIPE)
        if P.returncode != 0:
            log.error(P.stderr)
            Errors.raiseError(Errors.SoftwareError, 'usearch', fasta_nt)
        L = set([line.strip().split("\t")[0]
                 for line in open(tab).readlines()])
    # touch output files if nothing is found
    if len(L) == 0:
        pathlib.Path(tab).touch()
        pathlib.Path(fasta_out_nt).touch()
        pathlib.Path(fasta_out_aa).touch()
    else:
        # Filter the nucleotide fasta to keep only the sequences which
        # passed the filter
        Fasta.filterFasta(L, fasta_nt, fasta_out_nt, log, split=False)
        # Filter the aa fasta to keep only the sequences which passed
        # the filter
        Fasta.filterFasta(L, fasta_aa, fasta_out_aa, log, split=False)


@follows(mkdir("grouped.dir"))
@transform(checkORFsUBLAST,
           regex("ublast_orfs.dir/(.*)_UBLAST_alignments.txt"),
           r"grouped.dir/\1_groups.tsv")
def assignGroups(infiles, outfile):
    '''
    Many of the retroviruses in the input database all_ERVs_nt.fasta have
    been classified into groups based on sequence similarity, prior knowledge
    and phylogenetic clustering.  Some sequences don't fall into any well
    defined group, in these cases they are just assigned to a genus,
    usually based on prior knowledge. The information about these groups
    is stored in the provided file ERVsearch/ERV_db/convert.tsv.

    Each sequence in the filtered fasta file of newly identified ORFs
    is assigned to one of these groups based on the sequence identified
    as the most similar in the classifyWithExonerate step.

    The output table is also  tidied up to include the UBLAST output,
    chromosome, ORF start and end positions, genus and group.

    Input Files
    -----------
    ublast_orfs.dir/GENE_UBLAST.tsv
    ERVsearch/ERV_db/convert.tsv

    Output Files
    ------------
    grouped.dir/GENE_groups.tsv

    Parameters
    ----------
    [paths] path_to_ERVsearch
    '''
    ORF_file = infiles[2]
    # make the input fasta file into a dictionary
    ORF_fasta = Fasta.makeFastaDict(ORF_file, spliton="_")

    # this table has the group information - read it and put it into
    # a dictionary
    convert = pd.read_csv("%s/ERV_db/convert.tsv"
                          % PARAMS['paths']['path_to_ERVsearch'],
                          sep="\t")
    D = dict(zip(convert['id'], convert['match']))

    log.info("Assigning %s to a group" % infiles[2])
    # Read the UBLAST matches - these should already be the best UBLAST
    # match
    match_tab = pd.read_csv(infiles[1], sep="\t", header=None)

    # Just keep the relevant columns
    match_tab = match_tab[[0, 1, 2, 3, 10, 11]]
    match_tab.columns = ['name', 'match', 'perc_identity', 'alignment_length',
                         'evalue', 'bit_score']
    match_tab['ID'] = [x.split("_")[0] for x in match_tab['name']]

    # Split the ORF names to get the ID, start and end positions and strand
    segs = [ORFs.splitNam(nam) for nam in match_tab['name']]
    stab = pd.DataFrame(segs)

    # merge everything into one table
    match_tab = match_tab.merge(stab)

    groups = []
    # Find the group
    for nam in match_tab['match'].values:
        nam_stem = "_".join(nam.split("_")[:-2])
        if nam_stem in D:
            # if the sequence falls into a well defined group, use this group
            group = D[nam_stem]
        else:
            # otherwise just use the gene and genus
            group = "_".join(nam_stem.split("_")[-2:])
        groups.append(group)
    match_tab['group'] = groups
    match_tab['evalue'] = ["%.3e" % e for e in match_tab['evalue']]
    match_tab['genus'] = match_tab['match'].str.split("_").str.get(-4)
    match_tab = match_tab[match_tab['ID'].isin(ORF_fasta)]
    # output the clean table
    match_tab.to_csv(outfile, sep="\t", index=None)


@follows(mkdir("summary_tables.dir"))
@follows(mkdir("summary_plots.dir"))
@follows(mkdir("screen_results.dir"))
@merge((mergeOverlaps, runUBLASTCheck,
        getORFs, checkORFsUBLAST, assignGroups),
       screen_output)
def summariseScreen(infiles, outfiles):
    '''
    Generates a series of summary plots and tables showing the results of
    running the screening functions.

    The major outputs of this function are stored in the screen_results.dir
    directory. Further details of these files are provided in
    the [Main Output Files](introduction.html#main-output-files) section.

    The other files show the output of the intermediate steps.<br>

    **Exonerate Initial**<br>
    * `summary_tables.dir/exonerate_initial_summary.txt`
      Summary of the output of the initial Exonerate screening step. Note that
      these are unfiltered and many will not be true ERVs.
    * `summary_tables.dir/ublast_hits_initial_summary.txt`
      Summary of the results of running UBLAST on the initial Exonerate output.
    * `summary_tables.dir/orfs_initial_summary.txt`
      Summary of the results of the initial ORF identification.
    * `summary_tables.dir/ublast_orfs_initial_summary.txt`
      Summary of the results of running UBLAST on these ORFs.
    * `summary_plots.dir/exonerate_initial_lengths.FMT`
      Histogram showing the lengths of the initial Exonerate regions for each
      gene.
    * `summary_plots.dir/exonerate_initial_scores.FMT`
      Histogram showing the Exonerate score of the initial Exonerate regions
      for each gene.
    * `summary_plots.dir/exonerate_initial_strands.FMT`
      Bar chart showing the number of regions identified on each strand
      in the initial Exonerate screen.
    * `summary_plots.dir/exonerate_initial_by_sequence.FMT`
      Histogram showing the number of ERV-like regions identified on each
      sequence in the reference genome being screened.
    * `summary_plots.dir/exonerate_initial_counts_per_gene.FMT`
      Bar chart showing the number of ERV regions identified per gene in
      the initial Exonerate screen.

    **UBLAST**
    * `summary_plots.dir/ublast_hits_alignment_length.FMT`
      Histogram showing the lengths of the alignments of the UBLAST filtered
      Exonerate regions and the most similar reference ORF, based on the
      UBLAST output.
    * `summary_plots.dir/ublast_hits_perc_similarity.FMT`
      Histogram showing the percentage identity between the UBLAST filtered
      Exonerate regions and the most similar reference ORF, based on the
      UBLAST output.
    * `summary_plots.dir/ublast_hits_perc_similarity.FMT`
      Histogram showing the UBLAST bit score between the UBLAST filtered
      Exonerate regions and the most similar reference ORF, based on the
      UBLAST output.
    * `summary_plots.dir/ublast_hits_by_match.FMT`
      Bar chart showing the number of UBLAST filtered Exonerate regions most
      similar to each reference ORF in the ERVsearch/ERV_db database.
    * `summary_plots.dir/ublast_hits_per_gene.FMT`
      Bar chart showing the number of UBLAST filtered Exonerate regions
      identified per gene.

    **ORFs**<br>
    * `summary_plots.dir/orfs_lengths.FMT`
      Histogram of the lengths of ORFs identified in the ERV regions.
    * `summary_plots.dir/orfs_strands.FMT`
      Bar chart of the strand (positive (+) or negative (-) sense) of the ORFs
      identified in the ERV regions.
    * `summary_plots.dir/orfs_by_gene.FMT`
      Bar chart of the number of ORFs identified for each gene.

    **UBLAST ORFs**
    * `summary_plots.dir/ublast_orfs_alignment_length.FMT`
      Histogram showing the lengths of the alignments of the ERV-like ORFs
      and the most similar reference ORF, based on the UBLAST output.
    * `summary_plots.dir/ublast_orfs_perc_similarity.FMT`
      Histogram showing the percentage identity between the ERV-like ORFs
      and the most similar reference ORF, based on the UBLAST output.
    * `summary_plots.dir/ublast_orfs_bit_score.FMT`
      Histogram showing the UBLAST bit score between the ERV-like ORFs and
      the most similar reference ORF, based on the UBLAST output.
    * `summary_plots.dir/ublast_orfs_by_match.FMT`
      Bar chart showing the number of ERV-like ORFs most similar to each
      reference ORF in the ERVsearch/ERV_db database.
    * `summary_plots.dir/ublast_orfs_per_gene.FMT`
      Bar chart showing the number of ERV-like ORFs identified per gene.

    Input_Files
    -----------
    gene_bed_files.dir/GENE_merged.bed
    ublast.dir/GENE_UBLAST.tsv
    ORFs.dir/GENE_orfs_aa.fasta
    ublast_orfs.dir/GENE_UBLAST.tsv

    Output_Files
    ------------
    `summary_tables.dir/exonerate_initial_summary.txt`<br>
    `summary_tables.dir/ublast_hits_initial_summary.txt`<br>
    `summary_tables.dir/orfs_initial_summary.txt`<br>
    `summary_tables.dir/ublast_orfs_initial_summary.txt`<br>
    `summary_plots.dir/exonerate_initial_lengths.FMT`<br>
    `summary_plots.dir/exonerate_initial_scores.FMT`<br>
    `summary_plots.dir/exonerate_initial_strands.FMT`<br>
    `summary_plots.dir/exonerate_initial_by_sequence.FMT`<br>
    `summary_plots.dir/exonerate_initial_counts_per_gene.FMT`<br>
    `summary_plots.dir/ublast_hits_alignment_length.FMT`<br>
    `summary_plots.dir/ublast_hits_perc_similarity.FMT`<br>
    `summary_plots.dir/ublast_hits_by_match.FMT`<br>
    `summary_plots.dir/ublast_hits_per_gene.FMT`<br>
    `summary_plots.dir/orfs_lengths.FMT`<br>
    `summary_plots.dir/orfs_strands.FMT`<br>
    `summary_plots.dir/orfs_by_gene.FMT`<br>
    `summary_plots.dir/ublast_orfs_alignment_length.FMT`<br>
    `summary_plots.dir/ublast_orfs_perc_similarity.FMT`<br>
    `summary_plots.dir/ublast_orfs_bit_score.FMT`<br>
    `summary_plots.dir/ublast_orfs_by_match.FMT`<br>
    `summary_plots.dir/ublast_orfs_per_gene.FMT`<br>
    `screen_results.dir/results.tsv`<br>
    `screen_results.dir/by_length.FMT`<br>
    `screen_results.dir/by_genus.FMT`<br>
    `screen_results.dir/by_group.FMT`<br>
    `screen_results.dir/by_gene.FMT`<br>

    Parameters
    ----------
    `[plots] dpi`
    `[plots] format`
    `[plots] gag_colour`
    `[plots] pol_colour`
    `[plots] env_colour`
    `[plots] other_colour`
     '''
    funcs = ['gene_bed_files', 'ublast', 'orfs', 'ublast_orfs', "grouped"]
    inD = dict()
    outD = dict()
    j = 0
    for i in np.arange(0, (len(infiles) - 2), 3):
        inD[funcs[j]] = infiles[i: i+3]
        outD[funcs[j]] = outfiles[j]
        j += 1
    Summary.summariseExonerateInitial(inD['gene_bed_files'],
                                      outD['gene_bed_files'],
                                      log, genes,
                                      PARAMS['plots'])
    Summary.summariseUBLAST(inD['ublast'],
                            outD['ublast'], log, genes,
                            PARAMS['plots'])
    Summary.summariseORFs(inD['orfs'],
                          outD['orfs'],
                          log, genes, PARAMS['plots'])
    Summary.summariseUBLAST(inD['ublast_orfs'],
                            outD['ublast_orfs'],
                            log, genes, PARAMS['plots'])
    Summary.summariseGroups(inD['grouped'],
                            outD['grouped'],
                            log, genes, PARAMS['plots'])


@follows(summariseScreen)
def Screen():
    '''
    Helper function to run all screening functions (all functions prior to
    this point).

    Input Files
    -----------
    None

    Output Files
    ------------
    None

    Parameters
    ----------
    None
    '''
    pass


@follows(mkdir("group_fastas.dir"))
@subdivide(assignGroups, regex("grouped.dir/([a-z]+)_groups.tsv"),
           [r"group_fastas.dir/\1_*.fasta",
            r"group_fastas.dir/\1_*_A.fasta"])
def makeGroupFastas(infile, outfiles):
    '''
    Two sets of reference fasta files are available (files are stored in
    `ERVsearch/phylogenies/group_phylogenies` and
    `ERVsearch/phylogenies/summary_phylogenies`)

        * group_phylogenies - groups of closely related ERVs for fine
        classification of sequences
        * summary_phylogenies - groups of most distant ERVs for broad
        classification of sequences

    Sequences have been assigned to groups based on the most similar sequence
    in the provided ERV database, based on the score using the Exonerate
    ungapped algorithm.

    Where the most similar sequence is not part of a a well defined group,
    it has been assigned to a genus.

    Fasta files are generated containing all members of the group from
    the group_phylogenies file (plus an outgroup) where possible and using
    representative sequences from the same genus, using the
    summary_phylogenies file, where only a genus has been assigned, plus
    all the newly identified ERVs in the group. These files are saved
    as GENE_(group_name_)GENUS.fasta.

    The files are aligned using the MAFFT fftns algorithm
    https://mafft.cbrc.jp/alignment/software/manual/manual.html to generate
    the GENE_(group_name_)GENUS_A.fasta aligned output files.

    Input Files
    -----------
    grouped.dir/GENE_groups.tsv
    ublast_orfs.dir/GENE_filtered_UBLAST_nt.fasta
    ERVsearch/phylogenies/group_phylogenies/*fasta
    ERVsearch/phylogenies/summary_phylogenies/*fasta

    Output Files
    ------------
    group_fastas.dir/GENE_(.*)_GENUS.fasta
    group_fastas.dir/GENE_(.*)_GENUS_A.fasta

    Parameters
    ----------
    None
    '''
    # Read the table containing the group information
    grouptable = pd.read_csv(infile, sep="\t")
    gene = os.path.basename(infile).split("_")[0]

    # Read the fasta file of the newly identified ERV-like regions
    fasta = "ublast_orfs.dir/%s_filtered_UBLAST_nt.fasta" % gene
    # Build the FASTA file
    Trees.makeGroupFasta(grouptable, fasta,
                         PARAMS['paths']['path_to_ERVsearch'],
                         log)


@follows(mkdir("group_trees.dir"))
@transform(makeGroupFastas, regex("group_fastas.dir/(.*)_A.fasta"),
           r"group_trees.dir/\1.tre")
def makeGroupTrees(infile, outfile):
    '''
    Builds a phylogenetic tree, using the FastTree2 algorithm
    (http://www.microbesonline.org/fasttree) with the default settings plus
    the GTR algorithm for the aligned group FASTA files generated by the
    makeGroupFastas function.

    Input Files
    -----------
    group_fastas.dir/GENE_(.*_)GENUS_A.fasta

    Output Files
    ------------
    group_trees.dir/GENE_(.*_)GENUS.tre

    Parameters
    ----------
    None
    '''
    Trees.buildTree(infile, outfile, log)


@transform(makeGroupTrees, regex("group_trees.dir/(.*).tre"),
           r"group_trees.dir/\1.%s" % PARAMS['trees']['format'])
def drawGroupTrees(infile, outfile):
    '''
    Generates an image file for each file generated in the makeGroupTrees
    step, using ete3 (http://etetoolkit.org). Newly identified sequences are
    labelled as "~" and shown in a different colour.

    By default, newly identified sequences are shown in the colours specified
    in `plots_gag_colour`, `plots_pol_colour` and `plots_env_colour` -
    to do this then `trees_use_gene_colour` should be set to True in the
    `pipeline.ini`. Alternatively, a fixed colour can be used by setting
    `trees_use_gene_colour` to False and settings `trees_highlightcolour`.
    The text colour of the reference sequences (default black) can be set
    using `trees_maincolour` and the outgroup using `trees_outgroupcolour`.

    The output file DPI can be specified using `trees_dpi` and the format
    (which can be png, svg, pdf or jpg) using `trees_format`.

    Input_Files
    -----------
    group_trees.dir/GENE_(.*_)GENUS.tre

    Output_Files
    ------------
    group_trees.dir/GENE_(.*_)GENUS.FMT (png, svg, pdf or jpg)

    Parameters
    ----------
    [plots] gag_colour
    [plots] pol_colour
    [plots] env_colour
    [trees] use_gene_colour
    [trees] maincolour
    [trees] highlightcolour
    [trees] outgroupcolour
    [trees] dpi
    [trees] format
    '''
    # Establish the colour to highlight the leaf names
    if PARAMS['trees']['use_gene_colour'] == "True":
        hlcolour = PARAMS['plots']['%s_colour' % (os.path.basename(
            infile).split("_")[0])]
    else:
        hlcolour = PARAMS['trees']['highlightcolour']
    log.info("Drawing tree image for %s" % infile)
    # Generate the image
    Trees.drawTree(infile, outfile, PARAMS['trees']['maincolour'],
                   hlcolour,
                   PARAMS['trees']['outgroupcolour'],
                   PARAMS['trees']['dpi'])


@follows(mkdir("summary_fastas.dir"))
@follows(mkdir("group_lists.dir"))
@collate((makeGroupFastas, makeGroupTrees),
         regex("group_[a-z]+.dir/([a-z]+)(_?.*?)_([a-z]+)\.([a-z]+)"),
         [r"summary_fastas.dir/\1_\3.fasta",
          r"summary_fastas.dir/\1_\3_A.fasta"])
def makeSummaryFastas(infiles, outfiles):
    '''
    Based on the group phylogenetic trees generated in makeGroupTrees,
    monophyletic groups of newly idenified ERVs are identified. For each of
    these groups, a single sequence (the longest) is selected as
    representative. The representative sequences are combined with the FASTA
    files in `ERVsearch/phylogenies/summary_phylogenies`, which contain
    representative sequences for each retroviral gene and genus. These are
    extended to include further reference sequences from the same small group
    as the newly identified sequences.

    For example, if one MLV-like pol and one HERVF-like pol was identified
    in the gamma genus, the gamma_pol.fasta summary fasta would contain:
    * The new MLV-like pol sequence
    * The new HERVF-like pol sequence
    * The reference sequences from
     `ERVsearch/phylogenies/group_phylogenies/MLV-like_gamma_pol.fasta` -
     highly related sequences from the MLV-like group
    * The reference sequences from
     `ERVsearch/phylogenies/group_phylogenies/HERVF-like_gamma_pol.fasta` -
     highly related sequences from the HERVF-like group.
    * The reference sequences from
    `ERVsearch/phylogenies/summary_phylogenies/gamma_pol.fasta` -
    a less detailed but more diverse set of gammaretroviral pol ORFs.
    * A epsilonretrovirus outgroup

    This ensures sufficient detail in the groups of interest while avoiding
    excessive detail in groups where nothing new has been identified.

    These FASTA files are saved as GENE_GENUS.fasta

    The files are aligned using the MAFFT fftns algorithm
    https://mafft.cbrc.jp/alignment/software/manual/manual.html to generate
    the GENE_GENUS_A.fasta aligned output files.

    Input Files
    -----------
    group_fastas.dir/GENE_(.*_)GENUS.fasta
    group_trees.dir/GENE_(*_)GENUS.tre
    ERVsearch/phylogenies/summary_phylogenies/GENE_GENUS.fasta
    ERVsearch/phylogenies/group_phylogenies/(.*)_GENUS_GENE.fasta

    Output Files
    ------------
    summary_fastas.dir/GENE_GENUS.fasta
    summary_fastas.dir/GENE_GENUS.tre

    Parameters
    ----------
    [paths] path_to_ERVsearch
    '''
    inf = np.array(infiles)
    fastas = np.sort(inf[np.char.endswith(inf, ".fasta")])
    trees = np.sort(inf[np.char.endswith(inf, ".tre")])
    Trees.makeRepFastas(fastas, trees,
                        PARAMS['paths']['path_to_ERVsearch'],
                        outfiles, log)


@follows(mkdir("summary_trees.dir"))
@transform(makeSummaryFastas,
           regex("summary_fastas.dir/(.*).fasta"),
           r"summary_trees.dir/\1.tre")
def makeSummaryTrees(infiles, outfile):
    '''
    Builds a phylogenetic tree, using the FastTree2 algorithm
    (http://www.microbesonline.org/fasttree) with the default settings plus
    the GTR model, for the aligned group FASTA files generated by the
    makeSummaryFastas function.

    Input Files
    -----------
    summary_fastas.dir/GENE_GENUS_A.fasta

    Output Files
    ------------
    summary_trees.dir/GENE_GENUS.tre

    Parameters
    ----------
    None
    '''
    Trees.buildTree(infiles[1], outfile, log)


@transform(makeSummaryTrees,
           regex("summary_trees.dir/(.*).tre"),
           r"summary_trees.dir/\1.%s" % PARAMS['trees']['format'])
def drawSummaryTrees(infile, outfile):
    if PARAMS['trees']['use_gene_colour'] == "True":
        hlcolour = PARAMS['plots']['%s_colour' % (os.path.basename(
            infile).split("_")[0])]
    else:
        hlcolour = PARAMS['trees']['highlightcolour']
    Trees.drawTree(infile, outfile, PARAMS['trees']['maincolour'],
                   hlcolour,
                   PARAMS['trees']['outgroupcolour'],
                   PARAMS['trees']['dpi'], sizenodes=True)


@follows(mkdir("classify_results.dir"))
@merge((makeSummaryFastas, makeSummaryTrees),
       ['classify_results.dir/results.tsv',
        'classify_results.dir/by_gene_genus.%s' % plot_format])
def summariseClassify(infiles, outfiles):
    '''
    * `exonerate_initial_lengths.png` - histograms of lengths of
      the initial regions identified by Exonerate.
    * `exonerate_initial_by_sequence.png`- histograms of the number of
      sequences identified by exonerate in each input sequence.
    '''
    inD = dict()
    for infile in infiles:
        if isinstance(infile, str):
            direc = infile.split(".dir")[0]
            inD.setdefault(direc, [])
            if not infile.split(".")[-2].endswith("_A"):
                inD[direc].append(infile)
        else:
            for inf in infile:
                direc = inf.split(".dir")[0]
                inD.setdefault(direc, [])
                if not inf.split(".")[-2].endswith("_A"):
                    inD[direc].append(inf)
    Summary.summariseClassify(inD['summary_fastas'], inD['summary_trees'],
                              outfiles, genes, PARAMS['plots'], log)


@follows(drawGroupTrees)
@follows(drawSummaryTrees)
@follows(summariseClassify)
def Classify():
    '''
    Helper function to run all screening functions and classification
    functions (all functions prior to this point).

    Input Files
    -----------
    None

    Output Files
    ------------
    None

    Parameters
    ----------
    None
    '''
    pass


@follows(mkdir("clean_beds.dir"))
@transform(assignGroups, regex("grouped.dir/(.*)_groups.tsv"),
           r"clean_beds.dir/\1.bed")
def makeCleanBeds(infile, outfile):
    '''
    Generates a bed file for each gene which contains the co-ordinates of the
    ORFs which have passed all filtering criteria in the Screen section.

    Input_Files
    -----------
    grouped.dir/GENE_groups.tsv

    Output_Files
    ------------
    clean_beds.dir/GENE.bed

    Parameters
    ----------
    None
    '''
    df = pd.read_csv(infile, sep="\t")
    cols = HelperFunctions.getBedColumns()
    log.info("Generating a clean bed file of filtered ORF positions for %s\
              with %i rows" % (infile, len(df)))
    # subtract one to correct for 0-based vs 1-based systems
    df['start'][df['strand'] == "+"] -= 1
    df = df[cols]
    df.to_csv(outfile, sep="\t", header=None, index=None)


@follows(mkdir("clean_fastas.dir"))
@transform(makeCleanBeds, regex("clean_beds.dir/(.*).bed"),
           r"clean_fastas.dir/\1.fasta")
def makeCleanFastas(infile, outfile):
    '''
    Fasta files are generated containing the sequences of the regions
    listed by makeCleanBeds.

    These are extracted from the host chromosomes using bedtools getfasta
    https://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html

    Input Files
    -----------
    clean_beds.dir/GENE.bed
    genome.fa

    Output Files
    ------------
    clean_fastas.dir/GENE.fasta

    Parameters
    ----------
    None
    '''
    # Check the input file isn't empty
    if os.stat(infile).st_size == 0:
        pathlib.Path(outfile).touch()
    else:
        Bed.getFasta(infile, outfile, log)


@follows(mkdir("ERV_regions.dir"))
@follows(makeCleanFastas)
@merge(makeCleanBeds,
       ["ERV_regions.dir/all_ORFs.bed",
        "ERV_regions.dir/all_regions.bed",
        "ERV_regions.dir/multi_gene_regions.bed",
        "ERV_regions.dir/regions.fasta"])
def findERVRegions(infiles, outfiles):
    '''
    Combines the files containng the ORF regions for the different retroviral
    genes and merges any regions which are within regions_maxdist of each
    other to find larger regions containing multiple genes.
    The `all_ORFs.bed` output file is the concatenated and sorted bed
    files, `all_regions.bed `contains the merged regions with any ORFs
    within regions_maxdist of each other (end to end) combined, plus all
    regions with a single ORF, generated from all_regions.bed using bedtools
    merge (https://bedtools.readthedocs.io/en/latest/content/tools/merge.html).
    The name, strand and score columns are concatenated for merged regions,
    delimited with a ",".
    `multi_gene_regions.bed` contains only the regions which were found to
    contain multiple ORFs, `regions.fasta` is the sequence of these region
    in FASTA format. At this point this includes regions with multiple ORFs
    from the same gene (e.g. two *pol* ORFs).
lt
    Input Files
    -----------
    clean_fastas.dir/*.fasta

    Output Files
    ------------
    ERV_regions.dir/all_ORFs.bed
    ERV_regions.dir/all_regions.bed
    ERV_regions.dir/multi_gene_regions.bed
    ERV_regions.dir/regions.fasta

    Parameters
    ----------
    [regions] maxdist
    '''
    combined = Bed.combineBeds(infiles)
    combined.to_csv(outfiles[0], sep="\t", index=None, header=None)
    merged = Bed.mergeBeds(outfiles[0], overlap=PARAMS['regions']['maxdist'],
                           log=log, mergenames=False)
    merged.to_csv(outfiles[1], sep="\t", index=None, header=None)
    merged = merged[merged[3].str.find(",") != -1]
    merged.to_csv(outfiles[2], sep="\t", index=None, header=None)
    Bed.getFasta(outfiles[2], outfiles[3], log)


@merge(findERVRegions,
       ["ERV_regions.dir/ERV_regions_final.tsv",
        "ERV_regions.dir/ERV_regions_final.bed",
        "ERV_regions.dir/ERV_regions_final.fasta"])
def makeRegionTables(infiles, outfiles):
    '''
    Takes a merged bed file consisting of regions of the genome identified
    as having more than one ERV-like ORF, finds the regions within this file
    which contain more than one different gene (e.g. gag and pol instead of
    two gag ORFs) and outputs a formatted table of information about these
    regions.

    The output table (`ERV_regions_final.tsv`) will usually have 37 columns:
        * name - the final ID of the ERV region - the genes found plus an
          integer
          e.g. gag_pol_12
        * chrom - chromosome
        * start - start position of the ERV region
        * end - end position of the ERV region
        * strand - strand of the ERv region
        * genus - genus of the ERV region, can be multiple genera delimted by
          | if different genes had different genera
        * for each gene screened for (usually gag, pol and env)
              * GENE_name - the names of the ORFs for this gene in this region
              * GENE_ID - the original IDs of the ORFs for this gene in this
                region
              * GENE_start - the start position of this gene in this region
                (genome co-ordinates)
              * GENE_relative_start - the start position of this gene in this
                region (relative to the start of the region)
              * GENE_end - the end position of this gene in this region
                (genome co-ordinates)
              * GENE_relative_end - the end position of this gene in this
                region (relative to the start of the region)
              * GENE_strand - the strand for this gene in this region
              * GENE_match - the closest reference retrovirus to this gene
                in this region
              * GENE_group - the group of the closest reference retrovirus to
                this gene in this region
              * GENE_genus - the genus of the closest reference retrovirus to
                this gene in this region
        * orig_name - the name of the region in the input table
    If not all genes are screened for the table will not have the columns
    for this gene.

    A bed file (ERV_regions_final.bed) is generated with the co-ordinates
    of the identified regions and a FASTA file (ERV_regions_final.fasta)
    containing their sequences.

    Input Files
    -----------
    ERV_regions.dir/multi_gene_regions.bed
    grouped.dir/*_groups.tsv
    genome.fa

    Output Files
    ------------
    ERV_regions.dir/ERV_regions_final.tsv
    ERV_regions.dir/ERV_regions_final.bed
    ERV_regions.dir/ERV_regions_final.fasta

    Parameters
    ----------
    None
    '''
    results = Regions.getRegions(infiles[2], genes,
                                 PARAMS['regions']['maxoverlap'], log)
    results.to_csv(outfiles[0], sep="\t", index=None)
    cols = HelperFunctions.getBedColumns()
    # exclude column 5
    cols = cols[:4] + cols[5:]
    results[cols].to_csv(outfiles[1], sep="\t", index=None, header=None)
    Bed.getFasta(outfiles[1], outfiles[2], log)


@follows(mkdir("ERV_region_plots.dir"))
@split(makeRegionTables, "ERV_region_plots.dir/*%s" % plot_format)
def plotERVRegions(infiles, outfiles):
    '''
    For each region containing ORFs resembling more than one retroviral
    gene, a plot is generated showing how these ORFs are distributed
    on the genome relative to each other.

    Each gene is shown on a different line on the y axis, the x axis is
    chromosome co-ordinates.

    Input_Files
    -----------
    ERV_regions.dir/ERV_regions_final.tsv

    Output_Files
    ------------
    ERV_region_plots.dir/*FMT

    Parameters
    ----------
    [plots] format
    [plots] dpi
    [plots] gag_colour
    [plots] pol_colour
    [plots] env_colour
    '''
    infile = infiles[0]
    tab = pd.read_csv(infile, sep="\t")
    Regions.plotERVRegions(tab, genes, PARAMS['plots'], log)


@follows(mkdir("erv_regions_results.dir"))
@merge(makeRegionTables,
       [r"erv_regions_results.dir/results.tsv",
        r"erv_regions_results.dir/erv_regions.png"])
def summariseERVRegions(infiles, outfiles):
    """
    Combines the results of the ERVregions steps to generate additional
    summary files.

    The `results.tsv` output file is a copy of the output of the
    makeRegionTables functions.

    This will usually have 37 columns:
    * `name` - the final ID of the ERV region - the genes found plus an
      integer  e.g. gag_pol_12
    * `chrom` - chromosome
    * `start` - start position of the ERV region
    * `end` - end position of the ERV region
    * `strand` - strand of the ERv region
    * `genus` - genus of the ERV region, can be multiple genera
      delimted by "|" if different genes had different genera
    * for each gene screened for (usually gag, pol and env)
        * `GENE_name` - the names of the ORFs for this gene in this
           region
        * `GENE_ID` - the original IDs of the ORFs for this gene in this
           region
        * `GENE_start` - the start position of this gene in this region
           (genome co-ordinates)
        * `GENE_relative_start` - the start position of this gene in this
           region (relative to the start of the region)
        * `GENE_end` - the end position of this gene in this region (genome
           co-ordinates)
        * `GENE_relative_end` - the end position of this gene in this region
           (relative to the start of the region)
        * `GENE_strand` - the strand for this gene in this region
        * `GENE_match` - the closest reference retrovirus to this gene in this
           region
        * `GENE_group` - the group of the closest reference retrovirus to this
           gene in this region
        * `GENE_genus` - the genus of the closest reference retrovirus to this
           gene in this region
    * `orig_name` - the name of the region in the input table

    A bar chart - `erv_regions_results.dir/erv_regions.FMT` is also
    generated showing the number of ERV regions found with each combination
    of genes.

    Input Files
    -----------
    ERV_regions.dir/ERV_regions_final.tsv
    Output Files
    ------------
    erv_regions_results.dir/results.tsv
    erv_regions_results.dir/erv_regions.FMT

    Parameters
    ----------
    [plots] other_colour
    """
    shutil.copy(infiles[0], outfiles[0])
    Summary.summariseERVRegions(infiles, outfiles, genes, PARAMS['plots'], log)


@follows(summariseERVRegions)
@follows(plotERVRegions)
def ERVRegions():
    '''
    Helper function to run all screening functions and ERVRegions functions.

    Input_Files
    -----------
    None

    Output_Files
    ------------
    None

    Parameters
    ----------
    None
    '''
    pass


@follows(Screen)
@follows(Classify)
@follows(ERVRegions)
def full():
    """
    Helper function to run all functions.

    Input_Files
    -----------
    None

    Output_Files
    ------------
    None

    Parameters
    ----------
    None
    """
    pass


if __name__ == '__main__':
    cmdline.run(options)
