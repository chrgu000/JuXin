function psttmValue=PSTTM %计算市销率PS_TTM Price-to-sale
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','Id=a001010100000000');
stocks=w_wset_data(:,2);
totalShares=w.wss(stocks,'total_shares');
dateTem=w.tdays('20150101',today,'Period=Y','Days=Alldays'); % get end day of years
dateTarget=dateTem(end-1); 
priceClose=w.wss(stocks,'close','tradedate',dateTarget);
dateSnap=['rptDate=',datestr(dateTarget,'yyyymmdd')];
operateRevenue=w.wss(stocks,'oper_rev',dateSnap,'rptType=1');
ind=isnan(operateRevenue)<1;
operateRevenue=operateRevenue(ind);
stocksTem=stocks(ind);
totalSharesTem=totalShares(ind);
priceCloseTem=priceClose(ind);
PS_TTM=priceCloseTem./(operateRevenue./totalSharesTem);
psttmValue={stocksTem,PS_TTM};
end