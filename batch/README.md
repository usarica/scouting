## Instructions

* In general, use a `CMSSW_10_2_5` environment.

### Make a (non-EDM) slim/skim
* Run `python slim_and_skim.py -h` to see all the options. A list of files can be specified. Note that the `-a` option will retain all events:
no skim of >=1 DV and >=2 Muon is performed (useful for MC samples where acceptance needs to be calculated).

### Make (an EDM) slim/skim of data with CRAB

* First do `. install_filter.sh` to set up the EDFilters for skimming
* Note that `pset.py` is the relevant PSet for slim/skimming (testable locally with `cmsRun`)
* Submit crab jobs
  * `source /cvmfs/cms.cern.ch/crab3/crab.sh` for crab commands
  * submit with
```bash
for era in A B C D ; do 
    crab submit -c crabcfg.py General.requestName="skim_2018${era}" Data.inputDataset="/ScoutingCaloMuon/Run2018${era}-v1/RAW" ;
done
```
  * Spam `crab status -c crab/skim2018A`, `crab resubmit -c ...`

### Make nicer branches (non-EDM) from the CRAB output

* Check out [ProjectMetis](https://github.com/aminnj/ProjectMetis/) and source its environment
* Run `python slim_and_skim.py <filename>` on a file locally to test
* Edit `submit.py` to have the right paths to the crab output
* `tar cvzf package.tar.gz slim_and_skim.py` to make the (trivial) tarball for the jobs
* `python submit.py`

