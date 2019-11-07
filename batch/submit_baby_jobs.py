from metis.CMSSWTask import CMSSWTask
from metis.CondorTask import CondorTask
from metis.Sample import DirectorySample, DBSSample
from metis.StatsParser import StatsParser
from metis.Optimizer import Optimizer
import time

import numpy as np

def submit(info):
    total_summary = {}

    extra_requirements = "True"
    blacklisted_machines = [
             "cabinet-4-4-29.t2.ucsd.edu",
             "cabinet-7-7-36.t2.ucsd.edu",
             "cabinet-8-8-1.t2.ucsd.edu",
             ]
    if blacklisted_machines:
        extra_requirements = " && ".join(map(lambda x: '(TARGET.Machine != "{0}")'.format(x),blacklisted_machines))

    for reqname,tag,extra_args in info:
        extra_args = ""
        task = CondorTask(
                sample = DirectorySample(
                    location = "/hadoop/cms/store/user/namin/ScoutingCaloMuon/crab_{}/*/*/".format(reqname),
                    dataset = "/ScoutingCaloMuon/Run2018{}/RAW".format(reqname)
                    ),
                output_name = "output.root",
                executable = "executables/scouting_exe.sh",
                tarfile = "package.tar.gz",
                MB_per_output = 4000,
                condor_submit_params = {
                    "sites":"T2_US_UCSD",
                    "classads": [
                        ["metis_extraargs",extra_args],
                        ["JobBatchName",reqname],
                        ],
                    "requirements_line": 'Requirements = ((HAS_SINGULARITY=?=True) && (HAS_CVMFS_cms_cern_ch =?= true) && {extra_requirements})'.format(extra_requirements=extra_requirements),
                    },
                cmssw_version = "CMSSW_10_2_5",
                scram_arch = "slc6_amd64_gcc700",
                tag = tag,
                )

        task.process()
        summary = task.get_task_summary()
        total_summary[task.get_sample().get_datasetname()] = summary

    StatsParser(data=total_summary, webdir="~/public_html/dump/scouting/").do()
    time.sleep(30*60)

if __name__ == "__main__":

    print("Did you do `./make_tar.sh`? Sleeping for 5s for you to quit if not.")
    time.sleep(5)

    # Entries of [CRAB request name, output baby tag, extra string passed to babymaker]
    info = [
            # ["skim_2018A_v4","v4", ""],
            # ["skim_2018B_v4","v4", ""],
            # ["skim_2018C_v4","v4", ""],
            # ["skim_2018D_v4","v4", ""],
            # ["skim_2018C_v4_unblind1fb","v4", ""],

            ["skim_2018C_v4_unblind1fb","vtestskim1cm", "--skim1cm"],
            ]
    submit(info)

