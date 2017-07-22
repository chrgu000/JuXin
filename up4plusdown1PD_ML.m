function test=up4plusdown1PD_ML(varargin) 
tic;
test=0;
global date high low close open vol;
%% Get data
if nargin>0
    updateB='y';    
else
    updateB='n';
end   
    
h=waitbar(0,'Test starts......');
if updateB=='y'
    display('test succeed!');
    waitbar(0,h,'Read in data for running......');
    w=windmatlab;
    dataTem=w.wset('SectorConstituent');
    stocks=dataTem(:,2);
    stocks=[stocks',{'000300.sh','510050.sh','000905.sh','000016.sh','512510.sh','IF00.CFE','IC00.CFE','IH00.CFE',...
        'IF01.CFE','IC01.CFE','IH01.CFE','IF02.CFE','IC02.CFE','IH02.CFE','IF03.CFE','IC03.CFE','IH03.CFE',...
        'IF04.CFE','IC04.CFE','IH04.CFE'}];
    
%     load up4plusdown1Data;
%     stocks=stocksGroup5;
    
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
delete('D:\Trading\up4plusdown1DataML.txt');
for S=1:numStocks
    sample1=[];
    sample0=[];
    open=Open(:,S);
    indTem=isnan(open)<1;
    date=Date(indTem);
    open=open(indTem);
    close=Close(indTem,S);
    high=High(indTem,S);
    low=Low(indTem,S);
    vol=Volume(indTem,S);
    Ldays=length(open);
    for i=20:Ldays-5
        downNow=max(high(i-4:i-1))-low(i);
        downs=[max(high(i-4:i-2))-low(i-1),max(high(i-4:i-3))-low(i-2),max(high(i-5:i-4))-low(i-3),high(i-5)-low(i-4)];
        if close(i-1)>open(i-1) && close(i-2)>open(i-2) && close(i-3)>open(i-3) && close(i-4)>open(i-4) &&...% continuous ups(close>open)
                downNow>1*max(downs)&&low(i)>min(low(i-4:i-1))&&...%big down happens;
                close(i)<low(i)+0.25*(high(i)-low(i))
            
            sampleT=[vol(i)/vol(i-1),vol(i)/mean(vol(i-3:i-1))];
            
%             baseP=open(i);
%             baseV=vol(i);
%             sampleT=[ %open(i-4)/baseP,open(i-3)/baseP,open(i-2)/baseP,open(i-1)/baseP,...
%                       low(i-4)/baseP,low(i-3)/baseP,low(i-2)/baseP,low(i-1)/baseP,...
%                       high(i-4)/baseP,high(i-3)/baseP,high(i-2)/baseP,high(i-1)/baseP,...
%                       vol(i-4)/baseV,vol(i-3)/baseV,vol(i-2)/baseV,vol(i-1)/baseV,...
%                       close(i-4)/baseP,close(i-3)/baseP,close(i-2)/baseP,close(i-1)/baseP ]-1;
%             lowBar=lowest(i-10,i);
%             highBar=highest(lowBar,i);
%             uplen=high(highBar)-low(lowBar);
%             downlen=high(highBar)-low(i);
%             volratio=vol(i)/mean(vol(lowBar:highBar));
%             sampleT=[sampleT,std([open(i),low(i),high(i),close(i)]),std([open(i-1),low(i-1),high(i-1),close(i-1)]),...
%                 std([open(i-2),low(i-2),high(i-2),close(i-2)]),(i-lowBar)/10,downlen/uplen,volratio ];
                  
%             if high(i+1)>high(i)
            if close(i+1)>=close(i)
                sample1=[sample1;sampleT];
            else
                sample0=[sample0;sampleT];
            end         
        end
    end
    sample0=[sample0,zeros(size(sample0,1),1)];
    sample1=[sample1,ones(size(sample1,1),1)];
    Ltem1=size(sample1,1);
    Ltem2=size(sample0,1);
    Ltem=min(Ltem1,Ltem2);
%     dlmwrite('D:\Trading\up4plusdown1DataML.txt', [sample0(1:Ltem,:);sample1], 'newline','pc','-append');
    dlmwrite('C:\Users\Administrator\Desktop\up4plusdown1DataML.txt', [sample0(1:Ltem,:);sample1], 'newline','pc','-append');
    
    temBar=S/numStocks;
    temBar=roundn(temBar,-4);
    tem=toc;
    temTime=roundn(tem/60,-1);  
    waitbar(temBar,h,['Completed...',num2str(100*temBar),'%; Time lapses:',num2str(temTime),' minutes.']);    
end
pause(1);
delete(h);
end


