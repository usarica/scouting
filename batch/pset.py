import FWCore.ParameterSet.Config as cms

process = cms.Process('SLIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')



process.maxEvents = cms.untracked.PSet(
    # input = cms.untracked.int32(-1)
    input = cms.untracked.int32(10000)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(True),
    fileNames = cms.untracked.vstring('file:/hadoop/cms/store/user/namin/nanoaod/ScoutingCaloMuon__Run2018C-v1/6A94C331-F38D-E811-B4D7-FA163E146D61.root'),
    # fileNames = cms.untracked.vstring('/store/data/Run2018B/ScoutingCaloMuon/RAW/v1/000/317/696/00000/761E614C-156E-E811-B5AA-FA163E373C99.root'),
    inputCommands = cms.untracked.vstring(
        'keep *', 
        'drop *_hltScoutingTrackPacker_*_*', 
        # 'drop *_hltFEDSelectorL1_*_*', 
        # 'drop *_TriggerResults_*_*', 
    ),
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:output.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('skimpath'),
        ),
    outputCommands = cms.untracked.vstring(),
)
process.outpath = cms.EndPath(process.out)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
# process.MessageLogger.cerr.FwkReport.reportEvery = 500

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

# original line
process.skimpath = cms.Path(process.countmu + process.countvtx)

# NOTE random stuff below

# process.patTrigger = cms.EDProducer("PATTriggerProducer",
#     ReadPrescalesFromFile = cms.bool(False),
#     # l1GtReadoutRecordInputTag = cms.InputTag("gtDigis"),
#     # l1GtRecordInputTag = cms.InputTag("gtDigis"),
#     # l1GtTriggerMenuLiteInputTag = cms.InputTag("gtDigis"),
#     l1tAlgBlkInputTag = cms.InputTag("gtStage2Digis"),
#     l1tExtBlkInputTag = cms.InputTag("gtStage2Digis"),
#     onlyStandAlone = cms.bool(True),
#     packTriggerLabels = cms.bool(False),
#     packTriggerPathNames = cms.bool(True),
#     processName = cms.string('HLT')
# )

# # WORKS NOTE
# process.load('Configuration.StandardSequences.RawToDigi_cff')

# # WORKS NOTE
# process.load("EventFilter.L1TRawToDigi.gtStage2Digis_cfi")
# process.gtStage2Digis.InputLabel = cms.InputTag( "hltFEDSelectorL1" )
# # from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
# # process.l1stuff = cms.Path()
# # switchOnTrigger( process, path = 'l1stuff' )
# # process.skimpath = cms.Path(process.countmu + process.countvtx + process.l1stuff._seq)
# # from PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi import patTrigger
# # print(patTrigger)
# # process.load("L1Trigger.L1TGlobal.TriggerMenu_cff")
# # process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi")
# # from L1Trigger.Configuration.L1TRawToDigi_cff import *
# # from EventFilter.ScalersRawToDigi.ScalersRawToDigi_cfi import *
# # process.RawToDigi = cms.Sequence(L1TRawToDigi
# #                          +scalersRawToDigi
# #                          )
# # process.skimpath = cms.Path(process.countvtx + process.countmu + process.gtStage2Digis + process.RawToDigi + process.patTrigger)
# # process.skimpath = cms.Path(process.countvtx + process.countmu + process.gtStage2Digis + process.patTrigger)
# process.skimpath = cms.Path(process.countvtx + process.countmu + process.gtStage2Digis) # + process.patTrigger)
# # process.skimpath = cms.Path(process.countvtx + process.countmu)
# print(dir(process))
# print(process.skimpath)
# print(process.skimpath._seq)
# # print(process.l1stuff)
# # print(process.l1stuff._seq)

## 
#process.load("EventFilter.L1TRawToDigi.gtStage2Digis_cfi")
## process.load("EventFilter.L1TRawToDigi.gtStage2Digis_cfi")
#process.load("L1Trigger.Configuration.L1TRawToDigi_cff")
#print(process.L1TRawToDigi.dumpPython())
#print(process.L1TRawToDigi._seq.dumpSequencePython())
#process.gtStage2Digis.InputLabel = cms.InputTag( "hltFEDSelectorL1" )
## from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
#process.skimpath = cms.Path(process.countmu + process.countvtx + process.L1TRawToDigi + process.gtStage2Digis + process.patTrigger)
## help(switchOnTrigger)
## switchOnTrigger( process, path = 'skimpath' )
#print(process.skimpath)

# # import of standard configurations
# process.load('Configuration.EventContent.EventContent_cff')
# process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
# process.load('Configuration.StandardSequences.MagneticField_38T_cff')
# process.load('Configuration.StandardSequences.RawToDigi_cff')
# process.load('Configuration.StandardSequences.EndOfProcess_cff')
# process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# process.load("L1TriggerConfig.L1ScalesProducers.L1MuScalesRecords_cff")
# process.load("EventFilter.L1TRawToDigi.gtStage2Digis_cfi")
# process.load("EventFilter.L1GlobalTriggerRawToDigi.l1GtRecord_cfi")
# process.load("EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi")
# print(process.gtStage2Digis.dumpPython())
# print(process.l1GtRecord.dumpPython())
# print(process.l1GtUnpack.dumpPython())
# process.gtStage2Digis.InputLabel = cms.InputTag( "hltFEDSelectorL1" )
# process.skimpath = cms.Path(process.countvtx + process.countmu +
#         process.l1GtUnpack + process.l1GtRecord + 
#         process.gtStage2Digis) # + process.patTrigger)
# print(process.skimpath)


