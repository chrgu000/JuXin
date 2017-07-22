function scanTrade   % scan stocks which fit some Models and trade them automaticly;
trade=input('please confirm trading or not[y/n]?','s');
trade=strcmpi(trade,'y');
tic;
global date high low close open vol atr;
h=waitbar(0,'Wait for data in ...');
w=windmatlab;
pause(3);
Tem=w.tlogon('0000', '0', 'W115294100301', '*********', 'SHSZ'); 
logId=Tem{1};
try 
    load scanTrade; %save data of open close and so on;
    daysTem=w.tdays('ED-1TD',today);
    daysTem=datenum(daysTem,'yyyy/mm/dd');
    if daysTem(2)==today
        lastTradeDay=daysTem(1);
    else
        lastTradeDay=daysTem(2);
    end
    if Date(end)<lastTradeDay
        dataTem=w.wset('SectorConstituent');
        stocks=dataTem(:,2);
        while 1
            [Open,~,~,Date]=w.wsd(stocks,'open','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
            Close=w.wsd(stocks,'close','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
            High=w.wsd(stocks,'high','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
            Low=w.wsd(stocks,'low','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
            Vol=w.wsd(stocks,'volume','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
            if all([length(Open)>1,length(Close)>1,length(High)>1,length(Low)>1,length(Vol)>1])
                break;
            end
        end
        save scanTrade Date Open Close High Low Vol stocks;   
    end
catch
    dataTem=w.wset('SectorConstituent');
    stocks=dataTem(:,2);
    while 1
        [Open,~,~,Date]=w.wsd(stocks,'open','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
        Close=w.wsd(stocks,'close','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
        High=w.wsd(stocks,'high','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
        Low=w.wsd(stocks,'low','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
        Vol=w.wsd(stocks,'volume','ED-20TD',today-1,'Fill=Previous','PriceAdj=F');
        if all([length(Open)>1,length(Close)>1,length(High)>1,length(Low)>1,length(Vol)>1])
            break;
        end
    end
    save scanTrade Date Open Close High Low Vol stocks;   
end
Date=[Date;today];
Open=[Open;w.wsq(stocks,'rt_open')'];
Close=[Close;w.wsq(stocks,'rt_latest')'];
High=[High;w.wsq(stocks,'rt_high')'];
Low=[Low;w.wsq(stocks,'rt_low')'];
Vol=[Vol;w.wsq(stocks,'rt_vol')'];
try 
    load scanTradePosition; %save trade orders situation;
    [~,indTem0,indTem]=intersect(stocksHold,stocks);
    
    openTem=Open(:,indTem);
    closeTem=Close(:,indTem);
    highTem=High(:,indTem);
    lowTem=Low(:,indTem);    
    stocksHold=stocksHold(indTem0);
    dateTrade=dateTrade(indTem0);
    sharesHold=sharesHold(indTem0);
    typeM=typeM(indTem0);
    Lhold=length(stocksHold);
    indRe=zeros(Lhold,1);
    for i=1:Lhold
        open=openTem(:,i);
        close=closeTem(:,i);
        high=highTem(:,i);
        low=lowTem(:,i);
        if today-dateTrade(i)<1
            continue;
        end
%         if typeM(i)==6.1
%             if close(end)>=low(end)+(high(end)-low(end))*0.9&&close(end)>close(end-1)*1.03 && today-dateTrade(i)==1
%                 continue;
%             end
%         else
%             if close(end)-open(end)>=(high(end)-low(end))*1.1&&today-dateTrade(i)==1
%                 continue;
%             end
%         end
        fprintf('Close %s: %d shares;',stocksHold{i},sharesHold(i));
        if trade
            w.torder(stocksHold(i), 'Sell', '0', sharesHold(i), ['OrderType=B5TC;','LogonID=',num2str(logId)]);
            indRe(i)=1;     
            fprintf('send trade command!\n');
        else
            fprintf('not realy trade!\n');
        end   
    end    
    indTem0=indRe<1;
    stocksHold=stocksHold(indTem0);
    dateTrade=dateTrade(indTem0);
    sharesHold=sharesHold(indTem0);
    typeM=typeM(indTem0);
catch
    assetTotal=[];
    dateAsset=[];    
    stocksHold={};
    dateTrade=[];
    sharesHold=[];
    typeM=[]; % mark which type for closeing order;
end
Lstocks=length(stocks);
sti={};
shi=[];
tMi=[];
cli=[];%capital
pPi=[];%profit per order;
indicatorS=zeros(10,9);% Model Spring for hmm;columes:sti,shi,tMi,cli,pPi;
iSi=0;%count for indicatorS;
stockS=cell(10,1);% Model Spring for stocks' names;
for i=1:Lstocks
    open=Open(:,i); % get current stock's data;
    close=Close(:,i);
    high=High(:,i);
    low=Low(:,i);
    
    Lnan=sum(isnan(open));% delete Nan value;
    if Lnan>10
        continue;
    else
        open=open(Lnan+1:end);
        close=close(Lnan+1:end);
        high=high(Lnan+1:end);
        low=low(Lnan+1:end);
    end
    if close(end)/close(end-1)>=1.09 
        continue;
    end
    if close(end-1)<low(end-1)+(high(end-1)-low(end-1))*0.25 &&high(end)>low(end)...
            &&close(end)/close(end-1)-1>=0.025&&close(end)/close(end-1)-1<0.055 && low(end)/low(end-1)-1>=0.01 %% model:1 modelSpring
        handsB=ceil(100/close(end))*100;
        iSi=iSi+1;
        stockS(iSi)=stocks(i);
        indicatorS(iSi,:)=[handsB,1,close(end)*handsB,2.05,std([close(end);open(end);low(end);high(end)])/std([close(end-1);open(end-1);low(end-1);high(end-1)])-1,...
            mean(close(end-3:end))/mean(close(end-10:end))-1,high(end)/high(end-1)-1,close(end)/low(end-1)-1,close(end)/high(end-1)-1];         
    end
    if low(end-2)<=min(low(end-6:end)) %3
        if close(end)>=low(end)+(high(end)-low(end))*0.7
            if high(end-1)>max(high([end-2,end]))&&low(end-1)>low(end)&&close(end-2)>open(end-2)&&close(end)>=close(end-1)*1.025
                handsB=ceil(100/close(end))*100;
                sti=[sti;stocks(i)];
                shi=[shi;handsB];
                tMi=[tMi;3.1];
                cli=[cli;close(end)*handsB];
                pPi=[pPi;1.72];
            elseif high(end)<max(high(end-2:end-1)) && close(end-2)>open(end-2)&&close(end-1)<open(end-1)&&close(end)>close(end-1)*1.03
                handsB=ceil(100/close(end))*100;
                sti=[sti;stocks(i)];
                shi=[shi;handsB];
                tMi=[tMi;3.2];
                cli=[cli;close(end)*handsB];
                pPi=[pPi;2.01];
            end
        end   
    elseif low(end-3)<=min(low(end-7:end)) %4
        if close(end)>=low(end)+(high(end)-low(end))*0.8
            if high(end-2)>=max(high(end-3:end))&&low(end-1)<low(end-2)&&low(end-2)>low(end-1)&& close(end)>=close(end-1)*1.03
                corrTest=corr2([low(end-3),open(end-3),close(end-3),high(end-3)],[low(end-1),close(end-1),open(end-1),high(end-1)]);
                if corrTest<0.93
                    handsB=ceil(100/close(end))*100;
                    sti=[sti;stocks(i)];
                    shi=[shi;handsB];
                    tMi=[tMi;4.1];
                    cli=[cli;close(end)*handsB];
                    pPi=[pPi;1.79];
                end
            elseif high(end-3)<high(end-2)&&low(end-3)<low(end-2)&& high(end)<high(end-1)&&low(end)<low(end-1)&&close(end)>=close(end-1)*1.015
                corrTest1=corr2([low(end-3),open(end-3),close(end-3),high(end-3)],[low(end),close(end),open(end),high(end)]);
                corrTest2=corr2([low(end-2),open(end-2),close(end-2),high(end-2)],[low(end-1),close(end-1),open(end-1),high(end-1)]);
                if corrTest1<0.85&&corrTest2<0.9 
                    handsB=ceil(100/close(end))*100;
                    sti=[sti;stocks(i)];
                    shi=[shi;handsB];
                    tMi=[tMi;4.2];
                    cli=[cli;close(end)*handsB];
                    pPi=[pPi;1.54];
                end                   
            end
        end
    elseif low(end-4)<=min(low(end-10:end)) %5
        if close(end)>=low(end)+(high(end)-low(end))*0.8
            if high(end-2)>max([high(end-4:end-3);high(end-1:end)])&&close(end)>close(end-1)*1.02&&low(end)>=low(end-4) 
                corrTest=corr2([low(end-4),open(end-4),close(end-4),high(end-4)],[low(end),close(end),open(end),high(end)]);
                if corrTest>0.9
                    handsB=ceil(100/close(end))*100;
                    sti=[sti;stocks(i)];
                    shi=[shi;handsB];
                    tMi=[tMi;5.1];
                    cli=[cli;close(end)*handsB];
                    pPi=[pPi;1.62];
                end
            elseif high(end)<max(high(end-3:end-2))&&low(end-4)<low(end-3)&&low(end-1)<low(end-2)&&close(end)>close(end-1)*1.03
                corrTest1=corr2([low(end-4),open(end-4),close(end-4),high(end-4)],[low(end-1),close(end-1),open(end-1),high(end-1)]);
                corrTest2=corr2([low(end-3),open(end-3),close(end-3),high(end-3)],[low(end-2),close(end-2),open(end-2),high(end-2)]);
                if corrTest1>0.85&&corrTest2>0.85
                    handsB=ceil(100/close(end))*100;
                    sti=[sti;stocks(i)];
                    shi=[shi;handsB];
                    tMi=[tMi;5.2];
                    cli=[cli;close(end)*handsB];
                    pPi=[pPi;2.00];
                end
            end
        end
    elseif low(end-5)<=min(low(end-10:end)) %6
        if high(end)<max(high(end-3:end-2))&&high(end-2)>=high(end-1)&&close(end)>close(end-1)*1.02&&close(end-5)>open(end-5)
            Tem=[high(end-5:end-3),low(end-5:end-3)];
            Tem=Tem(2:end,:)-Tem(1:end-1,:);      
            Tem=sum(Tem>=0);                      
            highL=Tem(1);
            lowL=Tem(2);
            Tem=low(end-2:end);
            Tem=Tem(2:end)-Tem(1:end-1);
            Tem=sum(Tem<=0);
            lowR=Tem;
            corrTest=corr2([low(end-3),open(end-3),close(end-3),high(end-3)],[low(end-2),close(end-2),open(end-2),high(end-2)]);
            if highL==2&&lowL==2&&lowR==2&&corrTest<0.93
                handsB=ceil(100/close(end))*100;
                sti=[sti;stocks(i)];
                shi=[shi;handsB];
                tMi=[tMi;6.1];
                cli=[cli;close(end)*handsB];
                pPi=[pPi;2.25];
            end            
        end
    end
    tem=i/length(stocks);
    waitbar(tem,h,['Scaning: Completed...',num2str(roundn(100*tem,-2)),'%']);
end

indicatorS=indicatorS(1:iSi,:);
stockS=stockS(1:iSi);
flagTem=HMMpy(indicatorS(:,5:end));
indicatorS(:,4)=flagTem;
indTem=flagTem>0;
sti=[sti;stockS(indTem)];
shi=[shi;indicatorS(indTem,1)];
tMi=[tMi;indicatorS(indTem,2)];
cli=[cli;indicatorS(indTem,3)];
pPi=[pPi;indicatorS(indTem,4)];

[pPi,indTem]=sort(pPi,'descend');
sti=sti(indTem);
shi=shi(indTem);
tMi=tMi(indTem);
cli=cli(indTem);
dataTem=w.tquery('Capital', ['LogonId=',num2str(logId)]);
availableFun=dataTem{2};
assetNow=dataTem{6};
cliCS=cumsum(cli);
tem=find(cliCS>availableFun,1);
if isempty(tem)
else
    indTem=1:tem-1;
    sti=sti(indTem);
    shi=shi(indTem);
    pPi=pPi(indTem);
    tMi=tMi(indTem);
end
Ltrade=length(sti);
for i=1:Ltrade
    fprintf('Buy %s: %d shares;use capital:%.f Yuan;profitPerOrder:%.2f,ModelNumber:%d',sti{i},shi(i),cli(i),pPi(i),tMi(i));
    if trade
        w.torder(sti(i), 'Buy', '0', shi(i), ['OrderType=B5TC;','LogonID=',num2str(logId)]);
        fprintf(';send trade command!\n');
    else
        fprintf(';not realy trade!\n');
    end      
end
toc;
if trade
    stocksHold=[stocksHold;sti];
    dateTrade=[dateTrade;repmat(today,Ltrade,1)];
    sharesHold=[sharesHold;shi];
    typeM=[typeM;tMi];
end
if isempty(dateAsset)
    dateAsset=today;
    assetTotal=assetNow;
else
    if dateAsset(end)==today
        assetTotal(end)=assetNow;
    else
        dateAsset=[dateAsset;today];
        assetTotal=[assetTotal;assetNow];
    end
end
waitbar(1,h,'Completed...100%');
delete(h);
w.tlogout(num2str(logId));
save scanTradePosition assetTotal dateAsset stocksHold dateTrade sharesHold typeM;
end




















