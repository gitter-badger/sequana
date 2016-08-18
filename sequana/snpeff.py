# -*- coding: utf-8 -*-
#
#  This file is part of Sequana software
#
#  Copyright (c) 2016 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#      Dimitri Desvillechabrol <dimitri.desvillechabrol@pasteur.fr>, 
#          <d.desvillechabrol@gmail.com>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
""" Tools to launch snpEff."""

import re
import sys
import os
import shutil

import subprocess as sp
from collections import OrderedDict

from sequana.resources import snpeff
from sequana import FastA


class SnpEff(object):
    """ Python wrapper to launch snpEff.

    """
    extension = {"-genbank": ".gbk", "-gff3": ".gff", "-gtf22": ".gtf"}
    def __init__(self, reference, file_format=None, stdout=None, stderr=None):
        """

        :param vcf_filename: the input vcf file.
        :param reference: annotation reference.
        :param file_format: format of your file. ('-genbank'/'-gff3'/'-gtf22')
        """
        self.reference = reference
        self.ref_name = reference.split("/")[-1]
        # Check if snpEff.config is present
        if not os.path.exists("snpEff.config"):
            self._get_snpeff_config()
        if not file_format:
            self._check_format()
        # Check if reference is a file
        if os.path.exists(reference):
            if not os.path.exists("data" + os.sep + self.ref_name + os.sep +
                        "snpEffectPredictor.bin"):
                # Build snpEff predictor
                self._add_custom_db(stdout, stderr)
        # Check if reference is present in snpEff database
        elif self._check_database(self.ref_name):
            if not os.path.exists("data" + os.sep + self.ref_name):
                # Download file
                snpeff_dl = sp.Popen(["snpEff", "download", self.ref_name])
                snpeff_dl.wait()
        # If reference is nowhere
        else:
            print("The file " + self.ref_name + " is not present in the "
                  "directory.\n")
            print("And your reference is not present in the database of "
                  "sequana. If you are sure that the reference is present in "
                  "the last update of the snpEff database. Please, import your "
                  "snpEff.config.\n")

    def _check_format(self):
        # set regex for gff and gtf files
        self.regex = re.compile("^([^\s#]+)[ \t\v]")
        with open(self.reference, "r") as fp:
            first_line = fp.readline()
            if first_line.startswith('LOCUS'):
                self.file_format = "-genbank"
                # set regex for genbank file
                self.regex = re.compile("^LOCUS\s+([^\s]+)")
            elif re.search('##gff-version +3', first_line):
                self.file_format = "-gff3"
            elif first_line.startswith('#!'):
                self.file_format = "-gtf22"
            else:
                print("The format can not be determined, please relaunch " 
                      "the script with the file_format argument")
                sys.exit(1)

    def _check_database(self, reference):
        proc_db = sp.Popen(["snpEff", "databases"], stdout=sp.PIPE)
        snpeff_db = {line.split()[0] for line in proc_db.stdout}
        if reference.encode("utf-8") in snpeff_db:
            return True
        return False
    
    def _get_snpeff_config(self):
        from sequana import sequana_data
        CONFIG = sequana_data("snpEff.config.gz", "snpeff")
        shutil.copyfile(CONFIG, "./snpEff.config.gz")
        gunzip_proc = sp.Popen(["gunzip", "snpEff.config.gz"])
        gunzip_proc.wait()
        
    def _add_custom_db(self, stdout=None, stderr=None):
        """ Add your custom file in the local snpEff database.

        """
        # create directory and copy annotation file
        genome_dir = "data" + os.sep + self.ref_name + os.sep
        try:
            os.makedirs(genome_dir)
        except FileExistsError:
            pass
        shutil.copyfile(self.reference, genome_dir + "genes" + 
                SnpEff.extension[self.file_format])

        # add new annotation file in config file
        with open("snpEff.config", "a") as fp:
            fp.write(self.ref_name + ".genome : " + self.ref_name)
        
        try:
            with open(stdout, "wb") as out, open(stderr, "wb") as err:
                snp_build = sp.Popen(["snpEff", "build", self.file_format,
                    self.ref_name], stderr=err, stdout=out)
        except TypeError:
            snp_build = sp.Popen(["snpEff", "build", self.file_format, 
                self.ref_name], stderr=None, stdout=None)
        snp_build.wait()
        rc = snp_build.returncode
        if rc != 0:
            print("snpEff build return a non-zero code")
            sys.exit(rc)

    def launch_snpeff(self, vcf_filename, output, stderr="annot.err",
            options=""):
        """ Launch snpEff
        
        """
        args_ann = ["snpEff", "-formatEff", options, self.ref_name, 
                vcf_filename]
        with open(output, "wb") as fp:
            proc_ann = sp.Popen(args_ann, stdout=fp)
            proc_ann.wait()

    def _get_seq_ids(self):
        # genbank case
        if self.file_format == "-genbank":
            with open(self.reference, "r") as fp:
                seq = [self.regex.search(line).group(1) for line in fp 
                        if self.regex.search(line)]
            return seq
        # gff/gtf case
        else:
            with open(self.reference, "r") as fp:
                seq = [self.regex.seach(line).group(1) for line in fp 
                        if self.regex.search(line)]
            return list(OrderedDict.fromkeys(seq))

    def add_locus_in_fasta(self, fasta, output_file):
        """ Add locus of annotation file in description line of fasta file.

        :param str fasta: input fasta file where you want to add locus.
        :param str output_file: output file.
        
        It returns file name that contains locus in sequences ids.
        """
        fasta_record = FastA(fasta)
        ids_list = self._get_seq_ids()

        # check if both files have same number of contigs
        if len(fasta_record) != len(ids_list):
            print("fasta and annotation files don't have the same number of "
                  "contigs.")
            sys.exit(1)

        # check if directory exist
        output_dir = os.path.dirname(output_file)
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        except FileNotFoundError:
            pass

        if fasta_record.names[0] == ids_list[0]:
            print("Files have same sequence id.")
            os.symlink(fasta, output_file)
            return

        with open(output_file, "w") as fp:
            # write fasta with seqid of annotation file
            for n in range(len(fasta_record)):
                seq_id = ">{0} {1}\n".format(ids_list[n], fasta_record.names[n])
                seq = fasta_record.sequences[n]
                sequence = "\n".join([seq[i:min(i+80, len(seq))]
                    for i in range(0, len(seq), 80)]) + "\n"
                contigs = seq_id + sequence
                fp.write(contigs)


def download_fasta_and_genbank(identifier, tag):
    """

    :param identifier: valid identifier to retrieve from NCBI (genbank) and 
        ENA (fasta)
    :param tag: name of the filename for the genbank and fasta files.
    """
    from bioservices import EUtils
    eu = EUtils()
    data = eu.EFetch(db="nuccore",id="K01711.1", rettype="gbwithparts",
        retmode="text")
    with open("%s.gbk" %  tag, "w") as fout:
        fout.write(data.decode())

    from bioservices import ENA
    ena = ENA()
    data = ena.get_data('K01711', 'fasta')
    with open("%s.fa" % tag, "w") as fout:
        fout.write(data.decode())


