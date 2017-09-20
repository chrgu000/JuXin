% function optionShort % short less price for "buy/sell" according to their
% prices;
%     stepShort=2; % gas between current value and void value;
%     holdDays=20; % trading days from "short" to expire date;
%     dateFrom='2014/5/1';
%     dateFrom=year(datenum(dateFrom))*100+month(datenum(dateFrom));
%     w=windmatlab;
%     loops=ceil((today-datenum(2015,2,9))/29);
%     
%     Year=2015;
%     Month=1;
%     monthTem=1;
%     Day=28;
%     Data=[];% store data for all options;
%     for j=1:loops
%         if monthTem==12
%             Year=Year+1;
%         end
%         Month=Month+1;
%         monthTem=mod(Month,12);
%         if monthTem==0
%             monthTem=12;
%         end
%         Date=datenum(Year,monthTem,Day);
%         if Date >today
%             Date=today;
%         end    
%         parameters=['date=',datestr(Date,'yyyy-mm-dd'),';','us_code=510050.SH;option_var=全部;',...
%             'call_put=认购;field=option_code,strike_price,month,call_put,first_tradedate,last_tradedate,option_name'];
%         data=w.wset('optionchain',parameters);
%         Data=[Data;data];
%         if Date==today
%             break;
%         end       
%     end
%     options=Data(:,1);
%     [options,indTem]=unique(options);
%     Data=Data(indTem,:);
%     prices=cell2mat(Data(:,2));
%     indTem=mod(prices,0.05)<0.00000001;
%     prices=prices(indTem);
%     months=cell2mat(Data(indTem,3));
%     starts=Data(indTem,5);
%     ends=Data(indTem,6);      
%     options=options(indTem);
%     
%     Year=2015;
%     Month=1;
%     monthTem=1;
%     Day=28;
%     Data=[];% store data for all options;
%     for j=1:loops
%         if monthTem==12
%             Year=Year+1;
%         end
%         Month=Month+1;
%         monthTem=mod(Month,12);
%         if monthTem==0
%             monthTem=12;
%         end
%         Date=datenum(Year,monthTem,Day);
%         if Date >today
%             Date=today;
%         end    
%         parameters=['date=',datestr(Date,'yyyy-mm-dd'),';','us_code=510050.SH;option_var=全部;',...
%             'call_put=认沽;field=option_code,strike_price,month,call_put,first_tradedate,last_tradedate,option_name'];
%         data=w.wset('optionchain',parameters);
%         Data=[Data;data];
%         if Date==today
%             break;
%         end       
%     end
%     optionsSell=Data(:,1);
%     [optionsSell,indTem]=unique(optionsSell);
%     Data=Data(indTem,:);
%     pricesSell=cell2mat(Data(:,2));
%     indTem=mod(pricesSell,0.05)<0.00000001;
%     pricesSell=pricesSell(indTem);
%     monthsSell=cell2mat(Data(indTem,3));     
%     optionsSell=optionsSell(indTem);    
%     
%     Re=[];
%     records=[];
%     recordOptions={};
%     optionsRec={};
%     Comm=[];%for commission of all;
%     etfMonth={};
%     UniMonth=unique(months);
%     loops=length(UniMonth);    
%     for i=1:loops  
%         if Year*100+month(today)<=UniMonth(i)
%             continue;
%         end
%         if dateFrom>UniMonth(i)
%             continue;
%         end
%         indT=months==UniMonth(i);
%         optionT=options(indT);
%         priceT=prices(indT);
%         startT=starts(indT);
%         endT=ends(indT);
%         [priceT,tem]=unique(priceT);
%         optionT=optionT(tem);
%         startT=startT(tem);
%         endT=endT(tem); 
%         tem=datenum(endT)-datenum(startT)>5;
%         priceT=priceT(tem);
%         optionT=optionT(tem);
%         startT=startT(tem);
%         endT=endT(tem); 
%         
%         tradeDays=w.tdays(datenum(endT(1))-50,endT(1));
%         tradeDay=tradeDays(end-holdDays);
%         etfP=w.wss('510050.SH','close',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
%         difftem=abs(priceT-stepShort*0.05-etfP);
%         [~,tem]=sort(difftem);
%         optioni=optionT(tem(1));starti=startT(tem(1));endi=endT(tem(1));pricei=priceT(tem(1));
%         if min(difftem)>0.05 || datenum(starti)>datenum(tradeDay)
%             continue;
%         end
%         difftem=abs((etfP-(pricei-etfP))-priceT);
%         if min(difftem)>0.05
%             continue;
%         end
%         [~,tem]=sort(difftem);
%         priceiSell=priceT(tem(1));
%         monthiSell=UniMonth(i);
%         optioniSell=optionsSell((pricesSell==priceiSell)&(monthsSell==monthiSell));
%         tem=w.wss([optioni,optioniSell],'open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
%         if tem(1)>tem(2)
%             optioni=optioniSell;
%         end       
%         tem_1=w.wss(optioni,'open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
%         etf50_1=w.wss('510050.SH','open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
%         tem=w.wsd(optioni,'close',tradeDay{1},endi,'priceAdj=U');
%         ReTem=((tem(1)-tem(end))*10000-7.2)./commission(pricei,tem_1,etf50_1);
%         Re=[Re;ReTem];
%         etfMonth=[etfMonth;tradeDay{1}];
%         figure;
%         plot(tem);
%         title([endi{1},'--收益情况：',num2str(ReTem)]);
%     end
% 
%     figure;
%     ReCS=cumsum(Re);
%     plot(ReCS);
%     grid on;
%     Lre=length(Re);
%     step=max(floor(Lre/10),1);
%     set(gca,'xtick',1:step:Lre);
%     set(gca,'xticklabel',etfMonth(1:step:Lre),'XTickLabelRotation',60);
%     maxDown=0;
%     ReCS=[0;ReCS];
%     for i=2:Lre
%         tem=max(ReCS(1:i))-ReCS(i);
%         if tem>maxDown
%             maxDown=tem;
%         end
%     end
%     title(sprintf('年化收益估算：%.2f%%;最大回撤：%.2f%%',ReCS(end)*100/((datenum(etfMonth(end))-datenum(etfMonth(1)))/360), maxDown*100));
% end
    
  
    
    
%     function optionShort
%     stepShort=2; % gas between current value and void value;
%     holdDays=20; % trading days from "short" to expire date;
%     dateFrom='2014/5/1';
%     dateFrom=year(datenum(dateFrom))*100+month(datenum(dateFrom));
%     w=windmatlab;
%     loops=ceil((today-datenum(2015,2,9))/29);
%     Year=2015;
%     Month=1;
%     monthTem=1;
%     Day=28;
%     Data=[];% store data for all options;
%     for j=1:loops
%         if monthTem==12
%             Year=Year+1;
%         end
%         Month=Month+1;
%         monthTem=mod(Month,12);
%         if monthTem==0
%             monthTem=12;
%         end
%         Date=datenum(Year,monthTem,Day);
%         if Date >today
%             Date=today;
%         end    
%         parameters=['date=',datestr(Date,'yyyy-mm-dd'),';','us_code=510050.SH;option_var=全部;',...
%             'call_put=认购;field=option_code,strike_price,month,call_put,first_tradedate,last_tradedate,option_name'];
%         data=w.wset('optionchain',parameters);
%         Data=[Data;data];
%         if Date==today
%             break;
%         end       
%     end
%     options=Data(:,1);
%     [options,indTem]=unique(options);
%     Data=Data(indTem,:);
%     prices=cell2mat(Data(:,2));
%     indTem=mod(prices,0.05)<0.00000001;
%     prices=prices(indTem);
%     months=cell2mat(Data(indTem,3));
%     starts=Data(indTem,5);
%     ends=Data(indTem,6);      
%     options=options(indTem);
%     
%     Re=[];
%     records=[];
%     recordOptions={};
%     optionsRec={};
%     Comm=[];%for commission of all;
%     etfMonth={};
%     UniMonth=unique(months);
%     loops=length(UniMonth);
%     
%     for i=1:loops  
%         if Year*100+month(today)<=UniMonth(i)
%             continue;
%         end
%         if dateFrom>UniMonth(i)
%             continue;
%         end
%         indT=months==UniMonth(i);
%         optionT=options(indT);
%         priceT=prices(indT);
%         startT=starts(indT);
%         endT=ends(indT);
%         [priceT,tem]=unique(priceT);
%         optionT=optionT(tem);
%         startT=startT(tem);
%         endT=endT(tem); 
%         tem=datenum(endT)-datenum(startT)>5;
%         priceT=priceT(tem);
%         optionT=optionT(tem);
%         startT=startT(tem);
%         endT=endT(tem); 
%         
%         tradeDays=w.tdays(datenum(endT(1))-50,endT(1));
%         tradeDay=tradeDays(end-holdDays);
%         etfP=w.wss('510050.SH','close',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
%         difftem=abs(priceT-stepShort*0.05-etfP);
%         [~,tem]=sort(difftem);
%         optioni=optionT(tem(1));starti=startT(tem(1));endi=endT(tem(1));pricei=priceT(tem(1));
%         if min(difftem)>0.05 || datenum(starti)>datenum(tradeDay)
%             continue;
%         end
%         
%         tem_1=w.wss(optioni,'open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
%         etf50_1=w.wss('510050.SH','open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
%         priceTem=w.wsd(optioni,'close',tradeDay{1},endi,'priceAdj=U');
%         priceStop=priceTem(end);
%         for i2=2:length(priceTem)
%             if priceTem(i2)>=priceTem(1)*2
%                 priceStop=priceTem(i2);
%             end
%         end
%         ReTem=((priceTem(1)-priceStop)*10000-7.2)./commission(pricei,tem_1,etf50_1);
%         Re=[Re;ReTem];
%         etfMonth=[etfMonth;tradeDay{1}];
%         figure;
%         plot(priceTem);
%         title([endi{1},'--收益情况：',num2str(ReTem)]);
%     end
% 
%     figure;
%     ReCS=cumsum(Re);
%     plot(ReCS);
%     grid on;
%     Lre=length(Re);
%     step=max(floor(Lre/10),1);
%     set(gca,'xtick',1:step:Lre);
%     set(gca,'xticklabel',etfMonth(1:step:Lre),'XTickLabelRotation',60);
%     maxDown=0;
%     ReCS=[0;ReCS];
%     for i=2:Lre
%         tem=max(ReCS(1:i))-ReCS(i);
%         if tem>maxDown
%             maxDown=tem;
%         end
%     end
%     title(sprintf('年化收益估算：%.2f%%;最大回撤：%.2f%%',ReCS(end)*100/((datenum(etfMonth(end))-datenum(etfMonth(1)))/360), maxDown*100));
% end
    

function optionShort
    stepShort=2; % gas between current value and void value;
    holdDays=15; % trading days from "short" to expire date;
    stopRatio=1.2;
    dateFrom='2014/5/1';
    dateFrom=year(datenum(dateFrom))*100+month(datenum(dateFrom));
    w=windmatlab;
    loops=ceil((today-datenum(2015,2,9))/29);
    Year=2015;
    Month=1;
    monthTem=1;
    Day=28;
    Data=[];% store data for all options;
    for j=1:loops
        if monthTem==12
            Year=Year+1;
        end
        Month=Month+1;
        monthTem=mod(Month,12);
        if monthTem==0
            monthTem=12;
        end
        Date=datenum(Year,monthTem,Day);
        if Date >today
            Date=today;
        end    
        parameters=['date=',datestr(Date,'yyyy-mm-dd'),';','us_code=510050.SH;option_var=全部;',...
            'call_put=认购;field=option_code,strike_price,month,call_put,first_tradedate,last_tradedate,option_name'];
        data=w.wset('optionchain',parameters);
        Data=[Data;data];
        if Date==today
            break;
        end       
    end
    options=Data(:,1);
    [options,indTem]=unique(options);
    Data=Data(indTem,:);
    prices=cell2mat(Data(:,2));
    indTem=mod(prices,0.05)<0.00000001;
    prices=prices(indTem);
    months=cell2mat(Data(indTem,3));
    starts=Data(indTem,5);
    ends=Data(indTem,6);      
    options=options(indTem);
    
    Re=[];
    records=[];
    recordOptions={};
    optionsRec={};
    Comm=[];%for commission of all;
    etfMonth={};
    UniMonth=unique(months);
    loops=length(UniMonth);
    
    for i=1:loops  
        if Year*100+month(today)<=UniMonth(i)
            continue;
        end
        if dateFrom>UniMonth(i)
            UniMonth(i)
            continue;
        end
        indT=months==UniMonth(i);
        optionT=options(indT);
        priceT=prices(indT);
        startT=starts(indT);
        endT=ends(indT);
        [priceT,tem]=unique(priceT);
        optionT=optionT(tem);
        startT=startT(tem);
        endT=endT(tem); 
        tem=datenum(endT)-datenum(startT)>5;
        priceT=priceT(tem);
        optionT=optionT(tem);
        startT=startT(tem);
        endT=endT(tem); 
        
        tradeDays=w.tdays(datenum(endT(1))-50,endT(1));
        tradeDay=tradeDays(end-holdDays);
        etfP=w.wss('510050.SH','close',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
        difftem=abs(priceT-stepShort*0.05-etfP);
        [~,tem]=sort(difftem);
        optioni=optionT(tem(1));starti=startT(tem(1));endi=endT(tem(1));pricei=priceT(tem(1));
        if min(difftem)>0.05 || datenum(starti)>datenum(tradeDay)
            continue;
        end
        
        tem_1=w.wss(optioni,'open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
        etf50_1=w.wss('510050.SH','open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
        priceTem=w.wsd(optioni,'close',tradeDay{1},endi,'priceAdj=U');
        priceStop=priceTem(end);
        tem=w.wsd(optioni,'open,high,low',tradeDay{1},endi,'priceAdj=U');
        openTem=tem(:,1);highTem=tem(:,2);lowTem=tem(:,3);closeTem=priceTem;
        for i2=2:length(priceTem)
            if highTem(i2)>=priceTem(1)*stopRatio
                priceStop=max(openTem(i2),priceTem(1)*stopRatio);
                break;
            end
        end
        hands1=floor(0.1/(priceTem(1)*(stopRatio-1)));
        hands2=floor(10000/commission(pricei,tem_1,etf50_1));
        ReTem=((priceTem(1)-priceStop)*10000-7.2)*min(hands1,hands2);
        Re=[Re;ReTem];
        etfMonth=[etfMonth;tradeDay{1}];
        figure;
        candle(highTem,lowTem,closeTem,openTem);
%         plot(priceTem);
        title([endi{1},'--收益情况：',num2str(ReTem)]);
    end

    figure;
    winRatio=sum(Re>0)/length(Re);
    ReCS=cumsum(Re)+10000;
    plot(ReCS);
    grid on;
    Lre=length(Re);
    step=max(floor(Lre/10),1);
    set(gca,'xtick',1:step:Lre);
    set(gca,'xticklabel',etfMonth(1:step:Lre),'XTickLabelRotation',60);
    maxDown=0;
    ReCS=[0;ReCS];
    for i=2:Lre
        tem=max(ReCS(1:i))-ReCS(i);
        if tem>maxDown
            maxDown=tem;
        end
    end
    title(sprintf('年化收益估算：%.2f%%;最大回撤：%.2f%%;胜率：%.2f%%',100*((ReCS(end)/10000)^(1/((datenum(etfMonth(end))-datenum(etfMonth(1)))/360))-1), maxDown/100,winRatio*100));
end


    
    
    
    
    
    
    
    
    
    
    