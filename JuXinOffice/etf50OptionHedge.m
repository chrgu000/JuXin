
function etf50OptionHedge
    stepShort=2; % gas between current value and void value;
    holdDays=15; % trading days from "short" to expire date;
    stopRatio=1.3;
    dateFrom='2014/1/1';
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
            'call_put=认沽;field=option_code,strike_price,month,call_put,first_tradedate,last_tradedate,option_name'];
        data=w.wset('optionchain',parameters);
        Data=[Data;data];
        if Date==today
            break;
        end       
    end
    optionsSell=Data(:,1);
    [optionsSell,indTem]=unique(optionsSell);
    Data=Data(indTem,:);
    pricesSell=cell2mat(Data(:,2));
    indTem=mod(pricesSell,0.05)<0.00000001;
    pricesSell=pricesSell(indTem);
    monthsSell=cell2mat(Data(indTem,3));    
    optionsSell=optionsSell(indTem);
        
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
        difftem=abs(priceT-etfP);
        [~,tem]=sort(difftem);
        optioni=optionT(tem(1));starti=startT(tem(1));endi=endT(tem(1));pricei=priceT(tem(1));
        tem=(pricesSell==pricei & monthsSell==UniMonth(i));
        optioni2=optionsSell(tem);
        Pall=w.wss(strcat(optioni,',',optioni2),'open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
        getMoney=(pricei+Pall(1)-Pall(2)-etfP)*10000;        
        tem_1=w.wss(optioni2,'open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
        etf50_1=w.wss('510050.SH','open',['tradeDate=',tradeDay{1}],'priceAdj=U','cycle=D');
        Re=[Re;getMoney/(commission(pricei,tem_1,etf50_1)+etfP*10000)];
        etfMonth=[etfMonth;tradeDay{1}];
    end

    figure;
    winRatio=sum(Re>0)/length(Re);
    ReCS=cumsum(Re);
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
    title(sprintf('胜率：%.2f%%',winRatio*100));
end