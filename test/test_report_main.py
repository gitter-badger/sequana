from sequana.reporting.report_main import SequanaReport
from sequana.reporting.report_main import BaseReport    


def test_report_base():
    br = BaseReport("main/index.html")
    try:
        br.parse()
        assert False
    except:
        assert True

def test_report():

    from sequana import sequana_data
    stats = sequana_data("test_snakemake_stats.txt", "testing")

    from sequana import Module
    module = Module('phix_removal')
    

    r = SequanaReport(snakefile=module.snakefile, configfile=module.config,
        stats=stats)
    r.create_report()
