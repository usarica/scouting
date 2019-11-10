from metis.CMSSWTask import CMSSWTask
from metis.CondorTask import CondorTask
from metis.Sample import DirectorySample, DBSSample, DummySample
from metis.StatsParser import StatsParser
from metis.Optimizer import Optimizer
import time

def submit():
    total_summary = {}

    extra_requirements = "True"
    blacklisted_machines = [
             "cabinet-4-4-29.t2.ucsd.edu",
             "cabinet-7-7-36.t2.ucsd.edu",
             "cabinet-8-8-1.t2.ucsd.edu",
             ]
    if blacklisted_machines:
        extra_requirements = " && ".join(map(lambda x: '(TARGET.Machine != "{0}")'.format(x),blacklisted_machines))

    tag = "v1"
    # total_events = 50000
    # events_per_job = 500
    total_events = 100000
    events_per_job = 500
    for mass,ctau in [
            [5,10],
            [5,25],
            [5,50],
            [8,10],
            [8,25],
            [8,50],
            [10,10],
            [10,25],
            [10,50],
            [12,10],
            [12,25],
            [12,50],
            [15,10],
            [15,25],
            [15,50],
            [18,10],
            [18,25],
            [18,50],
            [20,10],
            [20,25],
            [20,50],
            ]:
        reqname = "mzd{}_ctau{}_{}".format(mass,ctau,tag)
        njobs = total_events//events_per_job
        task = CondorTask(
                sample = DummySample(dataset="/HToZdZdTo2Mu2X/params_mzd{}_ctau{}mm/RAWSIM".format(mass,ctau),N=njobs,nevents=total_events),
                output_name = "output.root",
                executable = "executables/condor_executable.sh",
                tarfile = "package.tar.gz",
                # open_dataset = True,
                files_per_output = 1,
                condor_submit_params = {
                    # "sites":"T2_US_UCSD",
                    "classads": [
                        ["param_mass",mass],
                        ["param_ctau",ctau],
                        ["param_nevents",events_per_job],
                        ["metis_extraargs",""],
                        ["JobBatchName",reqname],
                        ],
                    "requirements_line": 'Requirements = ((HAS_SINGULARITY=?=True) && (HAS_CVMFS_cms_cern_ch =?= true) && {extra_requirements})'.format(extra_requirements=extra_requirements),
                    },
                tag = tag,
                )

        task.process()
        total_summary[task.get_sample().get_datasetname()] = task.get_task_summary()

    StatsParser(data=total_summary, webdir="~/public_html/dump/scouting/").do()

if __name__ == "__main__":

    for i in range(500):
        submit()
        time.sleep(60*60)

