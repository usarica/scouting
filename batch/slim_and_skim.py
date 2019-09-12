import os
import sys

import ROOT as r
from tqdm import tqdm

import array
import time
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("fnames", help="input file(s)", nargs="*")
parser.add_argument("-n", "--nevents", help="max number of events to process (-1 = all)", default=-1, type=int)
parser.add_argument("-e", "--expected", help="expected number of events", default=-1, type=int)
args = parser.parse_args()
nevents = args.nevents
fnames = sum(map(lambda x:x.split(","),args.fnames),[])
print fnames
def xrootdify(fname):
    if fname.startswith("/store"):
        fname = "root://cmsxrootd.fnal.gov/" + fname
    return fname
fnames = map(xrootdify,fnames)

treename = "Events"
fname_out = "output.root" 

ch = r.TChain(treename)
for fname in fnames:
    ch.Add(fname)
ch.SetBranchStatus("ScoutingTracks_hltScoutingTrackPacker__HLT.*",0)
ch.SetBranchStatus("FEDRawDataCollection_hltFEDSelectorL1__HLT.*",0)
ch.SetBranchStatus("edmTriggerResults_TriggerResults__HLT.*",0)


newfile = r.TFile(fname_out, "recreate")
newtree = r.TTree(treename,"")

branches = {}
def make_branch(name, tstr="vi"):
    global branches
    extra = []
    if tstr == "vvi":
        obj = r.vector("vector<int>")()
    if tstr == "vi":
        obj = r.vector("int")()
    if tstr == "vf":
        obj = r.vector("float")()
    if tstr == "vb":
        obj = r.vector("bool")()
    if tstr == "f":
        obj = array.array("f",[999])
        extra.append("{}/f".format(name))
    if tstr == "b":
        obj = array.array("b",[0])
        extra.append("{}/O".format(name))
    if tstr == "i":
        obj = array.array("I",[999])
        extra.append("{}/I".format(name))
    if tstr == "l":
        obj = array.array("L",[999])
        extra.append("{}/L".format(name))
    branches[name] = obj
    newtree.Branch(name,obj,*extra)

def clear_branches():
    global branches
    for v in branches.values():
        if hasattr(v,"clear"):
            v.clear()

make_branch("run", "l")
make_branch("luminosityBlock", "l")
make_branch("event", "l")

make_branch("MET_pt", "f")
make_branch("MET_phi", "f")
make_branch("rho", "f")
make_branch("LeadingPair_mass", "f")
make_branch("LeadingPair_sameVtx", "b")
make_branch("LeadingPair_isOS", "b")

make_branch("DV_x","vf")
make_branch("DV_y","vf")
make_branch("DV_z","vf")
make_branch("DV_xError","vf")
make_branch("DV_yError","vf")
make_branch("DV_zError","vf")
make_branch("DV_tracksSize","vf")
make_branch("DV_chi2","vf")
make_branch("DV_ndof","vf")
make_branch("DV_isValidVtx","vf")

make_branch("Jet_pt", "vf")
make_branch("Jet_eta", "vf")
make_branch("Jet_phi", "vf")
make_branch("Jet_m", "vf")
make_branch("Jet_jetArea", "vf")
make_branch("Jet_maxEInEmTowers", "vf")
make_branch("Jet_maxEInHadTowers", "vf")
make_branch("Jet_hadEnergyInHB", "vf")
make_branch("Jet_hadEnergyInHE", "vf")
make_branch("Jet_hadEnergyInHF", "vf")
make_branch("Jet_emEnergyInEB", "vf")
make_branch("Jet_emEnergyInEE", "vf")
make_branch("Jet_emEnergyInHF", "vf")
make_branch("Jet_towersArea", "vf")
make_branch("Jet_mvaDiscriminator", "vf")
make_branch("Jet_btagDiscriminator", "vf")

