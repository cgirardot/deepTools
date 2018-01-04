from nose.tools import assert_equal
import deeptools.estimateReadFiltering as est
import os.path
from os import unlink

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/test_data/"
BAMFILE_FILTER = ROOT + "test_filtering.bam"
CRAMFILE_FILTER = ROOT + "test_filtering.cram"
BEDFILE_FILTER = ROOT + "test_filtering.blacklist.bed"


def test_estimate_read_filtering_minimal():
    """
    Minimal testing
    """
    outfile = '/tmp/test_minimal.txt'
    for fname in [BAMFILE_FILTER, CRAMFILE_FILTER]:
        args = '-b {} -o {}'.format(fname, outfile).split()
        est.main(args)

        _foo = open(outfile, 'r')
        resp = _foo.readlines()
        _foo.close()
        expected = ['Sample\tTotal Reads\tMapped Reads\tAlignments in blacklisted regions\tEstimated mapped reads filtered\tBelow MAPQ\tMissing Flags\tExcluded Flags\tInternally-determined Duplicates\tMarked Duplicates\tSingletons\tWrong strand\n',
                    '{}\t193\t193\t0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\n'.format(os.path.basename(fname))]
        # strip the path from the output
        _ = resp[1].split("\t")
        _[0] = os.path.basename(_[0])
        resp[1] = "\t".join(_)
        assert_equal(resp, expected)
        unlink(outfile)


def test_estimate_read_filtering_params():
    """
    Minimal testing
    """
    outfile = '/tmp/test_params.txt'
    for fname in [BAMFILE_FILTER, CRAMFILE_FILTER]:
        args = '-b {} --minMappingQuality 10 --samFlagExclude 512 --ignoreDuplicates -bl {} -o {}'.format(fname, BEDFILE_FILTER, outfile).split()
        est.main(args)

        _foo = open(outfile, 'r')
        resp = _foo.readlines()
        _foo.close()
        # strip the path from the output
        _ = resp[1].split("\t")
        _[0] = os.path.basename(_[0])
        resp[1] = "\t".join(_)
        expected = ['Sample\tTotal Reads\tMapped Reads\tAlignments in blacklisted regions\tEstimated mapped reads filtered\tBelow MAPQ\tMissing Flags\tExcluded Flags\tInternally-determined Duplicates\tMarked Duplicates\tSingletons\tWrong strand\n',
                    '{}\t193\t193\t7\t176.1\t41.4\t0.0\t186.5\t31.6\t0.0\t0.0\t0.0\n'.format(os.path.basename(fname))]
        assert_equal(resp, expected)
        unlink(outfile)
