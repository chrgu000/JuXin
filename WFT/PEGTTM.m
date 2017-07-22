function pegttmValue=PEGTTM
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','Id=a001010100000000');
stocks=w_wset_data(:,2);
dateTem=w.tdays('20150101',today,'Period=Y','Days=Alldays'); % get end day of years
dateTarget=dateTem(end-1); 
dateSnap=['rptDate=',datestr(dateTarget,'yyyymmdd')];
netProfit=w.wss(stocks,'net_profit_is',dateSnap,'rptType=1');
ind=isnan(netProfit)<1;
netProfit=netProfit(ind);
dateTargetPre=dateTem(end-2); 
dateSnapPre=['rptDate=',datestr(dateTargetPre,'yyyymmdd')];
stocksTem=stocks(ind);
netProfitPre=w.wss(stocksTem,'net_profit_is',dateSnapPre,'rptType=1');
pettm=PETTM;
PEG_TTM=pettm{2}./(netProfit./netProfitPre);
pegttmValue={stocksTem,PEG_TTM};
end