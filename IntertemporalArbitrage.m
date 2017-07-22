function IntertemporalArbitrage(varargin)
tic;
sw1=1;
sw2=0;
%% Public codes;
if nargin==0
    Date=datestr(today,'yyyymmdd');
else
    Date=datestr(varargin(1),'yyyymmdd');
end
w=windmatlab;
parameters=['date=',Date,';','us_code=510050.SH;option_var=全部;call_put=全部;field=option_code,strike_price,call_put,first_tradedate,last_tradedate,option_name'];
data=w.wset('optionchain',parameters);
indTem=[];
for i=1:size(data,1)
    if data{i,end}(end)~='A'
        indTem=[indTem;i];
    end
end
data=data(indTem,:);
indTem=strcmp(data(:,3),'认购');
optionBuy=data(indTem,:);%1code;2price;3call;4last trade date;
optionSell=data(~indTem,:);
futures=w.wss('IH00.CFE,IH01.CFE,IH02.CFE,IH03.CFE','trade_hiscode,lastdelivery_date',['tradeDate=',Date]);%1code;2last trade date;
%% sw1: scan current arbitrage diff;
if sw1
    L=size(optionBuy,1);
    for i=1:L % loop for options
        for ii=1:4 % loop for futures
            buyTem=w.wsq(optionBuy(i,1),'rt_latest,rt_vol');
            sellTem=w.wsq(optionSell(i,1),'rt_latest,rt_vol');            
            if datenum(optionBuy(i,5))<datenum(futures(ii,2))
                diff=w.wsq(futures(ii,1),'rt_latest')*300*(1-0.506/10000)-...
                    (optionBuy{i,2}+buyTem(1)-sellTem(1))*300000-876;
            else
                diff=(optionBuy{i,2}+buyTem(1)-sellTem(1))*300000-...
                    w.wsq(futures(ii,1),'rt_latest')*300*(1+0.506/10000)-876;
            end
            display([futures{ii,1},'-',num2str(optionBuy{i,2}),': ',num2str(diff),...
                '; volume(buy/sell):',num2str(buyTem(2)/1000),'/',num2str(sellTem(2)/1000),'(k)']);
        end
    end
end
%% sw2: draw history K lines of this arbitrage model;
if sw2
    [priceF1,~,~,Time1]=w.wsi(futures(1,1),'open,close','20150209',datestr(today,'yyyymmdd'),'periodstart=09:30:00;periodend=15:00:00');%;PriceAdj=F
    indTem=isnan(priceF1(:,2));
    priceF1=priceF1(indTem,:);
    Time1=Time1(indTem);
    [priceF2,~,~,Time2]=w.wsi(futures(2,1),'open,close','20150209',datestr(today,'yyyymmdd'),'periodstart=09:30:00;periodend=15:00:00');
    indTem=isnan(priceF2(:,2));
    priceF2=priceF2(indTem,:);
    Time2=Time2(indTem);
    [priceF3,~,~,Time3]=w.wsi(futures(3,1),'open,close','20150209',datestr(today,'yyyymmdd'),'periodstart=09:30:00;periodend=15:00:00');
    indTem=isnan(priceF3(:,2));
    priceF3=priceF3(indTem,:);
    Time3=Time3(indTem);
    [priceF4,~,~,Time4]=w.wsi(futures(4,1),'open,close','20150209',datestr(today,'yyyymmdd'),'periodstart=09:30:00;periodend=15:00:00');
    indTem=isnan(priceF4(:,2));
    priceF4=priceF4(indTem,:);
    Time4=Time4(indTem);
    L=size(optionBuy,1);
    for i=1:L % loop for options
        [priceB,~,~,timeB]=w.wsi(optionBuy(i,1),'open,close',optionBuy(i,4),datestr(today,'yyyymmdd'),'periodstart=09:30:00;periodend=15:00:00');
        [priceS,~,~,timeS]=w.wsi(optionSell(i,1),'open,close',optionBuy(i,4),datestr(today,'yyyymmdd'),'periodstart=09:30:00;periodend=15:00:00');
        for ii=1:4 % loop for futures
            
            
            
        end
    end
end

toc;
end