make_branch("PV_x", "vf")
make_branch("PV_y", "vf")
make_branch("PV_z", "vf")
make_branch("PV_zError", "vf")
make_branch("PV_xError", "vf")
make_branch("PV_yError", "vf")
make_branch("PV_tracksSize", "vi")
make_branch("PV_chi2", "vf")
make_branch("PV_ndof", "vi")
make_branch("PV_isValidVtx", "vb")

make_branch("PVM_x", "vf")
make_branch("PVM_y", "vf")
make_branch("PVM_z", "vf")
make_branch("PVM_zError", "vf")
make_branch("PVM_xError", "vf")
make_branch("PVM_yError", "vf")
make_branch("PVM_tracksSize", "vi")
make_branch("PVM_chi2", "vf")
make_branch("PVM_ndof", "vi")
make_branch("PVM_isValidVtx", "vb")

make_branch("Muon_pt", "vf")
make_branch("Muon_eta", "vf")
make_branch("Muon_phi", "vf")
make_branch("Muon_m", "vf")
make_branch("Muon_ecalIso", "vf")
make_branch("Muon_hcalIso", "vf")
make_branch("Muon_trackIso", "vf")
make_branch("Muon_chi2", "vf")
make_branch("Muon_ndof", "vf")
make_branch("Muon_charge", "vi")
make_branch("Muon_dxy", "vf")
make_branch("Muon_dz", "vf")
make_branch("Muon_nValidMuonHits", "vi")
make_branch("Muon_nValidPixelHits", "vi")
make_branch("Muon_nMatchedStations", "vi")
make_branch("Muon_nTrackerLayersWithMeasurement", "vi")
make_branch("Muon_type", "vi")
make_branch("Muon_nValidStripHits", "vi")
make_branch("Muon_trk_qoverp", "vf")
make_branch("Muon_trk_lambda", "vf")
make_branch("Muon_trk_pt", "vf")
make_branch("Muon_trk_phi", "vf")
make_branch("Muon_trk_eta", "vf")
make_branch("Muon_dxyError", "vf")
make_branch("Muon_dzError", "vf")
make_branch("Muon_trk_qoverpError", "vf")
make_branch("Muon_trk_lambdaError", "vf")
make_branch("Muon_trk_phiError", "vf")
make_branch("Muon_trk_dsz", "vf")
make_branch("Muon_trk_dszError", "vf")
make_branch("Muon_vtxIndx","vvi")
make_branch("Muon_vtxNum","vi")
make_branch("Muon_vtxIndx1","vi")
make_branch("Muon_vtxIndx2","vi")
make_branch("Muon_vtxIndx3","vi")
make_branch("Muon_vtxIndx4","vi")
make_branch("Muon_vtxIndx5","vi")

newtree.SetBasketSize("*",128000)

v1 = r.TLorentzVector()
v2 = r.TLorentzVector()

