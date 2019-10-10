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
