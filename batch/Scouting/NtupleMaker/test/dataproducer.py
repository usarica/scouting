import FWCore.ParameterSet.Config as cms

process = cms.Process('SLIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')


## ----------------- Global Tag ------------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = "101X_dataRun2_HLT_v7" # from edmProvDump, used for 2018A,B,C,D
# 92X_dataRun2_HLT_v4 for 2017C, and 92X_dataRun2_HLT_v7 for 2017D,E,F
# process.GlobalTag.globaltag = "102X_upgrade2018_realistic_v15"

process.maxEvents = cms.untracked.PSet(
    # input = cms.untracked.int32(-1)
    input = cms.untracked.int32(20000)
)
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(True),
    fileNames = cms.untracked.vstring('file:/hadoop/cms/store/user/namin/nanoaod/ScoutingCaloMuon__Run2018C-v1/6A94C331-F38D-E811-B4D7-FA163E146D61.root'),
    # fileNames = cms.untracked.vstring('file:/home/users/namin/2019/scouting/repo/reco/output_rawsim_5k.root'),
    # fileNames = cms.untracked.vstring('file:/hadoop/cms/store/user/namin/DisplacedMuons/2018/GluGluTo0PHH125ToZprimeZprimeTo2Mu2X_CTauVprime_20mm/PREMIX-RAWSIM/premixraw_1230385_slimmed.root'),
    # fileNames = cms.untracked.vstring('/store/data/Run2018B/ScoutingCaloMuon/RAW/v1/000/317/696/00000/761E614C-156E-E811-B5AA-FA163E373C99.root'),
    inputCommands = cms.untracked.vstring(
        'keep *', 
        'drop *_hltScoutingTrackPacker_*_*', 
    ),
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:output.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('skimpath'),
        ),
    outputCommands = cms.untracked.vstring(
        'keep *', 
        'drop *_hltFEDSelectorL1_*_*', 
        'drop FEDRawDataCollection_*_*_*',
        'drop *_gtStage2Digis_*_*', 
        ),
     basketSize = cms.untracked.int32(128*1024), # 128kb basket size instead of ~30kb default
)
process.outpath = cms.EndPath(process.out)


# process.options = cms.untracked.PSet(
#         allowUnscheduled = cms.untracked.bool(True),
#         wantSummary = cms.untracked.bool(True),
# )

process.Timing = cms.Service("Timing",
        summaryOnly = cms.untracked.bool(True)
        )

process.countmu = cms.EDFilter("ScoutingMuonCountFilter",
    src = cms.InputTag("hltScoutingMuonPackerCalo"),
    minNumber = cms.uint32(2)
)

process.countvtx = cms.EDFilter("ScoutingVertexCountFilter",
    src = cms.InputTag("hltScoutingMuonPackerCalo","displacedVtx"),
    minNumber = cms.uint32(1)
)

L1Info = ["L1_DoubleMu0", "L1_DoubleMu0_Mass_Min1", "L1_DoubleMu0_OQ",
 "L1_DoubleMu0_SQ", "L1_DoubleMu0_SQ_OS", "L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4",
 "L1_DoubleMu0er1p5_SQ", "L1_DoubleMu0er1p5_SQ_OS",
 "L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4", "L1_DoubleMu0er1p5_SQ_dR_Max1p4",
 "L1_DoubleMu0er2p0_SQ_OS_dR_Max1p4", "L1_DoubleMu0er2p0_SQ_dR_Max1p4",
 "L1_DoubleMu10_SQ", "L1_DoubleMu18er2p1", "L1_DoubleMu4_SQ_OS",
 "L1_DoubleMu4_SQ_OS_dR_Max1p2", "L1_DoubleMu4p5_SQ_OS",
 "L1_DoubleMu4p5_SQ_OS_dR_Max1p2", "L1_DoubleMu4p5er2p0_SQ_OS",
 "L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18", "L1_DoubleMu9_SQ", "L1_DoubleMu_12_5",
 "L1_DoubleMu_15_5_SQ", "L1_DoubleMu_15_7", "L1_DoubleMu_15_7_Mass_Min1",
 "L1_DoubleMu_15_7_SQ", "L1_QuadMu0", "L1_QuadMu0_OQ", "L1_QuadMu0_SQ",
 "L1_TripleMu0", "L1_TripleMu0_OQ", "L1_TripleMu0_SQ", "L1_TripleMu3",
 "L1_TripleMu3_SQ", "L1_TripleMu_5SQ_3SQ_0OQ",
 "L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9",
 "L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9", "L1_TripleMu_5_3_3",
 "L1_TripleMu_5_3_3_SQ", "L1_TripleMu_5_3p5_2p5",
 "L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17",
 "L1_TripleMu_5_3p5_2p5_OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17",
 "L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17", "L1_TripleMu_5_5_3",
 "L1_ZeroBias"]

HLTInfo = [
           ['CaloJet40_CaloBTagScouting',        'DST_CaloJet40_CaloBTagScouting_v*'],
           ['CaloScoutingHT250',                 'DST_HT250_CaloScouting_v*'],
           ['CaloBTagScoutingHT250',             'DST_HT250_CaloBTagScouting_v*'],
           ['CaloBTagScoutingL1HTT',             'DST_L1HTT_CaloBTagScouting_v*'],
           ['ZeroBias_CaloScouting_PFScouting',  'DST_ZeroBias_CaloScouting_PFScouting_v*'],
           ['DoubleMu1_noVtx',                   'DST_DoubleMu1_noVtx_CaloScouting_v*'],
           ['DoubleMu3_noVtx',                   'DST_DoubleMu3_noVtx_CaloScouting_v*'],
           ['DoubleMu3_noVtx_Monitoring',        'DST_DoubleMu3_noVtx_CaloScouting_Monitoring_v*'],
           ]


process.triggerMaker = cms.EDProducer("TriggerMaker",
        triggerAlias = cms.vstring(zip(*HLTInfo)[0]),
        triggerSelection = cms.vstring(zip(*HLTInfo)[1]),
        triggerConfiguration = cms.PSet(
            hltResults            = cms.InputTag('TriggerResults','','HLT'),
            l1tResults            = cms.InputTag(''),
            daqPartitions         = cms.uint32(1),
            l1tIgnoreMaskAndPrescale = cms.bool(False),
            throw                 = cms.bool(True),
            ),
        doL1 = cms.bool(True),
        AlgInputTag = cms.InputTag("gtStage2Digis"),
        l1tAlgBlkInputTag = cms.InputTag("gtStage2Digis"),
        l1tExtBlkInputTag = cms.InputTag("gtStage2Digis"),
        ReadPrescalesFromFile = cms.bool(False),
        l1Seeds = cms.vstring(L1Info),
        )

process.load("EventFilter.L1TRawToDigi.gtStage2Digis_cfi")
process.gtStage2Digis.InputLabel = cms.InputTag( "hltFEDSelectorL1" )

process.skimpath = cms.Path(process.countmu * process.countvtx * process.gtStage2Digis * process.triggerMaker)
