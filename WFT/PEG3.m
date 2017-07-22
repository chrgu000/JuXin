function peg3Value=PEG3
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','Id=a001010100000000');
stocks=w_wset_data(:,2);
dateTem=w.tdays('20100101',today,'Period=Y','Days=Alldays'); % get end day of years
dateTarget=dateTem(end-3:end-1); 
PE3=arrayfun(@(x) PETTM(x),dateTarget,'UniformOutput',false);
PE3=[PE3{1}{2},PE3{2}{2},PE3{3}{2}];
indPE3=sum(isnan(PE3),2)==0;

dateSnap=['rptDate=',datestr(dateTarget(end),'yyyymmdd')];
netProfit=w.wss(stocks,'net_profit_is',dateSnap,'rptType=1');
ind=~isnan(netProfit);
ind=sum([indPE3,ind],2)==2;

PE3=PE3(ind,:);
netProfit=netProfit(ind);
stocks=stocks(ind);
netProfits=zeros(length(netProfit),3);
for i=1:3
    dateTargetPre=dateTem(end-5+i); 
    dateSnapPre=['rptDate=',datestr(dateTargetPre,'yyyymmdd')];
    netProfits(:,i)=w.wss(stocks,'net_profit_is',dateSnapPre,'rptType=1');
end

netProfits=[netProfits,netProfit];
netProfitsRatio=netProfits(:,2:4)./netProfits(:,1:3);
PEG3=mean(PE3./netProfitsRatio,2);
peg3Value={stocks,PEG3};

end