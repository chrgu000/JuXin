function OptionsTrading
sw1=0;% show arbitrage history of a options' pair,same time for different buy/sell price;
sw2=1;% test arbitrage space for pairs of options;
% sw3=0;
if sw1
    option1='10000727.sh';%2.495A 10000765.sh
    option2='10000731.sh';%2.5 10000801.sh
    startT='20170510'; %20161130
    endT='20170605';
    w=windmatlab;
    [OP1,~,~,Time1]=w.wsi(option1,'open,close',startT,endT,'periodstart=09:30:00;periodend=15:00:00');
    [OP2,~,~,Time2]=w.wsi(option2,'open,close',startT,endT,'periodstart=09:30:00;periodend=15:00:00');
    priceTem=w.wss({option1,option2},'exe_price');
    [Time,ind1,ind2]=intersect(Time1,Time2);
    OP1=OP1(ind1,:)+priceTem(1);
    OP2=OP2(ind2,:)+priceTem(2);
    OP=(OP1-OP2)*10000;
    Time=floor(Time);
    Days=unique(Time);
    L=length(Days);
    fi=1;
    for i=1:3:L
        try
            ind=Time==Days(i)|Time==Days(i+1)|Time==Days(i+2);
        catch
            try
                ind=Time==Days(i)|Time==Days(i+1);
            catch
                ind=Time==Days(i);
            end
        end
        op=OP(ind,2);
        fTem=mod(fi,2);
        if fTem==1
            figure;
            set(gcf,'position',[100,100,1800,900]);
        else
            fTem=2;
        end
        subplot(2,1,fTem);
        plot(op);
        grid on;
        fi=fi+3;
    end   
elseif sw2
    Date='20160608';
    BoS=1;%1--buy(认购),-1--sell(认沽);
    w=windmatlab;
    parameters=['date=',Date,';','us_code=510050.SH;option_var=全部;call_put=全部;field=option_code,strike_price,month,call_put,first_tradedate,last_tradedate'];
    data=w.wset('optionchain',parameters);
    options=data(:,1);
    prices=cell2mat(data(:,2));
    months=cell2mat(data(:,3));
    calls=data(:,4);
    starts=data(:,5);
    ends=data(:,6);
    monthU=unique(months);
    L=length(monthU);
    for i=1:L
        if BoS==1
            sign=1;
            ind=months==monthU(i)&strcmp(calls,'认购');
        else
            sign=-1;
            ind=months==monthU(i)&strcmp(calls,'认沽');
        end        
        option=options(ind);
        price=prices(ind);
        startT=starts(ind);
        endT=ends(ind);
        startT=startT(1);
        endT=endT(1);
        Lop=length(option);
        while 1
%             etf50=w.wsi('510050.sh','close',startT,endT,'periodstart=09:30:00;periodend=15:00:00','BarSize=60');%;Fill=Previous
            etf50=w.wsd('510050.sh','close',startT,endT);%;Fill=Previous
            if size(etf50,1)>1
                break;
            end
        end
        while 1
%             [op1,~,~,Time]=w.wsi(option(1),'close',startT,endT,'periodstart=09:30:00;periodend=15:00:00','BarSize=60');%;Fill=Previous
            [op1,~,~,Time]=w.wsd(option(1),'close',startT,endT);%;Fill=Previous
            if size(op1,1)>1
                op1=sign*op1+price(1);
                break;
            end
        end
        datai=zeros(size(op1,1),Lop)*nan;
        datai(:,1)=op1;
        for ii=2:Lop
            while 1
