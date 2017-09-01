function EarningsyieldValue=EarningsYieldX
w=windmatlab;
% w_wset_data=w.wset('SectorConstituent','date=20170118;sectorId=a001010100000000');
w_wset_data=w.wset('SectorConstituent','a001010100000000');
x_stock=w_wset_data(:,2);
dateTem=w.tdays('20150101',today,'Period=Y','Days=Alldays');
if sum(dateTem{end}(end-1:end)=='31')==2
    dateTem0=dateTem{end};
else
    dateTem0=dateTem{end-1};
end
data=w.wss(x_stock,'ev,net_profit_is',strcat('rptDate=',dateTem0),'rptType=1');
indexTem=sum(isnan(data),2)==0;
data=data(indexTem,:);
x_stock=x_stock(indexTem);
ETOP=data(:,2)./data(:,1);
dateTem1=dateTem{end}(1:4);
data=w.wss(x_stock,'west_medianeps,cfps_ttm',strcat('year=',dateTem1),'westPeriod=180');
indexTem=sum(isnan(data),2)==0;
data=data(indexTem,:);
x_stock=x_stock(indexTem);
ETOP=ETOP(indexTem);
priceClose=w.wss(x_stock,'close','priceAdj=F');
EPIBS=data(:,1)./priceClose;% one columne array;
CETOP=data(:,2)./priceClose; % one columne array;

Value=0.68*EPIBS+0.11*ETOP+0.21*CETOP;
EarningsyieldValue={x_stock,Value};
save EarningsYield EarningsyieldValue;
end

