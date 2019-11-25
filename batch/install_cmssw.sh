source /cvmfs/cms.cern.ch/cmsset_default.sh

release=CMSSW_10_2_5
cmsrel $release
cd $_
cmsenv
cd -

cd $release/src
ln -s ../../Scouting/
scram b
cd -
