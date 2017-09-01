function ExRight
sw1=1; % get current ExRight status;
sw2=1; % get history ExRight status;
w=windmatlab;
index='000016.sh';
dateTest='2017-7-21';% for sw2
%% get current ExRight status;
if sw1 
    firstTime=1;
    try
        monthNow=month(today);
        if monthNow<5 || monthNow>=11
            display('no need to calculate within month 1~4 and 11~12');
            delete ExRight.mat;
            return;
        end
        load ExRight;
        firstTime=0;
        if year(dateComplete)<year(today)
            firstTime=1;
        end
    end
    yearNow=year(now);
    if firstTime  % calculate diff until now from May
        DaysPast=w.tdays([num2str(yearNow),'0501'],today);
        Ldays=length(DaysPast);
        DiffEx=[];
        PindexNan=[];
        weightCompleted=0;
        PstockNan=[];
        cashNan=[];
        stockNan=[];
        nameNan=[];
        stocksAll=[];
        namesAll=[];
        for i=1:Ldays
            datei=DaysPast(i);
            param=['date=',datei{1},';windcode=',index];
            [dateEx,cashEx,stocksEx,namesEx,weightsEx]=getData(w,param); 
            indi2=dateEx==datenum(datei,'yyyy/mm/dd');
            dateEx=dateEx(indi2);
            cashEx=cashEx(indi2);
            stocksEx=stocksEx(indi2);
            namesEx=namesEx(indi2);
            weightsEx=weightsEx(indi2);
            Li2=length(dateEx);
            diffi=0;
            for ii=1:Li2
                datei2=dateEx(ii);
                cashi2=cashEx(ii);
                stocki2=stocksEx(ii);
                namei2=namesEx(ii);
                weighti2=weightsEx(ii);
                while 1
                    dataTem=w.wss([stocki2,',',index],'close',['tradeDate=',datestr(datei2,'yyyy/mm/dd')],'priceAdj=U','cycle=D');
                    if length(dataTem)>1
                        break;
                    end
                end
                diffTem=dataTem(2)*cashi2/dataTem(1)*weighti2*3;
                if isnan(weighti2)
                    cashNan=[cashNan;cashi2];
                    PstockNan=[PstockNan;dataTem(1)];
                    PindexNan=[PindexNan;dataTem(2)];
                    stockNan=[stockNan;stocki2];
                    nameNan=[nameNan;namei2];                    
                elseif ~isnan(diffTem)
                    diffi=diffi+diffTem; 
                    weightCompleted=weightCompleted+weighti2;
                end            
            end
            DiffEx=[DiffEx;diffi]; 
            stocksAll=[stocksAll;stocksEx];
            namesAll=[namesAll;namesEx];
        end
        dataTem=w.wsd('000016.sh,510050.sh','close',[num2str(yearNow),'0101'],[num2str(yearNow),'0501']);
        diffBase=mean(dataTem(:,2)*1000-dataTem(:,1))*300;         
        StocksEx=unique(stocksAll);
        NamesEx=unique(namesAll);
        dateCompleted=today;
        save ExRight dateCompleted weightCompleted DiffEx diffBase StocksEx NamesEx cashNan PstockNan PindexNan stockNan nameNan;
    else
        DaysPast=w.tdays(datestr(dateCompleted,'yyyy/mm/dd'),today);
        Ldays=length(DaysPast);
        if Ldays>1
            DiffExAdd=[];
            for i=2:Ldays
                datei=DaysPast(i);
                param=['date=',datei{1},';windcode=',index];
                [dateEx,cashEx,stocksEx,namesEx,weightsEx]=getData(w,param); 
                indi2=dateEx==datenum(datei,'yyyy/mm/dd');
                dateEx=dateEx(indi2);
                cashEx=cashEx(indi2);
                stocksEx=stocksEx(indi2);
                namesEx=namesEx(indi2);
                weightsEx=weightsEx(indi2);
                Li2=length(dateEx);
                diffi=0;
                for ii=1:Li2
                    datei2=dateEx(ii);
                    cashi2=cashEx(ii);
                    stocki2=stocksEx(ii);
                    namei2=namesEx(ii);
                    weighti2=weightsEx(ii);
                    while 1
                        dataTem=w.wss([stocki2,',',index],'close',['tradeDate=',datestr(datei2,'yyyy/mm/dd')],'priceAdj=U','cycle=D');
                        if length(dataTem)>1
                            break;
                        end
                    end
                    diffTem=dataTem(2)*cashi2/dataTem(1)*weighti2*3;
                    if isnan(weighti2)
                        cashNan=[cashNan;cashi2];
                        PstockNan=[PstockNan;dataTem(1)];
                        PindexNan=[PindexNan;dataTem(2)];
                        stockNan=[stockNan;stocki2];
                        nameNan=[nameNan;namei2]; 
                    elseif ~isnan(diffTem)
                        diffi=diffi+diffTem;
                        weightCompleted=weightCompleted+weighti2;
                    end            
                end
                DiffExAdd=[DiffExAdd;diffi];
                StocksEx=[StocksEx;stocksEx];
                NamesEx=[NamesEx;namesEx];
            end
            DiffEx=[DiffEx;DiffExAdd];        
        end
        
        dataTem=w.wset('indexconstituent',['windcode=',index]);
        stocksTem=dataTem(:,2);
        weightsTem=dataTem(:,4);
        [~,indNan,indTem]=intersect(stockNan,stocksTem);
        namesAdd=[];
        diffExAdd=[];
        for i=1:length(indTem)
            if ~isnan(weightsTem{indTem(i)})
                namesAdd=[namesAdd;nameNan(indNan(i))];
                diffExAdd=[diffExAdd;PindexNan(indNan(i))*cashNan(indNan(i))/PstockNan(indNan(i))*weightsTem{indTem(i)}*3];
                weightCompleted=weightCompleted+weightsTem{indTem(i)};
            end
        end
        DiffEx(end)=DiffEx(end)+sum(diffExAdd);
        Lt=length(indNan);
        indTem=zeros(Lt,1);
        for i=1:Lt
            if indNan(i)>0
                indTem(indNan(i))=1;
            end
        end
        cashNan(indTem)=[];
        PstockNan(indTem)=[];
        PindexNan(indTem)=[];
        stockNan(indTem)=[];
        nameNan(indTem)=[];
        dateCompleted=today;
        save ExRight dateCompleted weightCompleted DiffEx diffBase StocksEx NamesEx cashNan PstockNan PindexNan stockNan nameNan;
    end
    fprintf(['截至今天','(',datestr(today,'yyyy/mm/dd'),')上证50成分股除权总数为：%d支'],size(StocksEx,1));
    fprintf(2,'(权重总和为%.1f%%),',weightCompleted);
    fprintf('由此产生的Diff值为：%.1f；\n',sum(DiffEx)+diffBase);
    try
        if ~isempty(namesAdd)
            fprintf('其中需对Diff值进行追加(除权时权重为Nan)的股票数为：%d支，本次追加的Diff总值为：%.1f；\n',length(namesAdd),sum(diffExAdd));
            display([['股票名称';namesAdd],['Diff贡献值：'; num2cell(diffExAdd)]]);
        end
    end
    
    param=['date=',datestr(today,'yyyy-mm-dd'),';windcode=',index];
    [dateEx,cashEx,stocksEx,namesEx,weightsEx]=getData(w,param);
    
    indTem=dateEx==today;% calculate diff of Today
    cashExT=cashEx(indTem);
    stocksExT=stocksEx(indTem);
    namesExT=namesEx(indTem);
    weightsExT=weightsEx(indTem);
    Lt=length(stocksExT);
    diffi=[];
    for i=1:Lt
        cashi=cashExT(i);
        stocki=stocksExT(i);
        namei=namesExT(i);
        weighti=weightsExT(i);
        while 1
            dataTem=w.wss([stocki,',',index],'close',['tradeDate=',datestr(today-1,'yyyy/mm/dd')],'priceAdj=U','cycle=D');
            if length(dataTem)>1
                break;
            end
        end
        diffTem=dataTem(2)*cashi/dataTem(1)*weighti*3;
        diffi=[diffi;diffTem];
    end
    fprintf('其中今天除权数为：%d支，增加的Diff值为：%.1f；\n',length(stocksExT),sum(diffi(~isnan(diffi))));
    if length(stocksExT)>=1
        display([['股票名称';namesExT],['Diff贡献值：'; num2cell(diffi)]]);
    end
    
    dateTrade=datenum(w.tdays(today,today+15),'yyyy/mm/dd');% calculate diff of the next trading day;
    if dateTrade(1)==today
        tomorrow=dateTrade(2);
    else
        tomorrow=dateTrade(1);
    end
    indTem=dateEx==tomorrow;
    cashExT=cashEx(indTem);
    stocksExT=stocksEx(indTem);
    namesExT=namesEx(indTem);
    weightsExT=weightsEx(indTem);
    Lt=length(stocksExT);
    diffi=[];
    for i=1:Lt
        cashi=cashExT(i);
        stocki=stocksExT(i);
        namei=namesExT(i);
        weighti=weightsExT(i);
        while 1
            dataTem=w.wss([stocki,',',index],'close',['tradeDate=',datestr(today-1,'yyyy/mm/dd')],'priceAdj=U','cycle=D');
            if length(dataTem)>1
                break;
            end
        end
        diffTem=dataTem(2)*cashi/dataTem(1)*weighti*3;
        diffi=[diffi;diffTem];
    end
    fprintf(['下一交易日(',datestr(tomorrow,'yyyy/mm/dd'),')除权数预计为：%d支，预计增加的Diff值为：%.1f；\n'],length(stocksExT),sum(diffi(~isnan(diffi))));
    if length(stocksExT)>=1
        display([['股票名称';namesExT],['Diff贡献值预计：';num2cell(diffi)]]);
    end
    
    indTem=dateEx>tomorrow;% calculate diff of all days after the next trading day;
    dateExT=dateEx(indTem);
    cashExT=cashEx(indTem);
    stocksExT=stocksEx(indTem);
    namesExT=namesEx(indTem);
    weightsExT=weightsEx(indTem);
    Lt=length(stocksExT);
    diffi=[];
    for i=1:Lt
        cashi=cashExT(i);
        stocki=stocksExT(i);
        namei=namesExT(i);
        weighti=weightsExT(i);
        while 1
            dataTem=w.wss([stocki,',',index],'close',['tradeDate=',datestr(today-1,'yyyy/mm/dd')],'priceAdj=U','cycle=D');
            if length(dataTem)>1
                break;
            end
        end
        diffTem=dataTem(2)*cashi/dataTem(1)*weighti*3;
        diffi=[diffi;diffTem];
    end
    fprintf('下一交易日以后（不含下一交易日）除权数预计为：%d支，预计增加的Diff值为：%.1f；\n',length(stocksExT),sum(diffi(~isnan(diffi))));
    if length(stocksExT)>=1
        display([['股票名称';namesExT],['除权日期';cellstr(datestr(dateExT,'yyyy/mm/dd'))],['Diff贡献值预计：';num2cell(diffi)]]);
    end
    figure;
    [dataTem,~,~,DateTem]=w.wsd('000016.sh,510050.sh','close',[num2str(yearNow),'0101'],today);
    dataTem(end,:)=w.wsq('000016.sh,510050.sh','rt_latest');
    Diff=(dataTem(:,2)*1000-dataTem(:,1))*300;
    Ld=length(Diff);
    Ldx=length(DiffEx);
    DiffExTem=[zeros(Ld-Ldx,1);DiffEx];
    DiffExTem(1)=diffBase;
    DiffExTem=cumsum(DiffExTem);
    plot([Diff,DiffExTem],'LineWidth',1);
    step=floor(Ld/18);
    indTem=1:step:Ld;
    if indTem(end)~=Ld
        indTem(end)=Ld;
    end
    title('最新Diff实际值和除权计算值走势','color','r','fontsize',15);
    set(gca,'xtick',indTem);
    set(gca,'xticklabel',cellstr(datestr(DateTem(indTem),'yyyymmdd')),'xticklabelrotation',60);
    h=legend('Diff实际值','Diff除权计算值','Location','northwest');
    set(h,'fontsize',12);
    grid on;    

