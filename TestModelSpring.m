function TestModelSpring
tic;
sw1=1;%get data from model;
sw2=1;%show results according to different days;
%% get data from model;
if sw1
    global high low close open vol;
    try
        load allStocks1;
        load allStocks2;
        load allStocks3;
    catch
        w=windmatlab;
        dataTem=w.wset('sectorconstituent','a001010100000000');
        stocks=dataTem(:,2);
        Lt=length(stocks);
        Date=w.tdays('ED-3000TD',today-1);
        opens=[];
        closes=[];
        highs=[];
        lows=[];
        vols=[];
        turns=[];
        for i=1:400:Lt
            if i+399<=Lt
                iend=i+399;
            else
                iend=Lt;
            end
            while 1
                openT=w.wsd(stocks(i:iend),'open','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
                if length(openT)>1
                    break;
                end
            end
            while 1
                closeT=w.wsd(stocks(i:iend),'close','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
                if length(closeT)>1
                    break;
                end
            end
            while 1
                highT=w.wsd(stocks(i:iend),'high','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
                if length(highT)>1
                    break;
                end
            end
            while 1
                lowT=w.wsd(stocks(i:iend),'low','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
                if length(lowT)>1
                    break;
                end
            end
            while 1
                volT=w.wsd(stocks(i:iend),'volume','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
                if length(volT)>1
                    break;
                end
            end     
            while 1
                turnT=w.wsd(stocks(i:iend),'free_turn','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
                if length(turnT)>1
                    break;
                end
            end  
            opens=[opens,openT];
            closes=[closes,closeT];
            highs=[highs,highT];
            lows=[lows,lowT];
            vols=[vols,volT];
            turns=[turns,turnT];
        end    
        save allStocks1 stocks Date opens closes;
        save allStocks2 highs lows;
        save allStocks3 vols turns;
    end
    Lstocks=size(opens,2);
    Rall=zeros(500000,1);
    dateAll=cell(500000,1);
    Matrix=zeros(500000,5);
    MatrixSpring=zeros(500000,13);%col-1:return from one trading day ago;col-2:return from 5 trading days ago;col-3:return between high and low of current trading day;col-4:return between  next trading day and current trading day
    iRall=0;
    Radd=[];
    DaysAdd=0;

    iStart=1;
    iEnd=Lstocks;%1980
    % iStart=100; % draw picture;
    % iEnd=500;
    keyTest=0;

    if iEnd-iStart<50
        fig=1;
    else
        fig=0;
    end
    listCorr=[];
    for i=iStart:iEnd
    % for i=1:1
    %     w=windmatlab;
    %     endStr=datestr(today-1,'yyyymmdd');
    %     [dataTem,~,~,Date]=w.wsi('zn.shf','open,close,high,low,volume','20140101 09:00:00',[endStr,'15:01:00'],...
    %         'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F','BarSize=15');
    %     opens=dataTem(:,1);
    %     closes=dataTem(:,2);
    %     highs=dataTem(:,3);
    %     lows=dataTem(:,4);    
    %     vols=dataTem(:,5);
    % %     if i>1329
    % %         continue;
    % %     end
        open=opens(:,i);
        close=closes(:,i);
        high=highs(:,i);
        low=lows(:,i);
        vol=vols(:,i);   
        turn=turns(:,i);
        datei=Date;
        indTem=~isnan(open);
        open=open(indTem);
        close=close(indTem);
        high=high(indTem);
        low=low(indTem);
        vol=vol(indTem);
        turn=turn(indTem);
        datei=datei(indTem);

        L=length(high);
        indTarget=[];
        Target=[];
        Ri=[];
        indAdd={};
        Add={};

        maN=zeros(L,1);
        ma10=zeros(L,1);
        for ii=11:L
            maN(ii)=mean(close(ii-3:ii));
            ma10(ii)=mean(close(ii-10:ii));        
        end

        for ii=20:L-2
            switch keyTest
                case  0
                    lowTest=low(ii)/low(ii-1)-1;
                    if close(ii-1)<low(ii-1)+(high(ii-1)-low(ii-1))*0.25 &&close(ii)/close(ii-1)-1<0.095&&high(ii)>low(ii)...%&&close(ii)>low(ii)+(high(ii)-low(ii))*0.1
                            &&close(ii)/close(ii-1)-1>=0.025&&close(ii)/close(ii-1)-1<0.055...
                            && lowTest>=0.01%&&lowTest<-0.01 % 
                            %&&close(ii)>maN(ii)%&&close(ii)<high(ii-1) %&&high(ii-1)<high(ii-2)&&low(ii)>low(ii-1)&& close(ii)>low(ii-1)+(high(ii-1)-low(ii-1))*0.5%                    
                        daysHold=1;
                        RTem=close(ii+daysHold)/close(ii);
                        indTarget=[indTarget,[ii;ii+daysHold]];
                        Target=[Target,[close(ii);close(ii+daysHold)]]; 
                        iRall=iRall+1;
                        Rall(iRall)=RTem;
                        Matrix(iRall,:)=[close(ii),close(ii-1),close(ii-5),high(ii),low(ii)];
                        MatrixSpring(iRall,:)=[close(ii+2)/close(ii)-0.003,close(ii+3)/close(ii+1)-0.003,(close(ii)-low(ii))/(high(ii)-low(ii)),std([close(ii);open(ii);low(ii);high(ii)])/std([close(ii-1);open(ii-1);low(ii-1);high(ii-1)]),maN(ii)/ma10(ii),close(ii)/close(ii-4),high(ii)/high(ii-1),low(ii)/low(ii-1),close(ii)/close(ii-2),close(ii)/low(ii-1),close(ii)/high(ii-1),close(ii)/mean([low(ii-1),high(ii-1)]),close(ii+2)/open(ii+1)-0.003]-1;
                        dateAll(iRall)=datei(ii);   
                    end
            end
        end

        if fig
            numberFig=size(indTarget,2);
            for i2=1:numberFig
                figure;
                ax1=subplot(3,1,1:2);
                figStart=indTarget(1,i2)-10;
                candle(high(figStart:figStart+20),low(figStart:figStart+20),close(figStart:figStart+20),open(figStart:figStart+20));
                try
                    listCorrStr=sprintf('%.3f ',listCorr(i2,:));
                catch
                    listCorrStr='no calculation';
                end           
                title(strcat(stocks(i),';listCorr: ',listCorrStr));
                grid on;
                hold on;
                lowTem=low(figStart:figStart+20);
                indTem=[11;11+indTarget(2,i2)-indTarget(1,i2)];
                line(indTem,Target(:,i2),'color','r');
                plot(indTem(1,:),lowTem(indTem(1,:)),'r*');
                plot(indTem(2,:),lowTem(indTem(2,:)),'k*');
                try
                    indAddTem=indAdd{i2}+11;
                    AddTem=Add{i2};                
                    line(indAddTem,AddTem,'color','b');
                    plot(indAddTem(1,:),lowTem(indAddTem(1,:)),'b*');
                end
                ax2=subplot(3,1,3);
                bar(vol(figStart:figStart+20));
                grid on;
                linkaxes([ax1,ax2],'x');   
            end
        end
    end
    
    MatrixSpring=[MatrixSpring(1:iRall,:),datenum(dateAll(1:iRall))];
    dlmwrite('D:\Trading\hmmMatlabIn.txt',MatrixSpring,'delimiter',',','precision','%.5f','newline','pc');
    msgbox('Needed data is prepared now,please run ''D:\Trading\Python\machinelearning\hmmSpring.py'' to train model and select good type CTA!');
    RTem=MatrixSpring(:,1);
    figure;
    statisticTrading(RTem);
%% show results according to different days;
elseif sw2
    dataTem=importdata('D:\Trading\hmmMatlabOut.txt');
    Rall=dataTem(:,1);
    R2all=dataTem(:,2);
    dateAll=dataTem(:,3);
    figure;
    set(gcf,'position',[50,100,1800,900]);
    weekDays=weekday(dateAll);
    months=month(dateAll);
    monthDays=day(dateAll);

    Lt=length(Rall);
    R=Rall;
    Rtem=[];
    for i=1:Lt
        if ismember(weekDays(i),[2,3,4])  && (ismember(monthDays(i),[10,16,17,25,30]) && ismember(months(i),[6,9]))
            R(i)=-2;
            Rtem=[Rtem,Rall(i)];
        end
    end   
    fprintf(2,'orders:%d;IR:%.4f;winRatio:%.2f%%;profitP:%.2f%%\n',length(Rtem),mean(Rtem)/std(Rtem),sum(Rtem>0)*100/length(Rtem),mean(Rtem)*100);    
    R=R(R>-1);
    if ~isempty(R)
        statisticTrading(R);
        xlabel('Rall Selected');
    end
    
    figure;
    set(gcf,'position',[50,100,1800,900]);
    for i=1:6 % Rall and Rweekday;
        subplot(2,3,i);
        if i==1
            R=Rall;  
            R=R(indTem);
        else
            indTem=weekDays==i;
            R=Rall(indTem);
        end
        if ~isempty(R)
            statisticTrading(R);
            if i==1
                xlabel('Rall Test');
            else
                xlabel(['week day: ',num2str(i-1)]);
            end
        else
            toc;
            return;
        end
    end
    for i=1:12 % Rmonth;
        iMod=mod(i,6);
        if iMod==1
            figure;
            set(gcf,'position',[50,100,1800,900]);
        elseif iMod==0
            iMod=6;
        end
        subplot(2,3,iMod);
        indTem=months==i;
        R=Rall(indTem); 
        if ~isempty(R)
            statisticTrading(R);
            xlabel(['month: ',num2str(i)]);
        end
    end
    for i=1:31 % Rmonthday;    
        iMod=mod(i,6);
        if iMod==1
            figure;
            set(gcf,'position',[50,100,1800,900]);
        elseif iMod==0
            iMod=6;
        end
        subplot(2,3,iMod);
        indTem=monthDays==i;
        R=Rall(indTem);
        if ~isempty(R)
            statisticTrading(R);
            xlabel(['monthday: ',num2str(i)]);
        end
    end
end

% if ~isempty(Radd)
%     statisticTrading(Radd,DaysAdd);
% end
toc;
end

function statisticTrading(R)
Lt=length(R);
IR=mean(R)/std(R);
winRatio=sum(R>0)/Lt;
ratioWL=-mean(R(R>0))/mean(R(R<0));
R=cumsum(R);
maxDraw=0;
indDraw=0;
pointDraw=0;
for i=2:Lt
    drawTem=max(R(1:i))-R(i);
    if drawTem>maxDraw
        maxDraw=drawTem;
        indDraw=i;
        pointDraw=R(i);
    end
end
plot(R);
try
    hold on;
    plot(indDraw,pointDraw,'r*');
end
strTitle=sprintf('Orders:%d; IR:%.4f; winRatio(ratioWL):%.2f%%(%.2f);\nmaxDraw:%.2f%%; profitP: %.4f%%'...
    ,Lt,IR,winRatio*100,ratioWL,maxDraw*100,R(end)*100/length(R));
title(strTitle);
grid on;
end