%                 opT=w.wsi(option(ii),'close',startT,endT,'periodstart=09:30:00;periodend=15:00:00','BarSize=60');%;Fill=Previous
                opT=w.wsd(option(ii),'close',startT,endT);%;Fill=Previous
                if size(opT,1)>1
                    opT=sign*opT+price(ii);
                    break;
                end                 
            end
            Ltem=length(opT);
            datai(end-Ltem+1:end,ii)=opT;           
        end
        nk=nchoosek(1:Lop,2);
        Lnk=length(nk);
        fi=1;
        for ii=1:Lnk
            indA=nk(ii,1);
            indB=nk(ii,2);
            opA=datai(:,indA);
            indT=isnan(opA);
            opA=opA(~indT);
            La=length(opA);
            opB=datai(:,indB);
            indT=isnan(opB);
            opB=opB(~indT);
            Lb=length(opB);
            Lab=min(La,Lb);
            Day=floor(Time(end-Lab+1:end));
            op=(opA(end-Lab+1:end)-opB(end-Lab+1:end))*10000;
            etf50Tem=etf50(end-Lab+1:end);
            fTem=mod(fi,6);
            if fTem==1
                figure;
                set(gcf,'position',[100,100,1800,900]);
            elseif fTem==0
                fTem=6;
            end
            subplot(2,3,fTem);
            lineB=ones(Lab,1)*price(indA);
            lineU=ones(Lab,1)*price(indB);
            lineZ=zeros(Lab,1);
            lineD=ones(Lab,1)*(price(indA)-price(indB))*10000;
            op=[op,lineZ,lineD];
            [AX,H1,H2]=plotyy(1:Lab,op,1:Lab,[etf50Tem,lineB,lineU]);
            set(H1,'color','k');
            set(H2(1),'color','r');
            set(H2(2:3),'color','r','linestyle','--');
            step=floor(Lab/4);
            set(gca,'xtick',1:step:Lab);
            set(gca,'xticklabel',cellstr(datestr(Day(1:step:Lab),'yyyy-mm-dd')));
            yL=get(AX(1),'ylim');
            step=floor((yL(2)-yL(1))/10);
            set(AX(1),'ytick',yL(1):step:yL(2));
            yR=get(AX(2),'ylim');
            step=(yR(2)-yR(1))/10;
            set(AX(2),'ytick',yR(1):step:yR(2));            
%             text(Lab,min(op),strcat(option(indA),':',num2str(price(indA))));
%             text(Lab,max(op),strcat(option(indB),':',num2str(price(indB))));
            title(endT);
            grid on;     
            fi=fi+1;
        end        
    end
elseif 0
    %% initiate environment;
    w=windmatlab;
    try
        load Options;
        DateTest=datestr(today,'yyyymmdd');
        if ~strcmp(Date,DateTest);
            DateTest+2.3;% go to catch;
        end
    catch
        display('run catch!');
        Date=datestr(today,'yyyymmdd');
        parameters=['date=',Date,';','us_code=510050.SH;option_var=全部;call_put=全部;field=option_code,strike_price,month,call_put'];
        data=w.wset('optionchain',parameters);
        Date=datestr(today,'yyyymmdd');
        save Options data Date;        
    end
    %% loop below code;
    dataNow=w.wsq(data(:,1),'rt_latest,rt_vol');
    indTem=strcmp(data(:,4),'认购')&dataNow(:,2)>10000;    
    indTemS=strcmp(data(:,4),'认沽')&dataNow(:,2)>1000; 
    dataNow=dataNow(:,1);
    optionBuy=data(indTem,1);
    optionSell=data(indTemS,1);
    BuyP=data(indTem,2);
    SellP=data(indTemS,2);
    priceBuy=cell2mat(BuyP)+dataNow(indTem);
    priceSell=cell2mat(SellP)-dataNow(indTemS);
    monthBuy=cell2mat(data(indTem,3));
    monthSell=cell2mat(data(indTemS,3));
    months=unique(monthBuy);
    monthsS=unique(monthSell);
    L=length(months);
    for i=1:L
        ind=monthBuy==months(i);
        price=priceBuy(ind);
        priceS=BuyP(ind);
        option=optionBuy(ind);
        [~,ind]=sort(price);
        display(strcat(num2str(priceS{ind(1)}),',','buy--',option(ind(1)),'; ',num2str(priceS{ind(end)}),' sell--',...
            option(ind(end)),':',num2str((price(ind(end))- price(ind(1)))*10000)));
    end
    L=length(monthsS);
    for i=1:L
        ind=monthSell==monthsS(i);
        price=priceSell(ind);
        priceS=SellP(ind);
        option=optionSell(ind);
        [~,ind]=sort(price);
        display(strcat(num2str(priceS{ind(end)}),',','buy--',option(ind(end)),'; ',num2str(priceS{ind(1)}),' sell--',...
            option(ind(1)),':',num2str((price(ind(end))- price(ind(1)))*10000)));
    end
    %%
end



end