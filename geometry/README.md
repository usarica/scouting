CMSSW_10_2_5
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFireworksGeometry
https://github.com/cms-sw/cmssw/blob/master/Fireworks/Core/interface/FWRecoGeom.h

cmsRun dumpRecoGeometry_cfg.py tracker=True muon=False calo=False
python dump_for_uproot.py
```
idToGeo->Draw("translation[0]:translation[1]:translation[2]","pow(translation[0],2)+pow(translation[1],2)<18*18","box2")
```