%% get history ExRight status;
elseif sw2
    dataTem=w.wset('indexconstituent',['date=',dateTest,';windcode=000016.SH']);
    stocks=dataTem(:,2);
    names=dataTem(:,3);
    weights=cell2mat(dataTem(:,4));
    yearNow=str2num(datestr(dateTest,'yyyy'));
    dataTem=w.wss(stocks,'div_cashandstock,div_exdate',['rptDate=',num2str(yearNow-1),'1231']);
    cashEx=cell2mat(dataTem(:,1));
    DateEx=dataTem(:,2);
    indTem=~strcmp(DateEx,'0:00:00');
    stocks=stocks(indTem);
    names=names(indTem);
    weights=weights(indTem);
    DateEx=DateEx(indTem);
    cashEx=cashEx(indTem);
    exDates=datenum(DateEx,'yyyy/mm/dd');
    indTem=exDates>datenum([num2str(yearNow),'0501'],'yyyymmdd') & exDates<=datenum(dateTest,'yyyy-mm-dd');
    stocks=stocks(indTem);
    weights=weights(indTem);
    DateEx=cellstr(datestr(exDates(indTem)-1,'yyyymmdd'));
    cashEx=cashEx(indTem);
    prices=w.wsd('000016.sh,510050.sh','close',[num2str(yearNow),'0101'],[num2str(yearNow),'0501']);
    diff=mean(prices(2)-prices(1));
    for i=1:length(stocks)
        stock=stocks{i};
        Date=DateEx{i};
        weight=weights(i);
        dataTem=w.wss([stock,',',index],'close',['tradeDate=',Date],'priceAdj=U','cycle=D');
        stockP=dataTem(1);
        indexP=dataTem(2);
        diffTem=indexP*cashEx(i)/stockP*weight*3;
        if ~isnan(diffTem)
            diff=diff+diffTem;
        end
    end    
    display(diff);
