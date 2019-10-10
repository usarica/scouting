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
    # print(N, t1-t0)

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
    with open(fname_out,"w") as fh:
        fh.write(buff)

    return True
    # return dict_to_csv
    # print("x,y,z,run,lumi")




if __name__ == "__main__":

    # fnames = ["root://cmsxrootd.fnal.gov//store/data/Run2018C/MET/MINIAOD/17Sep2018-v1/100000/2E6BCD18-5138-7340-B7A8-1CB666726AB4.root"]

    executor = concurrent.futures.ProcessPoolExecutor(8)

    import dis_client as dis
    files = dis.query("/MET/Run2018C-17Sep2018-v1/MINIAOD",typ="files",detail=True)["payload"]
    fnames = [f["name"] for f in files]
    print(len(fnames))

    outdir = "outputs/"
    os.system("mkdir -p {}".format(outdir))

    futures = []
    fnames = map(xrootdify,fnames)
    for fname in tqdm(fnames):
        fname_out = outdir+"/"+fname.split("/store/data/",1)[1].replace("/","_").replace(".root",".csv")
        if os.path.exists(fname_out): continue
        # save_one(fname,fname_out)
        executor.submit(save_one,fname,fname_out)

    for future in tqdm(concurrent.futures.as_completed(futures),total=len(futures)):
        _ = future.result()
