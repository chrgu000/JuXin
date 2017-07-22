function pcfttmValue=PCFTTM %计算市现率PCF_TTM Price cash flow ratio;
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','Id=a001010100000000');
stocks=w_wset_data(:,2);
totalShares=w.wss(stocks,'total_shares');
dateTem=w.tdays('20150101',today,'Period=Y','Days=Alldays'); % get end day of years
dateTarget=dateTem(end-1); 
priceClose=w.wss(stocks,'close','tradedate',dateTarget);
dateSnap=['rptDate=',datestr(dateTarget,'yyyymmdd')];
operateProfit=w.wss(stocks,'opprofit',dateSnap,'rptType=1');
ind=isnan(operateProfit)<1;
operateProfit=operateProfit(ind);
stocksTem=stocks(ind);
totalSharesTem=totalShares(ind);
priceCloseTem=priceClose(ind);
PCF_TTM=priceCloseTem./(operateProfit./totalSharesTem);
pcfttmValue={stocksTem,PCF_TTM};
end