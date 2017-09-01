function growthValue=GrowthX
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','a001010100000000');
x_stock=w_wset_data(:,2);
dateTem=w.tdays('20150101',today,'Period=Y','Days=Alldays');
if sum(dateTem{end}(end-1:end)=='31')==2
    dateTem0=dateTem{end};
    dateTem1=dateTem{end}(1:4);
else
    dateTem0=dateTem{end-1};
    dateTem1=dateTem{end-1}(1:4);
end
data=w.wss(x_stock,'growth_cagr_tr,growth_netprofit,est_cagr_np,west_yoynetprofit',strcat('year=',dateTem1),'n=5',...
    strcat('rptDate=',dateTem0),'N=3',strcat('tradeDate=',dateTem{end}),'westPeriod=180');
indexTem=sum(isnan(data),2)<1;
data=data(indexTem,:);
x_stock=x_stock(indexTem);
Value=0.47*data(:,1)+0.24*data(:,2)+0.18*data(:,3)+0.11*data(:,4);
growthValue={x_stock,Value};
save Growth growthValue;
end