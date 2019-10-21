#include "Scouting/NtupleMaker/plugins/TriggerMaker.h" 
#include "TMath.h"

using namespace edm;
using namespace std;

TriggerMaker::TriggerMaker(const edm::ParameterSet& iConfig) {

    produces<std::vector<std::string> >       ("l1name"         ).setBranchAlias("l1_name"          );
    produces<std::vector<bool> >       ("l1result"         ).setBranchAlias("l1_result"          );
    produces<std::vector<int> >       ("l1prescale"         ).setBranchAlias("l1_prescale"          );

    produces<std::vector<std::string> >       ("hltname"         ).setBranchAlias("hlt_name"          );
    produces<std::vector<bool> >       ("hltresult"         ).setBranchAlias("hlt_result"          );

    triggerCache_ = triggerExpression::Data(iConfig.getParameterSet("triggerConfiguration"),consumesCollector());
    vtriggerAlias_ = iConfig.getParameter<vector<string>>("triggerAlias");
    vtriggerSelection_ = iConfig.getParameter<vector<string>>("triggerSelection");

    doL1_ = iConfig.getParameter<bool>("doL1");

    vtriggerSelector_.clear();
    for (unsigned i=0; i<vtriggerSelection_.size(); ++i) {
        vtriggerSelector_.push_back(triggerExpression::parse(vtriggerSelection_[i]));
    }

    if (doL1_) {
        algToken_ = consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<InputTag>("AlgInputTag"));
        l1Seeds_ = iConfig.getParameter<std::vector<std::string> >("l1Seeds");
        l1GtUtils_ = new l1t::L1TGlobalUtil(iConfig,consumesCollector());
    }
    else {
        l1Seeds_ = std::vector<std::string>();
        l1GtUtils_ = 0;
    }

}

TriggerMaker::~TriggerMaker()
{
}

void  TriggerMaker::beginJob()
{
}

void TriggerMaker::endJob()
{
    for (unsigned i=0; i<vtriggerSelector_.size(); ++i) {
        delete vtriggerSelector_[i];
    }
}

void TriggerMaker::beginRun(const edm::Run& iRun, const edm::EventSetup& iSetup) {
}

// ------------ method called to produce the data  ------------
void TriggerMaker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    unique_ptr<vector<string> >                 l1_name          (new vector<string>                );
    unique_ptr<vector<bool> >                 l1_result          (new vector<bool>                );
    unique_ptr<vector<int> >                 l1_prescale          (new vector<int>                );

    unique_ptr<vector<string> >                 hlt_name          (new vector<string>                );
    unique_ptr<vector<bool> >                 hlt_result          (new vector<bool>                );

    if (triggerCache_.setEvent(iEvent, iSetup)) {
        for(unsigned itrig=0; itrig<vtriggerSelector_.size(); ++itrig) {
            bool result = false;
            if (vtriggerSelector_[itrig]) {
                if (triggerCache_.configurationUpdated()) {
                    vtriggerSelector_[itrig]->init(triggerCache_);
                }
                result = (*(vtriggerSelector_[itrig]))(triggerCache_);
            }
            hlt_result->push_back(result);
            hlt_name->push_back(vtriggerAlias_[itrig]);
        }
    }

    if (doL1_) {
        l1GtUtils_->retrieveL1(iEvent,iSetup,algToken_);
        for( unsigned int iseed = 0; iseed < l1Seeds_.size(); iseed++ ) {
            bool l1htbit = 0;
            int prescale = -1;
            l1GtUtils_->getFinalDecisionByName(l1Seeds_[iseed], l1htbit);
            l1GtUtils_->getPrescaleByName(l1Seeds_[iseed], prescale);
            l1_result->push_back( l1htbit );
            l1_name->push_back( l1Seeds_[iseed] );
            l1_prescale->push_back(prescale);
        }
    }
    
    iEvent.put(std::move(l1_name             ), "l1name"         );
    iEvent.put(std::move(l1_result             ), "l1result"         );
    iEvent.put(std::move(l1_prescale             ), "l1prescale"         );
    iEvent.put(std::move(hlt_name             ), "hltname"         );
    iEvent.put(std::move(hlt_result             ), "hltresult"         );

}

DEFINE_FWK_MODULE(TriggerMaker);
