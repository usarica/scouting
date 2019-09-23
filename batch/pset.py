import FWCore.ParameterSet.Config as cms

process = cms.Process('SLIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.maxEvents = cms.untracked.PSet(
    # input = cms.untracked.int32(-1)
    input = cms.untracked.int32(50000)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(True),
    # fileNames = cms.untracked.vstring('file:/hadoop/cms/store/user/namin/nanoaod/ScoutingCaloMuon__Run2018C-v1/7E15C500-338E-E811-9848-FA163E2B0A7A.root'),
    fileNames = cms.untracked.vstring('/store/data/Run2018B/ScoutingCaloMuon/RAW/v1/000/317/696/00000/761E614C-156E-E811-B5AA-FA163E373C99.root'),
    inputCommands = cms.untracked.vstring(
        'keep *', 
        'drop *_hltScoutingTrackPacker_*_*', 
        'drop *_hltFEDSelectorL1_*_*', 
        'drop *_TriggerResults_*_*', 
    ),
)

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
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

process.skimpath = cms.Path(process.countmu + process.countvtx)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:output.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('skimpath'),
        ),
    # outputCommands = outputCommands,
)
process.outpath = cms.EndPath(process.out)
