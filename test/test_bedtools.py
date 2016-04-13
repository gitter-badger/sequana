# Import -----------------------------------------------------------------------

import os
from sequana import bedtools
from easydev import TempFile
from . import data
pathdata = data.__path__[0]

# Test -------------------------------------------------------------------------

def test_genomecov():
    mydata = bedtools.genomecov(pathdata + os.sep + "test.bed")
    mydata.moving_average(n=3)
    mydata.running_median(n=3, circular=True)
    mydata.running_median(n=3, circular=False)
    mydata.coverage_scaling()
    mydata.compute_zscore()
    mydata.get_low_coverage()
    mydata.get_high_coverage()
    mydata.merge_region(mydata.df)
    with TempFile(suffix='.png') as fh:
        mydata.plot_coverage(filename=fh.name)
    with TempFile(suffix='.png') as fh:
        mydata.plot_hist(filename=fh.name)
