from metis.CMSSWTask import CMSSWTask
from metis.CondorTask import CondorTask
from metis.Sample import DirectorySample, DBSSample
from metis.StatsParser import StatsParser
from metis.Optimizer import Optimizer
import time
import glob

extra_requirements = "True"
blacklisted_machines = [
         "cabinet-4-4-29.t2.ucsd.edu",
         "cabinet-7-7-36.t2.ucsd.edu",
         "cabinet-8-8-1.t2.ucsd.edu",
         ]
if blacklisted_machines:
    extra_requirements = " && ".join(map(lambda x: '(TARGET.Machine != "{0}")'.format(x),blacklisted_machines))


def get_data_tasks(info):
    tasks = []
    for reqname,tag,extra_args in info:
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
        tasks.append(task)
    return tasks

def get_mc_tasks(pattern,tag,extra_args=""):
    samples = []
    for location in glob.glob(pattern):
        taskname = location.rstrip("/").rsplit("/")[-1]
        dataset = "/{}/{}/BABY".format(
                taskname.split("_",1)[0],
                taskname.split("_",1)[1].split("_RAWSIM")[0],
                )
        samples.append(DirectorySample(location=location, dataset=dataset))
    tasks = []
    for sample in samples:
        task = CondorTask(
                sample = sample,
                output_name = "output.root",
                executable = "executables/scouting_exe.sh",
                tarfile = "package.tar.gz",
                files_per_output = int(1e5),
                condor_submit_params = {
                    "sites":"T2_US_UCSD",
                    "classads": [
                        ["metis_extraargs",extra_args],
                        ["JobBatchName",sample.get_datasetname().split("/")[2].replace("params_","")],
                        ],
                    "requirements_line": 'Requirements = ((HAS_SINGULARITY=?=True) && (HAS_CVMFS_cms_cern_ch =?= true) && {extra_requirements})'.format(extra_requirements=extra_requirements),
                    },
                cmssw_version = "CMSSW_10_2_5",
                scram_arch = "slc6_amd64_gcc700",
                tag = tag,
                )
        tasks.append(task)
    return tasks

if __name__ == "__main__":

    print("Did you do `./make_tar.sh`? Sleeping for 5s for you to quit if not.")
    time.sleep(5)

    # Entries of [CRAB request name, output baby tag, extra string passed to babymaker]
    data_info = [
            # ["skim_2018A_v4","v4", ""],
            # ["skim_2018B_v4","v4", ""],
            # ["skim_2018C_v4","v4", ""],
            # ["skim_2018D_v4","v4", ""],
            # ["skim_2018C_v4_unblind1fb","v4", ""],

            # ["skim_2018C_v4_unblind1fb","vtestskim1cm", "--skim1cm"],
            ]
    data_tasks = get_data_tasks(data_info)

    mc_tasks = get_mc_tasks(
            pattern="/hadoop/cms/store/user/namin/ProjectMetis/HToZdZdTo2Mu2X_params_mzd*_ctau*mm_RAWSIM_*/",
            tag="v4",
            )

    for _ in range(500):
        total_summary = {}
        for task in data_tasks + mc_tasks:
            task.process()
            total_summary[task.get_sample().get_datasetname()] = task.get_task_summary()
        StatsParser(data=total_summary, webdir="~/public_html/dump/scouting/").do()
        time.sleep(30*60)
