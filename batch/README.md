## Info

RAW ntuples are generated/slimmed first, then these are made into babies.

### (Slimmed) RAW ntuples

#### Data
RAW scouting data is already available, but it stores huge FED and track info, so we first skim it with CRAB
* Do `. install_cmssw.sh`. This sets up a CMSSW environment with some EDFilters and a small EDAnalyzer to strip out the L1 information. (Note that `Scouting/NtupleMaker/test/dataproducer.py` is the relevant PSet for slim/skimming)
* Submit crab jobs
  * `source /cvmfs/cms.cern.ch/crab3/crab.sh` for crab commands
  * submit with
```bash
# A-D
crab submit -c crabcfg.py General.requestName="skim_2018A_v4" Data.inputDataset="/ScoutingCaloMuon/Run2018A-v1/RAW" ;
crab submit -c crabcfg.py General.requestName="skim_2018B_v4" Data.inputDataset="/ScoutingCaloMuon/Run2018B-v1/RAW" ;
crab submit -c crabcfg.py General.requestName="skim_2018C_v4" Data.inputDataset="/ScoutingCaloMuon/Run2018C-v1/RAW" ;
crab submit -c crabcfg.py General.requestName="skim_2018D_v4" Data.inputDataset="/ScoutingCaloMuon/Run2018D-v1/RAW" ;

# C again, but just the unblinded set
crab submit -c crabcfg.py General.requestName="skim_2018D_v4_unblind1fb" Data.inputDataset="/ScoutingCaloMuon/Run2018D-v1/RAW" Data.lumiMask="data/unblind_2018C_1fb_JSON.txt" Data.unitsPerJob=2000000;
```
  * Spam `crab status -c crab/<requestname>`, `crab resubmit -c ...`

#### MC
First, we make and store EDM RAW-tier data to make further iteration faster.
* Submit jobs with [https://github.com/usarica/DisplacedMuons/tree/master/MCSubmission](https://github.com/usarica/DisplacedMuons/tree/master/MCSubmission) to get RAWSIM output
* Follow the instructions for Data above without submitting any crab jobs. We will just do a local `cmsRun` to make a single file. Now the PSet is `mcproducer.py` instead of `dataproducer.py`. You will need to edit paths and maybe the global tag inside the PSet.


### Flattened babies (non-EDM)

* Run `python babymaker.py -h` to see all the options. A list of files can be specified. Note that the `-a` option will retain all events:
no skim of >=1 DV and >=2 Muon is performed (useful for MC samples where acceptance needs to be calculated).

* Clone [ProjectMetis](https://github.com/aminnj/ProjectMetis/) and source its environment
* Run the babymaker on a file locally to test
* Edit `submit_baby_jobs.py` to have the right paths (search for "hadoop") to the crab output, including the request names, output tags, and skimming options (search for "skim")
* `./make_tar.sh` to make the tarball for the jobs
* `python submit_baby_jobs.py`
* For now, this just does data. From earlier instructions MC should just be in a single file, so we run `python babymaker.py -a <filename>` locally and wait half an hour.

