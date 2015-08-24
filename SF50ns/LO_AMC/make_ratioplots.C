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

//!! To compute SF = MC/Data
TH1F* DividTGraphs(TGraphAsymmErrors* gr1, TGraphAsymmErrors* gr2){

    int nbins = gr1->GetN();
    double xbins[nbins+1];
    cout<<"The number of bins is "<<nbins<<endl;

    for(int i = 0;  i < nbins; ++i){

        Double_t x = 999; 
        Double_t x_hi = 999; 
        Double_t x_low = 999; 
        Double_t y = 999; 
        gr1->GetPoint(i,x,y);
        x_hi = gr1->GetErrorXhigh(i);
        x_low = gr1->GetErrorXlow(i);
        if(i == nbins-1){
            // gr1->GetPoint(i-1,x,y);
            // x_hi = gr1->GetErrorXhigh(i-1);
            xbins[i] = x-x_low;
            xbins[i+1] = x+x_hi;
            cout << "lower edge xbins["<<i<<"]=" << xbins[i] << " y=" << y<< endl;
            cout << "final higher edge xbins["<<i+1<<"]=" <<xbins[i+1] << endl;
        }else{
            xbins[i] = x-x_low;
            cout << "lower edge xbins["<<i<<"]=" << xbins[i] << " y=" << y<< endl;
        }
    }

    TH1F *h1 = new TH1F("h1","h1",nbins,xbins);
    TH1F *h2 = new TH1F("h2","h2",nbins,xbins);

    TGraphAsymmErrors* gr[2] = {gr1, gr2};
    TH1F* h[2] = {h1, h2};

    //Loop over bins to do ratio
    //
    for (int k = 0; k < 2; ++k){
        for(int i = 0;  i < nbins+1; ++i){
            //
            //TGraph
            //
            Double_t num_x = 999; 
            Double_t num_y = 999; 
            Double_t num_y_hi = 999; 
            Double_t num_y_low = 999; 

            gr[k]->GetPoint(i,num_x,num_y);
            //std::cout<<"num x "<<i<<" is"<<num_x<<std::endl;
            //std::cout<<"num y "<<i<<" is"<<num_y<<std::endl;
            num_y_hi = gr[k]->GetErrorYhigh(i);
            num_y_low = gr[k]->GetErrorYlow(i);

            double max_error = max(num_y_hi,num_y_low);

            //Convert into TH1D
            h[k]->SetBinContent(h[k]->FindBin(num_x), num_y);
            h[k]->SetBinError(h[k]->FindBin(num_x), max_error);
            //std::cout<<"the bin number "<<i<<"was filled with"<<num_y<<std::endl;
            //std::cout<<"the bin number "<<i<<" of th is "<<h[k]->GetBinContent(h[k]->FindBin(num_x))<<std::endl;

        }
    }
    //ratio histogram
    h[0]->Divide(h[1]);

    return h[0]; 

}


