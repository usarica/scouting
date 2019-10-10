
source /cvmfs/cms.cern.ch/cmsset_default.sh

release=CMSSW_10_2_5
cmsrel $release
cd $_
cmsenv
cd -


plugindir=$release/src/MyFilter/Dummy/plugins
mkdir -p $plugindir
cat <<EOF > $plugindir/MyFilter.cc
#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/ObjectCountFilter.h"
#include "DataFormats/Scouting/interface/ScoutingMuon.h"
#include "DataFormats/Scouting/interface/ScoutingVertex.h"
typedef ObjectCountFilter<ScoutingMuonCollection>::type ScoutingMuonCountFilter;
DEFINE_FWK_MODULE(ScoutingMuonCountFilter);
typedef ObjectCountFilter<ScoutingVertexCollection>::type ScoutingVertexCountFilter;
DEFINE_FWK_MODULE(ScoutingVertexCountFilter);
EOF

cat <<EOF > $plugindir/BuildFile.xml
<use name="FWCore/Framework"/>
<flags EDM_PLUGIN="1"/>
EOF

cd $release
scram b
cd -
