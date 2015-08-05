#include "TString.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"
#include "TAxis.h"
#include "TGaxis.h"
#include "TH1F.h"
#include "TROOT.h"
#include "TLegend.h"

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
    // for(int i=0; i<=nbins; i++){
    // std::cout<<"The bound "<<i<<" is "<<xbins[i] << std::endl;
    // }

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


void make_ratioplots2(TString _file = "TnP_MuonID_data_all_Tight_noIP_vtx.root", TString _canvas = "tpTree/Tight_noIP_vtx/fit_eff_plots/tag_nVertices_PLOT_tag_IsoMu20_pass"){

    TString _par = "";
    if(_canvas.Contains("pt_PLOT_abseta_bin0")){_par = "_abseta_bin0";}
    else if(_canvas.Contains("pt_PLOT_abseta_bin1")){_par = "_abseta_bin1";}

    cout<<_file<<endl;
    TFile *f1 = TFile::Open("DATAeff4/" + _file);
    TCanvas* c1 = (TCanvas*) f1->Get(_canvas);
    TGraphAsymmErrors* eff1 = (TGraphAsymmErrors*)c1->GetPrimitive("hxy_fit_eff");
    TFile *f2 = TFile::Open("MCeff4/" + _file);
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

    TCanvas* c3 = new TCanvas("c3","c3",800,800);
    //c3->UseCurrentStyle();
    TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1->SetBottomMargin(0.02); 
    pad1->Draw();
    pad1->cd();
    //c3->Divide(1,2);
    //c3->cd(1);
    eff1->Draw("AP");
    eff1->GetYaxis()->SetTitle("Efficiency");
    eff1->GetXaxis()->SetRangeUser(x_low, x_hi);
    eff1->GetXaxis()->SetLabelOffset(999);
    eff1->GetXaxis()->SetLabelSize(0);
    TString _title = eff1->GetXaxis()->GetTitle();
    eff1->GetXaxis()->SetTitle("");
    eff1->GetYaxis()->SetRangeUser(0.8, 1.05);
    eff1->GetYaxis()->SetTitleSize(20);
    eff1->GetYaxis()->SetTitleFont(63);
    eff1->GetYaxis()->SetTitleOffset(2);
    eff2->Draw("P");
    eff2->SetLineColor(4);
    eff2->SetMarkerColor(4);
    TLegend* leg = new TLegend(0.7, 0.8, 0.9 , 0.9);
    leg->AddEntry(eff1, "Data", "LP");
    leg->AddEntry(eff2, "MC","LP");
    leg->SetBorderSize(0.);
    leg->SetTextFont(43);
    leg->SetTextSize(25);
    leg->SetBorderSize(1);
    leg->Draw();
    _file.ReplaceAll("root","pdf");

    c3->cd();
    TPad *pad2 = new TPad("pad2", "pad2", 0, 0., 1, 0.3);
    pad2->SetTopMargin(0.05); 
    pad2->SetBottomMargin(0.2); 
    pad2->SetGridy(); 
    pad2->Draw();
    pad2->cd();
    ratio->SetTitle("");
    ratio->SetLineWidth(2);
    ratio->SetLineColor(1);
    ratio->SetMarkerStyle(20);
    ratio->SetMarkerColor(1);
    ratio->GetYaxis()->SetRangeUser(0.9,1.1);
    ratio->GetYaxis()->SetTitle("SF (Data/MC) ");
    ratio->GetYaxis()->SetNdivisions(505);
    ratio->GetYaxis()->SetTitleSize(20);
    ratio->GetYaxis()->SetLabelSize(20);
    ratio->GetYaxis()->SetTitleFont(63);
    ratio->GetYaxis()->SetTitleOffset(1.55);
    ratio->GetYaxis()->SetLabelFont(63); // Absolute font size in pixel (precision 3)
    ratio->GetXaxis()->SetTitleSize(25);
    ratio->GetXaxis()->SetLabelSize(20);
    ratio->GetXaxis()->SetTitle(_title);
    ratio->GetXaxis()->SetTitleFont(63);
    ratio->GetXaxis()->SetTitleOffset(2.5);
    ratio->GetXaxis()->SetLabelFont(63); // Absolute font size in pixel (precision 3)
    ratio->Draw();
    //c3->SaveAs("RatioPlots3/"+_par+"_"+_file);
    c3->SaveAs("RatioPlots4/"+_par+"_"+_file);
    //c3->SaveAs("TEST"+_file);

    //TFile *f_out = TFile::Open("TEST.root","recreate");
    //f_out->cd();
    //c3->Write();

}

