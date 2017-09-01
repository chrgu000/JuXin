function OP=up4plusdown1TA
tic;
%% Get data
updateB=input('update data or not? y/n [n]:','s');
h=waitbar(0,'Test starts......');
if updateB=='y'
    waitbar(0,h,'Read in data for running......');
    w=windmatlab;
    dataTem=w.wset('SectorConstituent');
    stocks=dataTem(:,2);
    stocks=[stocks',{'000300.sh','510050.sh','000905.sh','000016.sh','512510.sh','IF00.CFE','IC00.CFE','IH00.CFE',...
        'IF01.CFE','IC01.CFE','IH01.CFE','IF02.CFE','IC02.CFE','IH02.CFE','IF03.CFE','IC03.CFE','IH03.CFE',...
        'IF04.CFE','IC04.CFE','IH04.CFE'}];
    numStocks=length(stocks);
    Open=zeros(4000,numStocks);
    Close=zeros(4000,numStocks);
    High=zeros(4000,numStocks);
    Low=zeros(4000,numStocks);
    Volume=zeros(4000,numStocks);
    for ii=1:150:numStocks
        if ii+150<numStocks
            Open(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'open','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
            Close(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'close','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
            High(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'high','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
            Low(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'low','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
            Volume(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'volume','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
        else
            Open(:,ii:end)=w.wsd(stocks(ii:end),'open','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
            Close(:,ii:end)=w.wsd(stocks(ii:end),'close','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
            High(:,ii:end)=w.wsd(stocks(ii:end),'high','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
            Low(:,ii:end)=w.wsd(stocks(ii:end),'low','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
            Volume(:,ii:end)=w.wsd(stocks(ii:end),'volume','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
        end
    end
    [~,~,~,Date]=w.wsd('000001.sh','open','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
    save('e:\testAllData', 'Date','Open', 'Close', 'High', 'Low', 'Volume','stocks');
else
    load('e:\testAllData');
    numStocks=length(stocks);
end
OP=zeros(numStocks,3);
for loop=1:numStocks % loop for all stocks;
    %% strategy codes 
    indTem=sum(isnan(Open(:,loop)))+1;
    open=Open(indTem:end,loop);
    close=Close(indTem:end,loop);
    high=High(indTem:end,loop);
    low=Low(indTem:end,loop);
    vol=Volume(indTem:end,loop);
    
    L=length(open);
    x=zeros(1,L);
    y=zeros(1,L);
    results=zeros(1,L);
    j=1;
    for i=6:L-3
        downNow=max(high(i-4:i-1))-low(i);
        downs=[max(high(i-4:i-2))-low(i-1),max(high(i-4:i-3))-low(i-2),max(high(i-5:i-4))-low(i-3),high(i-5)-low(i-4)];
        if close(i-1)>open(i-1) && close(i-2)>open(i-2) && close(i-3)>open(i-3) && close(i-4)>open(i-4) &&...% continuous ups(close>open)
                downNow>1*max(downs)&&low(i)>min(low(i-4:i-1))&&...%big down happens;
                close(i)<low(i)+0.25*(high(i)-low(i)) %&& (vol(i)/vol(i-1)<=0.65|| vol(i)/mean(vol(i-3:i-1))<0.65 )%(high(i)-low(i))>0.85*diff &&close(i) < low(i-4)+0.6*(high(i-1)-low(i-4))&&
            x(j)=i;
            y(j)=low(i);
            if open(i+1)<close(i)
                results(j)=0.5*(close(i+1)-close(i))/close(i);
                j=j+1;
                results(j)=0.5*(open(i+2)-open(i+1))/open(i+1);
                j=j+1;
            else
                results(j)=0.5*(close(i+1)-close(i))/close(i);
                j=j+1;
            end
        end
    end   
    plus=sum(results>0);
    winRatio=plus/(j-1);
    resultsRaw=results;
    results=results(1:j-1)+1;
    y=cumprod(results)-1;
    if ~isempty(y)
        sharpe=mean(resultsRaw)/std(resultsRaw);
        op=[winRatio,sharpe,j-1];
    else
        op=[0,0,0];
    end
    OP(loop,:)=op;    
    %% for wait bar
    temBar=loop/numStocks;
    temBar=roundn(temBar,-4);
    tem=toc;
    temTime=roundn(tem/60,-1);  
    waitbar(temBar,h,['Completed...',num2str(100*temBar),'%; Time lapses:',num2str(temTime),' minutes.']);    
end
delete(h)

% indTem=OP(:,2)>0.01&OP(:,3)>10&OP(:,1)>0.6;
% resultsGroup5=OP(indTem,:);
% % stocksAdd={'000300.sh','510050.sh','000905.sh','000016.sh','512510.sh'};
% stocksGroup5=stocks(indTem);
% % for i=1:length(stocksAdd)
% %     reTem=up4plusdown1(stocksAdd(i),2);
% %     resultsGroup5=[resultsGroup5;reTem];
% % end
% length(stocks(indTem))
% save up4plusdown1Data stocksGroup5 resultsGroup5;

op2=OP(:,2);
tem=isfinite(OP(:,2))&OP(:,3)>5;
tem=op2(tem);
x=sum(tem>0)
y=sum(tem<0)
x/y
toc;
end


