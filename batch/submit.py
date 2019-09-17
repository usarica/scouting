from metis.CMSSWTask import CMSSWTask
from metis.Sample import DirectorySample, DBSSample
from metis.StatsParser import StatsParser
from metis.Optimizer import Optimizer
import time

import numpy as np

def main():
    optimizer = Optimizer()
    total_summary = {}

    # Technically not a cmssw job, just a python script we execute, but be lazy and use CMSSWTask
    # and tell it the python script is a pset, but our executable uses python instead of cmsRun
    # and we don't want to edit pset stuff at the end in CMSSWTask.py (`dont_edit_pset`)


    for ds in [
            "/ScoutingCaloMuon/Run2018A-v1/RAW",
            # "/ScoutingCaloMuon/Run2018B-v1/RAW",
            # "/ScoutingCaloMuon/Run2018C-v1/RAW",
            # "/ScoutingCaloMuon/Run2018D-v1/RAW",
            ]:

        task = CMSSWTask(
                sample = DBSSample(dataset=ds),
                output_name = "output.root",
                executable = "executables/scouting_exe.sh",
                pset = "slim_and_skim.py",
                cmssw_version = "CMSSW_10_2_5",
                scram_arch = "slc6_amd64_gcc700",
                publish_to_dis = False,
                snt_dir = False,
                dont_edit_pset = True,
                tag = "v2",
                events_per_output = 5e6,
                )
        task.process(optimizer=optimizer)
        summary = task.get_task_summary()
        total_summary[task.get_sample().get_datasetname()] = summary

    StatsParser(data=total_summary, webdir="~/public_html/dump/scouting/").do()
    time.sleep(30*60)

def test():
    optimizer = Optimizer()
    total_summary = {}

    # Technically not a cmssw job, just a python script we execute, but be lazy and use CMSSWTask
    # and tell it the python script is a pset, but our executable uses python instead of cmsRun
    # and we don't want to edit pset stuff at the end in CMSSWTask.py (`dont_edit_pset`)


    for ds in [
            "/ScoutingCaloMuon/Run2018A-v1/RAW",
            "/ScoutingCaloMuon/Run2018B-v1/RAW",
            "/ScoutingCaloMuon/Run2018C-v1/RAW",
            "/ScoutingCaloMuon/Run2018D-v1/RAW",
            ]:

        task = CMSSWTask(
                sample = DBSSample(dataset=ds),
                output_name = "output.root",
                executable = "executables/scouting_exe.sh",
                pset = "slim_and_skim.py",
                cmssw_version = "CMSSW_10_2_5",
                scram_arch = "slc6_amd64_gcc700",
                publish_to_dis = False,
                snt_dir = False,
                dont_edit_pset = True,
                tag = "vtest",
                events_per_output = 500e3,
                max_jobs = 10,
                )
        task.process(optimizer=optimizer)
        summary = task.get_task_summary()
        total_summary[task.get_sample().get_datasetname()] = summary

    StatsParser(data=total_summary, webdir="~/public_html/dump/scouting/").do()
    time.sleep(30*60)

if __name__ == "__main__":

    main()
    # test()
