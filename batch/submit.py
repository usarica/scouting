from metis.CMSSWTask import CMSSWTask
from metis.CondorTask import CondorTask
from metis.Sample import DirectorySample, DBSSample
from metis.StatsParser import StatsParser
from metis.Optimizer import Optimizer
import time

import numpy as np

def main():
    total_summary = {}

    extra_requirements = "True"
    blacklisted_machines = [
             "cabinet-4-4-29.t2.ucsd.edu",
             "cabinet-7-7-36.t2.ucsd.edu",
             "cabinet-8-8-1.t2.ucsd.edu",
             ]
    if blacklisted_machines:
        extra_requirements = " && ".join(map(lambda x: '(TARGET.Machine != "{0}")'.format(x),blacklisted_machines))

    # for era in ["B"]:
    # for era in ["B","C"]:
    for era in ["A","B","C","D"]:
        extra = {}
        # if era == "D":
        #     extra = dict(open_dataset=True)
        task = CondorTask(
                sample = DirectorySample(
                    location = "/hadoop/cms/store/user/namin/ScoutingCaloMuon/crab_skim_2018{}/190919_*/0000/".format(era),
                    dataset = "/ScoutingCaloMuon/Run2018{}-v1/RAW".format(era)
                    ),
                output_name = "output.root",
                executable = "executables/scouting_exe.sh",
                tarfile = "package.tar.gz",
                MB_per_output = 3000,
                condor_submit_params = {
                    "sites":"T2_US_UCSD",  # I/O is hella faster
                    "classads": [ 
                        ["JobBatchName","scouting_2018{}".format(era)],
                        ],
                    "requirements_line": 'Requirements = ((HAS_SINGULARITY=?=True) && (HAS_CVMFS_cms_cern_ch =?= true) && {extra_requirements})'.format(extra_requirements=extra_requirements),
                    },
                cmssw_version = "CMSSW_10_2_5",
                scram_arch = "slc6_amd64_gcc700",
                tag = "v3",
                **extra
                )

        task.process()
        summary = task.get_task_summary()
        total_summary[task.get_sample().get_datasetname()] = summary

    StatsParser(data=total_summary, webdir="~/public_html/dump/scouting/").do()
    time.sleep(30*60)

if __name__ == "__main__":

    main()

