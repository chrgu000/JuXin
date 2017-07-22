function opgValue=OPG
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','Id=a001010100000000');
stocks=w_wset_data(:,2);
dateTem=w.tdays('20100101',today,'Period=Y','Days=Alldays'); % get end day of years
dateSnap=['rptDate=',datestr(dateTem(end-1),'yyyymmdd')];
operateProfit=w.wss(stocks,'opprofit',dateSnap,'rptType=1');
ind=~isnan(operateProfit);
operateProfit=operateProfit(ind);
stocks=stocks(ind);
dateSnap=['rptDate=',datestr(dateTem(end-2),'yyyymmdd')];
operateProfitPre=w.wss(stocks,'opprofit',dateSnap,'rptType=1');
OPG=operateProfit./operateProfitPre-1;
opgValue={stocks,OPG};
end