ievt = 0
# for ievt, evt in enumerate(tqdm(ch,total=ch.GetEntries())):
# for ievt, evt in enumerate(t):
print ">>> Started slimming/skimming tree"
t0 = time.time()
for evt in ch:
    if ievt % 10000 == 0:
        print ievt
    if (nevents > 0) and (ievt > nevents): break
    ievt += 1

    dvs = evt.ScoutingVertexs_hltScoutingMuonPackerCalo_displacedVtx_HLT.product()
    nDV = dvs.size()
    if nDV < 1: continue

    muons = evt.ScoutingMuons_hltScoutingMuonPackerCalo__HLT.product()
    nMuons = muons.size()
    if nMuons < 2: continue

    jets = evt.ScoutingCaloJets_hltScoutingCaloPacker__HLT.product()
    nJet = muons.size()

    pvs = evt.ScoutingVertexs_hltScoutingPrimaryVertexPacker_primaryVtx_HLT.product()
    pvms = evt.ScoutingVertexs_hltScoutingPrimaryVertexPackerCaloMuon_primaryVtx_HLT.product()

    clear_branches()

    branches["run"][0] = int(evt.EventAuxiliary.run())
    branches["luminosityBlock"][0] = int(evt.EventAuxiliary.luminosityBlock())
    branches["event"][0] = int(evt.EventAuxiliary.event())

    branches["MET_pt"][0] = evt.double_hltScoutingCaloPacker_caloMetPt_HLT.product()[0]
    branches["MET_phi"][0] = evt.double_hltScoutingCaloPacker_caloMetPhi_HLT.product()[0]
    branches["rho"][0] = evt.double_hltScoutingCaloPacker_rho_HLT.product()[0]

    for dv in dvs:
        for k in branches:
            if k.startswith("DV_"):
                branches[k].push_back(getattr(dv,k.replace("DV_",""))())
        # branches["DV_x"].push_back(dv.x())
        # branches["DV_y"].push_back(dv.y())
        # branches["DV_z"].push_back(dv.z())

    for pv in pvs:
        for k in branches:
            if k.startswith("PV_"):
                branches[k].push_back(getattr(pv,k.replace("PV_",""))())

    for pvm in pvms:
        for k in branches:
            if k.startswith("PVM_"):
                branches[k].push_back(getattr(pvm,k.replace("PVM_",""))())

    for jet in jets:
        for k in branches:
            if k.startswith("Jet_"):
                branches[k].push_back(getattr(jet,k.replace("Jet_",""))())


    for muon in muons:
        for k in branches:
            if k.startswith("Muon_") and k not in [
                    "Muon_vtxIndx",
                    "Muon_vtxIndx1",
                    "Muon_vtxIndx2",
                    "Muon_vtxIndx3",
                    "Muon_vtxIndx4",
                    "Muon_vtxIndx5",
                    "Muon_vtxNum",
                    ]:
                branches[k].push_back(getattr(muon,k.replace("Muon_",""))())
        indices = muon.vtxIndx()
        num = len(indices)
        branches["Muon_vtxIndx"].push_back(indices)
        branches["Muon_vtxNum"].push_back(num)
        if num > 0: branches["Muon_vtxIndx1"].push_back(indices[0])
        else: branches["Muon_vtxIndx1"].push_back(-1)
        if num > 1: branches["Muon_vtxIndx2"].push_back(indices[1])
        else: branches["Muon_vtxIndx2"].push_back(-1)
        if num > 2: branches["Muon_vtxIndx3"].push_back(indices[2])
        else: branches["Muon_vtxIndx3"].push_back(-1)
        if num > 3: branches["Muon_vtxIndx4"].push_back(indices[3])
        else: branches["Muon_vtxIndx4"].push_back(-1)
        if num > 4: branches["Muon_vtxIndx5"].push_back(indices[4])
        else: branches["Muon_vtxIndx5"].push_back(-1)

    if len(muons) >= 2:
        v1.SetPtEtaPhiM(muons[0].pt(), muons[0].eta(), muons[0].phi(), muons[0].m())
        v2.SetPtEtaPhiM(muons[1].pt(), muons[1].eta(), muons[1].phi(), muons[1].m())
        branches["LeadingPair_mass"][0] = (v1+v2).M()
        branches["LeadingPair_sameVtx"][0] = (branches["Muon_vtxNum"][0]>0) and (branches["Muon_vtxNum"][1]>0) and (branches["Muon_vtxIndx1"][0] == branches["Muon_vtxIndx1"][1])
        branches["LeadingPair_isOS"][0] = (branches["Muon_charge"][0] == -branches["Muon_charge"][1])
    else:
        branches["LeadingPair_mass"][0] = 0.
        branches["LeadingPair_sameVtx"][0] = False
        branches["LeadingPair_isOS"][0] = False

    newtree.Fill()
t1 = time.time()

print ">>> Finished slim/skim of {} events in {:.2f} seconds @ {:.1f}Hz".format(ievt,(t1-t0),ievt/(t1-t0))
print ">>> Output tree has size {:.1f}MB and {} events".format(os.stat(fname_out).st_size/1e6,newtree.GetEntries())

if args.expected > 0:
    print "Expected {} events and ran on {}".format(args.expected,ievt)
    # FIXME do we delete if they don't match?


newtree.Write()
newfile.Close()