void make_ratioplots(TString _file, TString _canvas, TString _path1, TString _path2, TString _output){

    setTDRStyle();
    gROOT->SetBatch(kTRUE);


    TString _par = "";
    if(_canvas.Contains("pt_PLOT_abseta_bin0")){_par = "_abseta_bin0";}
    else if(_canvas.Contains("pt_PLOT_abseta_bin1")){_par = "_abseta_bin1";}

    cout<<_file<<endl;
    //TFile *f1 = TFile::Open("DATAeff_app2MC1/" + _file);
    TFile *f1 = TFile::Open(_path1 + _file);
    TCanvas* c1 = (TCanvas*) f1->Get(_canvas);
    TGraphAsymmErrors* eff1 = (TGraphAsymmErrors*)c1->GetPrimitive("hxy_fit_eff");
    //TFile *f2 = TFile::Open("MCeff_app2MC1/" + _file);
    TFile *f2 = TFile::Open(_path2 + _file);
    TCanvas* c2 = (TCanvas*) f2->Get(_canvas);
    TGraphAsymmErrors* eff2 = (TGraphAsymmErrors*)c2->GetPrimitive("hxy_fit_eff");

    TH1F* ratio = DividTGraphs(eff1, eff2);
    ratio->SetStats(0);

    int nbins = eff1->GetN();
    double x,y;
    eff1->GetPoint(0,x,y);
    double x_low = x-eff1->GetErrorXlow(0);
    eff1->GetPoint(nbins-1,x,y);
    double x_hi = x+eff1->GetErrorXhigh(nbins-1);

    TCanvas* c3 = new TCanvas("c3","c3");
    //c3->UseCurrentStyle();
    TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1->SetBottomMargin(0.); 
    pad1->SetTopMargin(0.1); 
    pad1->Draw();
    pad1->cd();
    //c3->Divide(1,2);
    //c3->cd(1);
    eff1->Draw("AP");
    eff1->SetTitle("");
    eff1->GetYaxis()->SetTitle("Efficiency");
    eff1->GetXaxis()->SetRangeUser(x_low, x_hi);
    eff1->GetXaxis()->SetLabelOffset(999);
    eff1->GetXaxis()->SetLabelSize(0);
    TString _xtitle = eff1->GetXaxis()->GetTitle();
    if(_xtitle.Contains("tag_nVertices")){_xtitle = "N(primary vertices)";
    }else if (_xtitle.Contains("eta")){_xtitle = "muon #eta";
    }else if (_xtitle.Contains("pt")){_xtitle = "muon p_{t} [GeV]";}
    eff1->GetXaxis()->SetTitle(_xtitle);
    TString _title = eff1->GetXaxis()->GetTitle();
    eff1->GetXaxis()->SetTitle("");
    //eff1->GetYaxis()->SetRangeUser(0.8001, 1.05);
    eff1->GetYaxis()->SetRangeUser(0.79, 1.1);
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
    //TString _legtext = "";
    //if(_xtitle.Contains("eta")){_legtext = "#mu p_{t} #geq 22 [GeV]";} 
    TLegend* leg = new TLegend(0.2, 0.05, 0.5 , 0.25);
    //leg->AddEntry((TObject*)0, _legtext, "");
    //leg->AddEntry((TObject*)0, "", "");
    //leg->SetHeader("Loose ID, p_{T} #geq 22 GeV");
    //leg->SetHeader("Tight ID, p_{T} #geq 20 GeV");
    leg->SetHeader("p_{T} #geq 20 GeV");
    TLegendEntry *header = (TLegendEntry*)leg->GetListOfPrimitives()->First();
    //header->SetTextAlign(22);
    header->SetTextColor(1);
    header->SetTextFont(43);
    header->SetTextSize(20);
    leg->AddEntry(eff1, "Data", "LP");
    leg->AddEntry(eff2, "MC","LP");
    //leg->AddEntry(eff1, "MadGraph aMC@NLO", "LP");
    //leg->AddEntry(eff2, "LO MadGraph","LP");
    leg->SetBorderSize(0.);
    leg->SetTextFont(43);
    leg->SetTextSize(20);
    leg->Draw();
    _file.ReplaceAll("root","pdf");
    TGaxis *axis = new TGaxis( -5, 20, -5, 220, 20,220,510,"");
    axis->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    axis->SetLabelSize(15);
    axis->Draw();

    c3->cd();
    TPad *pad2 = new TPad("pad2", "pad2", 0, 0., 1, 0.3);
    pad2->SetTopMargin(0.0); 
    pad2->SetBottomMargin(0.35); 
    pad2->SetGridy(); 
    pad2->Draw();
    pad2->cd();
    ratio->SetTitle("");
    ratio->SetLineWidth(2);
    ratio->SetLineColor(1);
    ratio->SetMarkerStyle(20);
    ratio->SetMarkerColor(1);
    //ratio->GetYaxis()->SetRangeUser(0.9,1.0999);
    ratio->GetYaxis()->SetRangeUser(0.95,1.04999);
    //ratio->GetYaxis()->SetRangeUser(0.98,1.01999);
    ratio->GetYaxis()->SetTitle("Data/MC");
    //ratio->GetYaxis()->SetTitle("aMC@NLO/LO");
    ratio->GetYaxis()->SetNdivisions(505);
    ratio->GetYaxis()->SetLabelSize(20);
    ratio->GetYaxis()->SetTitleFont(63);
    ratio->GetYaxis()->SetTitleOffset(1.5);
    ratio->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    ratio->GetYaxis()->SetTitleSize(27);
    ratio->GetXaxis()->SetTitleSize(27);
    ratio->GetXaxis()->SetLabelSize(20);
    ratio->GetXaxis()->SetTitle(_title);
    ratio->GetXaxis()->SetTitleFont(63);
    ratio->GetXaxis()->SetTitleSize(27);
    ratio->GetXaxis()->SetTitleOffset(3);
    ratio->GetXaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    ratio->Draw();
    CMS_lumi(pad1, 4, 11);
    c3->Update();

    c3->SaveAs(_output + _par + "_" + _file);

    //c3->RedrawAxis();
    //c3->GetFrame()->Draw();


    //TFile *f_out = TFile::Open("TEST.root","recreate");
    //f_out->cd();
    //c3->Write();

}

