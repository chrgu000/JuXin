function op1=test2
tic;
%% Get data
% updateB=input('update data or not? y/n [n]:','s');
global open close high low vol;
updateB=0;
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
%     numStocks=100;
end
for j=3:6
for loop=1:numStocks % loop for all stocks;
    %% strategy codes 
    indTem=sum(isnan(Open(:,loop)))+1;
    open=Open(indTem:end,loop);
    close=Close(indTem:end,loop);
    high=High(indTem:end,loop);
    low=Low(indTem:end,loop);
    vol=Volume(indTem:end,loop);
    date=Date(indTem:end);
    
    L=length(open)-j;
    if L>30
        for i=3:10
            centerB=L-i;
            rightHB=highest(centerB,L);
            leftHB=highest(centerB-i,centerB);
            [~,leftHInd]=sort(high(leftHB:centerB));
            [~,rightHInd]=sort(high(centerB:rightHB));
            [~,leftLInd]=sort(low(leftHB:centerB));
            [~,rightLInd]=sort(low(centerB:rightHB));
            if low(centerB)==min(low(centerB-i:L))&& rightHB+leftHB==centerB*2 && ...
                    low(centerB-i)==min(low(centerB-3*i:leftHB)) && low(L)==min(low( rightHB:L ))&&rightHB~=L &&...
                    max(high(leftHB:rightHB)-low(leftHB:rightHB))>1.2*max([high(centerB-i:leftHB-1)-low(centerB-i:leftHB-1);high(rightHB+1:L)-low(rightHB+1:L)])&&...
                    ( all(leftHInd'==centerB-leftHB+1:-1:1) || all(leftLInd'==centerB-leftHB+1:-1:1) )&&...
                    ( all(rightHInd'==1:rightHB-centerB+1)  || all(rightLInd'==1:rightHB-centerB+1) )
                op1=1;
                X(1,1)=L-i;  Y(1,1)=low(L-i);
                X(2,1)=L;     Y(2,1)=low(L);
                [stocks(loop),datestr(date(L),'yyyy-mm-dd')]
                break;
            end
        end
    end
    %% for wait bar
    temBar=loop/numStocks;
    temBar=roundn(temBar,-4);
    tem=toc;
    temTime=roundn(tem/60,-1);  
    waitbar(temBar,h,['Completed...',num2str(100*temBar),'%; Time lapses:',num2str(temTime),' minutes.']);    
end
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

toc;
end


