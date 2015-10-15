#include "TString.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"
#include "TAxis.h"
#include "TGaxis.h"
#include "TH1F.h"
#include "TROOT.h"
#include "TLegend.h"
#include "TGaxis.h"
#include "tdrstyle.C"
#include "CMS_lumi.C"
#include "TLegendEntry.h"

#include <iostream>

int make_dataplots(TString _file, TString _canvas, TString _path1, TString _path2, TString _output, TString _comparison){

    setTDRStyle();
    gROOT->SetBatch(kTRUE);


    TString _par = "";
    if(_canvas.Contains("pt_PLOT_abseta_bin0")){_par = "abseta_bin0";}
    else if(_canvas.Contains("pt_PLOT_abseta_bin1")){_par = "abseta_bin1";}

    //cout<<_file<<endl;
    TFile *f1 = TFile::Open(_path1 + _file);
    TCanvas* c1 = (TCanvas*) f1->Get(_canvas);
    TGraphAsymmErrors* eff1 = (TGraphAsymmErrors*)c1->GetPrimitive("hxy_fit_eff");
    TFile *f2 = TFile::Open(_path2 + _file);
    TCanvas* c2 = (TCanvas*) f2->Get(_canvas);
    TGraphAsymmErrors* eff2 = (TGraphAsymmErrors*)c2->GetPrimitive("hxy_fit_eff");
    TFile *f3 = TFile::Open(_path3 + _file);
    TCanvas* c4 = (TCanvas*) f3->Get(_canvas);
    TGraphAsymmErrors* eff3 = (TGraphAsymmErrors*)c4->GetPrimitive("hxy_fit_eff");

    int nbins = eff1->GetN();
    double x,y;
    eff1->GetPoint(0,x,y);
    double x_low = x-eff1->GetErrorXlow(0);
    eff1->GetPoint(nbins-1,x,y);
    double x_hi = x+eff1->GetErrorXhigh(nbins-1);

    TCanvas* c3 = new TCanvas("c3","c3");
    eff1->Draw("AP");
    eff1->SetTitle("");
    TString _xtitle = eff1->GetXaxis()->GetTitle();
    if(_xtitle.Contains("tag_nVertices")){_xtitle = "N(primary vertices)";
    }else if (_xtitle.Contains("eta")){_xtitle = "muon #eta";
    }else if (_xtitle.Contains("pt")){_xtitle = "muon p_{t} [GeV]";}
    eff1->GetXaxis()->SetTitle(_xtitle);
    eff1->GetYaxis()->SetTitle("Efficiency");
    eff1->GetXaxis()->SetRangeUser(x_low, x_hi);
    eff1->GetXaxis()->SetTitleSize(27);
    eff1->GetXaxis()->SetTitleFont(63);
    eff1->GetXaxis()->SetLabelFont(43);
    eff1->GetXaxis()->SetLabelSize(20);
    //eff1->GetYaxis()->SetRangeUser(0.8001, 1.05);
    eff1->GetYaxis()->SetRangeUser(0.8, 1.1);
    eff1->GetYaxis()->SetTitleSize(27);
    eff1->GetYaxis()->SetTitleFont(63);
    eff1->GetYaxis()->SetLabelFont(43);
    eff1->SetMarkerStyle(20);
    eff1->GetYaxis()->SetLabelSize(20);
    eff1->GetYaxis()->SetTitleOffset(1.5);
    eff2->Draw("P");
    eff2->SetLineColor(4);
    eff2->SetMarkerStyle(21);
    eff2->SetMarkerColor(4);
    eff3->Draw("P");
    eff3->SetLineColor(2);
    eff3->SetMarkerColor(2);
    eff3->SetMarkerStyle(22);
    TString _legtext = "";

    if(_canvas.Contains("/Loose_noIP_eta")){
        _legtext = "Loose Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/Loose_noIP_vtx_bin")){
        _legtext = "Loose Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/Loose_noIP_pt_alleta_bin")){
        _legtext = "Loose Id, #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/Loose_noIP_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin0")){
        _legtext = "Loose Id, #||{#eta} #leq 1.2";
    }else if(_canvas.Contains("/Loose_noIP_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin1")){
        _legtext = "Loose Id, 1.2 < #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/Medium_noIP_eta")){
        _legtext = "Medium Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/Medium_noIP_vtx_bin")){
        _legtext = "Medium Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/Medium_noIP_pt_alleta_bin")){
        _legtext = "Medium Id, #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/Medium_noIP_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin0")){
        _legtext = "Medium Id, #||{#eta} #leq 1.2";
    }else if(_canvas.Contains("/Medium_noIP_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin1")){
        _legtext = "Medium Id, 1.2 < #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/Tight2012_zIPCut_eta")){
        _legtext = "Tight Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/Tight2012_zIPCut_vtx_bin")){
        _legtext = "Tight Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/Tight2012_zIPCut_pt_alleta_bin")){
        _legtext = "Tight Id, #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/Tight2012_zIPCut_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin0")){
        _legtext = "Tight Id, #||{#eta} #leq 1.2";
    }else if(_canvas.Contains("/Tight2012_zIPCut_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin1")){
        _legtext = "Tight Id, 1.2 < #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/LooseIso4_loose_eta")){
        _legtext = "Loose Iso/Loose Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/LooseIso4_loose_vtx_bin")){
        _legtext = "Loose Iso/Loose Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/LooseIso4_loose_pt_alleta_bin")){
        _legtext = "Loose Iso/Loose Id, #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/LooseIso4_loose_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin0")){
        _legtext = "Loose Iso/Loose Id, #||{#eta} #leq 1.2";
    }else if(_canvas.Contains("/LooseIso4_loose_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin1")){
        _legtext = "Loose Iso/Loose Id, 1.2 < #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/LooseIso4_medium_eta")){
        _legtext = "Loose Iso/Medium Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/LooseIso4_medium_vtx_bin")){
        _legtext = "Loose Iso/Medium Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/LooseIso4_medium_pt_alleta_bin")){
        _legtext = "Loose Iso/Medium Id, #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/LooseIso4_medium_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin0")){
        _legtext = "Loose Iso/Medium Id, #||{#eta} #leq 1.2";
    }else if(_canvas.Contains("/LooseIso4_medium_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin1")){
        _legtext = "Loose Iso/Medium Id, 1.2 < #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/LooseIso4_tightip_eta")){
        _legtext = "Loose Iso/Tight Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/LooseIso4_tightip_vtx_bin")){
        _legtext = "Loose Iso/Tight Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/LooseIso4_tightip_pt_alleta_bin")){
        _legtext = "Loose Iso/Tight Id, #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/LooseIso4_tightip_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin0")){
        _legtext = "Loose Iso/Tight Id, #||{#eta} #leq 1.2";
    }else if(_canvas.Contains("/LooseIso4_tightip_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin1")){
        _legtext = "Loose Iso/Tight Id, 1.2 < #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/TightIso4_loose_eta")){
        _legtext = "Tight Iso/Loose Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/TightIso4_loose_vtx_bin")){
        _legtext = "Tight Iso/Loose Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/TightIso4_loose_pt_alleta_bin")){
        _legtext = "Tight Iso/Loose Id, #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/TightIso4_loose_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin0")){
        _legtext = "Tight Iso/Loose Id, #||{#eta} #leq 1.2";
    }else if(_canvas.Contains("/TightIso4_loose_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin1")){
        _legtext = "Tight Iso/Loose Id, 1.2 < #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/TightIso4_tightip_eta")){
        _legtext = "Tight Iso/Tight Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/TightIso4_tightip_vtx_bin")){
        _legtext = "Tight Iso/Tight Id, p_{T} #geq 20 GeV";
    }else if(_canvas.Contains("/TightIso4_tightip_pt_alleta_bin")){
        _legtext = "Tight Iso/Tight Id, #||{#eta} #leq 2.4";
    }else if(_canvas.Contains("/TightIso4_tightip_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin0")){
        _legtext = "Tight Iso/Tight Id, #||{#eta} #leq 1.2";
    }else if(_canvas.Contains("/TightIso4_tightip_pt_spliteta_bin") && _canvas.Contains("pt_PLOT_abseta_bin1")){
        _legtext = "Tight Iso/Tight Id, 1.2 < #||{#eta} #leq 2.4";
    }else{
        std::cout<<"=============================="<<std::endl;
        std::cout<<"ERROR: No corresponding legend"<<std::endl;
        std::cout<<"=============================="<<std::endl;
        //return 1;
    }
    TLegend* leg = new TLegend(0.45, 0.70, 0.75 , 0.9);
    leg->SetHeader(_legtext);
    TLegendEntry *header = (TLegendEntry*)leg->GetListOfPrimitives()->First();
    //header->SetTextAlign(22);
    header->SetTextColor(1);
    header->SetTextFont(43);
    header->SetTextSize(20);
    //leg->AddEntry(eff1, "2015B, 50ns", "LP");
    //leg->AddEntry(eff2, "2015C, 50ns","LP");
    //leg->AddEntry(eff3, "2015C, 25ns","LP");
    leg->SetBorderSize(0.);
    leg->SetTextFont(43);
    leg->SetTextSize(20);
    leg->Draw();
    _file.ReplaceAll("root","pdf");
    TGaxis *axis = new TGaxis( -5, 20, -5, 220, 20,220,510,"");
    axis->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    axis->SetLabelSize(15);
    axis->Draw();

    CMS_lumi(c3, 5, 11);
    c3->Update();

    c3->SaveAs(_output + _par + "_" + _file);

    //TFile *f_out = TFile::Open("TEST.root","recreate");
    //f_out->cd();
    //c3->Write();

    return 0;

}

