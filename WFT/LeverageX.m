function leverageValue=LeverageX
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
data=w.wss(x_stock,'ev,wgsd_debt_lt,debttoassets,wgsd_com_eq_paholder,wgsd_stkhldrs_eq',...
    strcat('rptDate=',dateTem0),'rptType=1','currencyType='); %最后两列分别是普通权益和总权益；
indexTem=sum(isnan(data),2)<1;
data=data(indexTem,:);
x_stock=x_stock(indexTem);
MLEV=(data(:,1)+data(:,2)+data(:,5)-data(:,4))./data(:,1);
DTOA=data(:,3)/100;
BLEV=(data(:,5)+data(:,2))./data(:,4);
Value=0.38*MLEV+0.35*DTOA+0.27*BLEV;
leverageValue={x_stock,Value};
save Leverage leverageValue;
end