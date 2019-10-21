#ifndef NTUPLEMAKER_TRIGGERMAKER_H
#define NTUPLEMAKER_TRIGGERMAKER_H

// system include files
#include <memory>
#include <iostream>
#include <vector>
#include <string>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "HLTrigger/HLTcore/interface/TriggerExpressionData.h"
#include "HLTrigger/HLTcore/interface/TriggerExpressionEvaluator.h"
#include "HLTrigger/HLTcore/interface/TriggerExpressionParser.h"
#include "L1Trigger/L1TGlobal/interface/L1TGlobalUtil.h"


//
// class decleration
//

class TriggerMaker : public edm::stream::EDProducer<> {
public:
     explicit TriggerMaker (const edm::ParameterSet&);
     ~TriggerMaker();

private:
     virtual void beginJob() ;
     virtual void produce(edm::Event&, const edm::EventSetup&);
     virtual void endJob() ;
     virtual void beginRun(const edm::Run&, const edm::EventSetup&);

    triggerExpression::Data triggerCache_;
    std::vector<triggerExpression::Evaluator*> vtriggerSelector_;
    std::vector<std::string> vtriggerAlias_, vtriggerSelection_;
    bool doL1_;

    edm::EDGetToken algToken_;
    l1t::L1TGlobalUtil *l1GtUtils_;
    std::vector<std::string> l1Seeds_;


};

#endif

