function gpgValue=GPG
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','Id=a001010100000000');
stocks=w_wset_data(:,2);
dateTem=w.tdays('20100101',today,'Period=Y','Days=Alldays'); % get end day of years
dateSnap=['rptDate=',datestr(dateTem(end-1),'yyyymmdd')];
operateRevenue=w.wss(stocks,'oper_rev',dateSnap,'rptType=1');
ind=~isnan(operateRevenue);
operateRevenue=operateRevenue(ind);
stocks=stocks(ind);
dateSnap=['rptDate=',datestr(dateTem(end-2),'yyyymmdd')];
operateRevenuePre=w.wss(stocks,'oper_rev',dateSnap,'rptType=1');
GPG=operateRevenue./operateRevenuePre-1;
gpgValue={stocks,GPG};
end