end
end

function [dateEx,cashEx,stocksEx,namesEx,weightsEx]=getData(w,param)
dataTem=w.wset('indexconstituent',param);
stocks=dataTem(:,2);
names=dataTem(:,3);
weights=cell2mat(dataTem(:,4));
yearNow=year(now);
while 1
    dateExTem=w.wsd(stocks,'div_exdate',[num2str(yearNow-1),'0101'],today,'Period=Q;Days=Alldays');
    if length(dateExTem)>1
        break;
    end
end
while 1
    cashExTem=w.wsd(stocks,'div_cashandstock',[num2str(yearNow-1),'0101'],today,'Period=Q;Days=Alldays');
    if length(cashExTem)>1
        break;
    end
end
dateEx=[];
cashEx=[];
stocksEx=[];
namesEx=[];
weightsEx=[];
for i=1:50
    datei=dateExTem(:,i);
    cashi=cashExTem(:,i);
    indTem=~cellfun(@any,cellfun(@isnan,datei,'un',0));
    if sum(indTem)<1
        continue;
    end
    dateEx=[dateEx;datenum(datei(indTem),'yyyy/mm/dd')];
    cashEx=[cashEx;cashi(indTem)];
    stocksEx=[stocksEx;repmat(stocks(i),[sum(indTem),1])];
    namesEx=[namesEx;repmat(names(i),[sum(indTem),1])];
    weightsEx=[weightsEx;repmat(weights(i),[sum(indTem),1])];
end
end









