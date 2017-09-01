function TrainModel % copy from TestModel;
tic;
fig=1;figNum=20;figNumi=0;%get data from model;
NameModel='TrainModel';
transferM_M=['E:\Matlab2Python\',NameModel];     % transfer between matlab;
%% get data from model;
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
Rall=zeros(2000000,5);
dateAll=cell(2000000,1);
Matrix=zeros(2000000,31); % for indicators
iRall=0;
iStart=1;
iEnd=Lstocks;%1980
for i=iStart:iEnd
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
    maN=zeros(L,1);
    ma10=zeros(L,1);
    for ii=11:L
        maN(ii)=mean(close(ii-3:ii));
        ma10(ii)=mean(close(ii-10:ii));        
    end

    for ii=15:L-5
        if low(ii-3)<=min(low(ii-5:ii))&&high(ii-2)>high(ii-3)&&high(ii-1)>high(ii)&&low(ii-1)>low(ii)&&...
                min(vol(ii-2:ii-1))>max(vol([ii,ii-3])) && high(ii-3)>low(ii-3)&&high(ii-2)>low(ii-2)&&high(ii-1)>low(ii-1)&&high(ii)>low(ii)
            iRall=iRall+1;
            if close(ii+1)>close(ii)
                Rtem=close(ii+2)/close(ii);
            else
                Rtem=close(ii+1)/close(ii);
            end
            Rall(iRall,:)=[Rtem,close(ii+2)/close(ii),close(ii+2)/close(ii),close(ii+2)/close(ii+1),close(ii+3)/close(ii+1)]-1;
            dateAll(iRall)=datei(ii);   
            Matrix(iRall,:)=[ corr2([low(ii-3),open(ii-3),close(ii-3),high(ii-3)],[low(ii),close(ii),open(ii),high(ii)]),...
                corr2([low(ii-2),open(ii-2),close(ii-2),high(ii-2)],[low(ii-1),close(ii-1),open(ii-1),high(ii-1)]),...
                corr2([low(ii-3),open(ii-3),close(ii-3),high(ii-3),low(ii-2),open(ii-2),close(ii-2),high(ii-2)],[low(ii),close(ii),open(ii),high(ii),low(ii-1),close(ii-1),open(ii-1),high(ii-1)]),...
                vol(ii)/vol(ii-3),vol(ii)/vol(ii-2),vol(ii)/vol(ii-1),vol(ii-1)/vol(ii-3),vol(ii-1)/vol(ii-2),vol(ii-2)/vol(ii-3),(vol(ii)+vol(ii-1))/(vol(ii-3)+vol(ii-2)),...
                high(ii)/high(ii-1),high(ii)/open(ii-1),high(ii)/low(ii-1),high(ii)/close(ii-1),...
                low(ii)/high(ii-1),low(ii)/open(ii-1),low(ii)/low(ii-1),low(ii)/close(ii-1),...
                open(ii)/high(ii-1),open(ii)/open(ii-1),open(ii)/low(ii-1),open(ii)/close(ii-1),...
                close(ii)/high(ii-1),close(ii)/open(ii-1),close(ii)/low(ii-1),close(ii)/close(ii-1),...
                mean(close(ii-4:ii))/mean(close(ii-9:ii)),mean(high(ii-4:ii))/mean(high(ii-9:ii)),...
                std(close(ii-4:ii))/std(close(ii-9:ii)),std(high(ii-4:ii))/std(high(ii-9:ii)),...
                std([ close(ii),open(ii),high(ii),low(ii) ])/std([close(ii-1),open(ii-1),high(ii-1),low(ii-1)]) ];  
            if fig && figNumi<figNum
                figNumi=figNumi+1;
                figure;
                a1=subplot(3,1,[1,2]);
                candle(high(ii-10:ii+2),low(ii-10:ii+2),close(ii-10:ii+2),open(ii-10:ii+2));
                grid on;
                a2=subplot(313);
                bar(vol(ii-10:ii+2));
                grid on;
                linkaxes([a1,a2],'x');
                %linkprop([a1,a2],'xlim');%ylim
            end
        end
    end
end
Rall=Rall(1:iRall,:);
dateAll=dateAll(1:iRall);
Matrix=Matrix(1:iRall,:);
save(transferM_M,'Rall','dateAll','Matrix');
fprintf('get %d records in all.',iRall);
%     dlmwrite('D:\Trading\hmmMatlabIn.txt',MatrixSpring,'delimiter',',','precision','%.5f','newline','pc');
%     msgbox('Needed data is prepared now,please run ''D:\Trading\Python\machinelearning\hmmSpring.py'' to train model and select good type CTA!');
figure;
RTem=Rall(:,1);
[tem1,tem2]=statisticTrading(RTem);
legend(tem1,tem2);
figure;
RTem=Rall(:,2);
[tem1,tem2]=statisticTrading(RTem);
legend(tem1,tem2);
toc;
end

function [Line,Lege]=statisticTrading(R)
Lt=length(R);
IR=mean(R)/std(R);
winRatio=sum(R>0)/Lt;
ratioWL=-mean(R(R>0))/mean(R(R<0));
R=cumsum(R);
maxDraw=0;
indDraw=1;
pointDraw=0;
for i=2:Lt
    drawTem=max(R(1:i))-R(i);
    if drawTem>maxDraw
        maxDraw=drawTem;
        indDraw=i;
        pointDraw=R(i);
    end
end
Line=plot(R);
try
    hold on;
    plot(indDraw,pointDraw,'r*');
end
Lege=sprintf('Orders:%d; IR:%.4f; winRatio(ratioWL):%.2f%%(%.2f);\nmaxDraw:%.2f%%; profitP: %.4f%%'...
    ,Lt,IR,winRatio*100,ratioWL,maxDraw*100,R(end)*100/length(R));
grid on;
end


