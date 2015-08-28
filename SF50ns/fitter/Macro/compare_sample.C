#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TROOT.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TStyle.h"

#include <iostream>

int compare_sample(){

TFile* f1 = new TFile("SmallTnP_trees_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8tnpZ_MC.root","read");

TTree* t1 = (TTree*) f1->Get("tpTree/fitter_tree");
TH1D* probe_pt1 = new TH1D("probe_pt1", "probe_pt1",120, 0, 120);
TH1D* probe_eta1 = new TH1D("probe_eta1", "probe_eta1",48, -2.4, 2.4);
TH1D* tag_pt1 = new TH1D("tag_pt1", "tag_pt1",120, 0, 120);
TH1D* tag_eta1 = new TH1D("tag_eta1", "tag_eta1",48, -2.4, 2.4);

t1->Draw("pt >> probe_pt1");
t1->Draw("eta >> probe_eta1");
t1->Draw("tag_pt >> tag_pt1");
t1->Draw("tag_eta >> tag_eta1");

TFile* f2 = new TFile("SmallTnP_trees_aod74X_DY.root","read");
TTree* t2 = (TTree*) f2->Get("tpTree/fitter_tree");
TH1D* probe_pt2 = new TH1D("probe_pt2", "probe_pt2",120, 0, 120);
TH1D* probe_eta2 = new TH1D("probe_eta2", "probe_eta2",48, -2.4, 2.4);
TH1D* tag_pt2 = new TH1D("tag_pt2", "tag_pt2",120, 0, 120);
TH1D* tag_eta2 = new TH1D("tag_eta2", "tag_eta2",48, -2.4, 2.4);

t2->Draw("pt >> probe_pt2");
t2->Draw("eta >> probe_eta2");
t2->Draw("tag_pt >> tag_pt2");
t2->Draw("tag_eta >> tag_eta2");

gStyle->SetOptStat(0);

TCanvas* c1 = new TCanvas("c1","c1");
probe_pt1->Draw();
probe_pt1->GetXaxis()->SetTitle("Probe p_{T}");
probe_pt1->SetLineColor(2);
probe_pt1->Scale(1./probe_pt1->GetEntries());
probe_pt2->Draw("same");
probe_pt2->SetLineColor(4);
probe_pt2->Scale(1./probe_pt2->GetEntries());

//TLegend* leg1 = new TLegend(0.2, 0.1, 0.5 , 0.3);
//leg1->AddEntry(probe_pt1, "LO MadGraph","LP");
//leg1->AddEntry(probe_pt2, "MadGraph aMC@NLO", "LP");
//leg1->SetBorderSize(0.);
//leg1->SetTextFont(43);
//leg1->SetTextSize(25);
//leg1->Draw();

TCanvas* c2 = new TCanvas("c2","c2");
probe_eta2->Draw();
probe_eta2->GetXaxis()->SetTitle("Probe #eta");
probe_eta1->SetLineColor(2);
probe_eta1->Scale(1./probe_eta1->GetEntries());
probe_eta1->Draw("same");
probe_eta2->SetLineColor(4);
probe_eta2->Scale(1./probe_eta2->GetEntries());
//TLegend* leg2 = new TLegend(0.2, 0.1, 0.5 , 0.3);
//leg2->AddEntry(probe_eta1, "LO MadGraph","LP");
//leg2->AddEntry(probe_eta2, "MadGraph aMC@NLO", "LP");
//leg2->SetBorderSize(0.);
//leg2->SetTextFont(43);
//leg2->SetTextSize(25);
//leg2->Draw();

TCanvas* c3 = new TCanvas("c3","c3");
tag_pt1->Draw();
tag_pt1->GetXaxis()->SetTitle("Tag p_{T}");
tag_pt1->SetLineColor(2);
tag_pt1->Scale(1./tag_pt1->GetEntries());
tag_pt2->Draw("same");
tag_pt2->SetLineColor(4);
tag_pt2->Scale(1./tag_pt2->GetEntries());
//TLegend* leg3 = new TLegend(0.2, 0.1, 0.5 , 0.3);
//leg3->AddEntry(tag_pt1, "LO MadGraph","LP");
//leg3->AddEntry(tag_pt2, "MadGraph aMC@NLO", "LP");
//leg3->SetBorderSize(0.);
//leg3->SetTextFont(43);
//leg3->SetTextSize(25);
//leg3->Draw();

TCanvas* c4 = new TCanvas("c4","c4");
tag_eta2->Draw();
tag_eta2->GetXaxis()->SetTitle("Tag #eta");
tag_eta1->SetLineColor(2);
tag_eta1->Scale(1./tag_eta1->GetEntries());
tag_eta1->Draw("same");
tag_eta2->SetLineColor(4);
tag_eta2->Scale(1./tag_eta2->GetEntries());
//TLegend* leg4 = new TLegend(0.2, 0.1, 0.5 , 0.3);
//leg4->AddEntry(tag_eta1, "LO MadGraph","LP");
//leg4->AddEntry(tag_eta2, "MadGraph aMC@NLO", "LP");
//leg4->SetBorderSize(0.);
//leg4->SetTextFont(43);
//leg4->SetTextSize(25);
//leg4->Draw();

c1->SaveAs("Compariton_plots/c1.pdf");
c2->SaveAs("Compariton_plots/c2.pdf");
c3->SaveAs("Compariton_plots/c3.pdf");
c4->SaveAs("Compariton_plots/c4.pdf");








return 0;


}
