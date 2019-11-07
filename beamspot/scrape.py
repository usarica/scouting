#!/usr/bin/env python

import os, sys

from itertools import groupby
import glob
import time
import json
import glob
from tqdm import tqdm
import ROOT as r
import concurrent.futures

def xrootdify(fname):
    if "/namin/" in fname:
        fname = "root://redirector.t2.ucsd.edu/" + fname.replace("/hadoop/cms","")
    if fname.startswith("/store"):
        fname = "root://cmsxrootd.fnal.gov/" + fname
    return fname


def dict_to_csv(d):
    buff = "x,y,z,run,lumi\n"
    for (run,lumi),(x0,y0,z0) in d.items():
        buff += "{},{},{},{},{}\n".format(x0, y0, z0, run, lumi)
    return buff

def save_one(fname_in,fname_out):
    try:
        ch = r.TChain("Events")
        ch.Add(fname_in)

        N = ch.GetEntries()
        ch.SetEstimate(N)

        t0 = time.time()
        N = ch.Draw(
                "recoBeamSpot_offlineBeamSpot__RECO.obj.x0()"
                ":recoBeamSpot_offlineBeamSpot__RECO.obj.y0()"
                ":recoBeamSpot_offlineBeamSpot__RECO.obj.z0()"
                ":EventAuxiliary.run()"
                ":EventAuxiliary.luminosityBlock()","","goff")
        t1 = time.time()

        vx0 = ch.GetVal(0)
        vy0 = ch.GetVal(1)
        vz0 = ch.GetVal(2)
        vrun = ch.GetVal(3)
        vlumi = ch.GetVal(4)

        data = {}
        for i in range(N):
            run = int(vrun[i])
            lumi = int(vlumi[i])
            if (run,lumi) not in data:
                x0 = vx0[i]
                y0 = vy0[i]
                z0 = vz0[i]
                data[(run,lumi)] = (x0,y0,z0)

        buff = dict_to_csv(data)
    except:
        print("Error with {}".format(fname_in))
        return False

    with open(fname_out,"w") as fh:
        fh.write(buff)

    return True


if __name__ == "__main__":

    executor = concurrent.futures.ProcessPoolExecutor(12)

    import dis_client as dis

    # files = (
    #         dis.query("/MET/Run2018A-17Sep2018-v1/MINIAOD",typ="files",detail=True)["payload"]
    #         + dis.query("/MET/Run2018B-17Sep2018-v1/MINIAOD",typ="files",detail=True)["payload"]
    #         + dis.query("/MET/Run2018C-17Sep2018-v1/MINIAOD",typ="files",detail=True)["payload"]
    #         + dis.query("/MET/Run2018D-PromptReco-v2/MINIAOD",typ="files",detail=True)["payload"]
    #         )
    # outdir = "outputs_full2018/"

    files = (
            dis.query("/MET/Run2017B-31Mar2018-v1/MINIAOD",typ="files",detail=True)["payload"]
            + dis.query("/MET/Run2017C-31Mar2018-v1/MINIAOD",typ="files",detail=True)["payload"]
            + dis.query("/MET/Run2017D-31Mar2018-v1/MINIAOD",typ="files",detail=True)["payload"]
            + dis.query("/MET/Run2017E-31Mar2018-v1/MINIAOD",typ="files",detail=True)["payload"]
            + dis.query("/MET/Run2017F-31Mar2018-v1/MINIAOD",typ="files",detail=True)["payload"]
            )
    outdir = "outputs_full2017/"

    fnames = [f["name"] for f in files if f["nevents"]>0]
    print(len(fnames))

    os.system("mkdir -p {}".format(outdir))

    futures = []
    fnames = map(xrootdify,fnames)
    for fname in tqdm(fnames):
        fname_out = outdir+"/"+fname.split("/store/data/",1)[1].replace("/","_").replace(".root",".csv")
        if os.path.exists(fname_out): continue
        executor.submit(save_one,fname,fname_out)

    for future in tqdm(concurrent.futures.as_completed(futures),total=len(futures)):
        _ = future.result()
