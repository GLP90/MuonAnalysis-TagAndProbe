//_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*
//Copy a TTree with a smaller number of events
//_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*

#include "TFile.h"
#include "TTree.h"

int GetSmallerTree(){

	//input
	TFile* f_in = new TFile("/afs/cern.ch/work/g/gaperrin/private/TnP/TnP_v3/CMSSW_7_4_10/src/MuonAnalysis/TagAndProbe/test/zmumu/mu_POG/50nsfinal/TnP_trees_aod747_DY_amcatnlo_50ns_withFixes.root","read");
	TTree* t_in = (TTree*)f_in->Get("tpTree/fitter_tree");

	//output
	TFile* f_out = new TFile("SmallTree.root","recreate");
	f_out->mkdir("tpTree");
	f_out->cd("tpTree");
	TTree* t_out = t_in->CloneTree(0);

	for (Int_t i=0;i<1000000; i++) {
		t_in->GetEntry(i);
		t_out->Fill();
	}
	t_out->Print();
	t_out->AutoSave();
	delete f_in;
	delete f_out;

	return 0;

}
