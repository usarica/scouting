## References

* [https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFireworksGeometry](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFireworksGeometry)
* [https://github.com/cms-sw/cmssw/blob/master/Fireworks/Core/interface/FWRecoGeom.h](https://github.com/cms-sw/cmssw/blob/master/Fireworks/Core/interface/FWRecoGeom.h)

## Instructions

* Edit `dumpRecoGeometry_cfg.py` to have the desired global tag (search for `data2018`, `mc2018`, `2017`, ...)
* Note, need to play with `process.source.firstRun` in order to pick up the right geometry (if data,
pick a run within the collection period, or comment it out for MC).
* In a `CMSSW_10_2_5` environment, run `cmsRun dumpRecoGeometry_cfg.py tag=data2018 tracker=True muon=False calo=False`,
specifying `tag` appropriately
* The `dump_for_uproot.py` script converts the output of cmsRun into something flatter/more-friendly for uproot.
* Look inside `../analysis/pixelgeometry.ipynb` for geometry visualization stuff
