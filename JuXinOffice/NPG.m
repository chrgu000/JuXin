function npgValue=NPG
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','Id=a001010100000000');
stocks=w_wset_data(:,2);
dateTem=w.tdays('20100101',today,'Period=Y','Days=Alldays'); % get end day of years
dateSnap=['rptDate=',datestr(dateTem(end-1),'yyyymmdd')];
netProfit=w.wss(stocks,'net_profit_is',dateSnap,'rptType=1');
ind=~isnan(netProfit);
netProfit=netProfit(ind);
stocks=stocks(ind);
dateSnap=['rptDate=',datestr(dateTem(end-2),'yyyymmdd')];
netProfitPre=w.wss(stocks,'net_profit_is',dateSnap,'rptType=1');
NPG=netProfit./netProfitPre-1;
npgValue={stocks,NPG};
end