function pettmValue=PETTM(varargin) % º∆À„ –”Ø¬ PE_TTM Price earnings ratio
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','Id=a001010100000000');
stocks=w_wset_data(:,2);
totalShares=w.wss(stocks,'total_shares');
if nargin==0
    dateTem=w.tdays('20100101',today,'Period=Y','Days=Alldays'); % get end day of years
else
    dateTem=w.tdays('20100101',varargin{1},'Period=Y','Days=Alldays');
end
dateTarget=dateTem(end-1); 
priceClose=w.wss(stocks,'close','tradedate',dateTarget);
dateSnap=['rptDate=',datestr(dateTarget,'yyyymmdd')];
netProfit=w.wss(stocks,'net_profit_is',dateSnap,'rptType=1');
ind=isnan(netProfit)<1;
netProfit=netProfit(ind);
stocksTem=stocks(ind);
totalSharesTem=totalShares(ind);
priceCloseTem=priceClose(ind);
PE_TTM=priceCloseTem./(netProfit./totalSharesTem);
pettmValue={stocksTem,PE_TTM};
end