% function up4plusdown1PD_ML 
% tic;
% global date high low close open vol;
% %% Get data
% updateB=input('update data or not? y/n [n]:','s');
% h=waitbar(0,'Test starts......');
% if updateB=='y'
%     waitbar(0,h,'Read in data for running......');
%     w=windmatlab;
%     dataTem=w.wset('SectorConstituent');
%     stocks=dataTem(:,2);
%     numStocks=length(stocks);
%     Open=zeros(4000,numStocks);
%     Close=zeros(4000,numStocks);
%     High=zeros(4000,numStocks);
%     Low=zeros(4000,numStocks);
%     Volume=zeros(4000,numStocks);
%     for ii=1:150:numStocks
%         if ii+150<numStocks
%             Open(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'open','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%             Close(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'close','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%             High(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'high','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%             Low(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'low','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%             Volume(:,ii:ii+150)=w.wsd(stocks(ii:ii+150),'volume','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%         else
%             Open(:,ii:end)=w.wsd(stocks(ii:end),'open','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%             Close(:,ii:end)=w.wsd(stocks(ii:end),'close','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%             High(:,ii:end)=w.wsd(stocks(ii:end),'high','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%             Low(:,ii:end)=w.wsd(stocks(ii:end),'low','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%             Volume(:,ii:end)=w.wsd(stocks(ii:end),'volume','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%         end
%     end
%     [~,~,~,Date]=w.wsd('000001.sh','open','ED-3999TD',today-1,'Fill=Previous','PriceAdj=F');
%     save('e:\testAllData', 'Date','Open', 'Close', 'High', 'Low', 'Volume','stocks');
% else
%     load('e:\testAllData');
%     numStocks=length(stocks);
% end
% delete('D:\Trading\up4plusdown1DataML.txt');
% for S=1:numStocks
%     sample1=[];
%     sample0=[];
%     open=Open(:,S);
%     indTem=isnan(open)<1;
%     date=Date(indTem);
%     open=open(indTem);
%     close=Close(indTem,S);
%     high=High(indTem,S);
%     low=Low(indTem,S);
%     vol=Volume(indTem,S);
%     Ldays=length(open);
%     for i=11:Ldays-1
%         downNow=max(high(i-4:i-1))-low(i);
%         downs=[max(high(i-4:i-2))-low(i-1),max(high(i-4:i-3))-low(i-2),max(high(i-5:i-4))-low(i-3),high(i-5)-low(i-4)];
%         if close(i-1)>open(i-1) && close(i-2)>open(i-2) && close(i-3)>open(i-3) && close(i-4)>open(i-4) &&...% continuous ups(close>open)
%                 downNow>1*max(downs)&&low(i)>min(low(i-4:i-1))&&...%big down happens;
%                 close(i)<low(i)+0.25*(high(i)-low(i))
%             lowBar=lowest(i-10,i);
%             highBar=highest(lowBar,i);
%             uplen=high(highBar)-low(lowBar);
%             downlen=high(highBar)-low(i);
%             volratio=vol(i)/mean(vol(lowBar:highBar));
%             sampleT=[(i-lowBar)/10,open(i)/high(i),downlen/uplen,volratio ];
% %             sampleT=[ open(i-4)/baseP,open(i-3)/baseP,open(i-2)/baseP,open(i-1)/baseP,...
% %                       close(i-4)/baseP,close(i-3)/baseP,close(i-2)/baseP,close(i-1)/baseP,...
% %                       high(i-4)/baseP,high(i-3)/baseP,high(i-2)/baseP,high(i-1)/baseP,...
% %                       low(i-4)/baseP,low(i-3)/baseP,low(i-2)/baseP,low(i-1)/baseP,...
% %                       vol(i-4)/baseV,vol(i-3)/baseV,vol(i-2)/baseV,vol(i-1)/baseV ]-1;
% 
% %             if close(i+1)/close(i)-1>0.003
%             if close(i+1)>=open(i)
%                 sample1=[sample1;sampleT];
%             else
%                 sample0=[sample0;sampleT];
%             end         
%         end
%     end
%     sample0=[sample0,zeros(size(sample0,1),1)];
%     sample1=[sample1,ones(size(sample1,1),1)];
%     Ltem1=size(sample1,1);
%     Ltem2=size(sample0,1);
%     Ltem=min(Ltem1,Ltem2);
%     dlmwrite('D:\Trading\up4plusdown1DataML.txt', [sample0(1:Ltem,:);sample1], 'newline','pc','-append');
%     
%     temBar=S/numStocks;
%     temBar=roundn(temBar,-4);
%     tem=toc;
%     temTime=roundn(tem/60,-1);  
%     waitbar(temBar,h,['Completed...',num2str(100*temBar),'%; Time lapses:',num2str(temTime),' minutes.']);    
% end
% pause(1);
% delete(h);
% end
% 
