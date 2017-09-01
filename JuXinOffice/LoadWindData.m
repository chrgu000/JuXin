function op=LoadWindData
op=1;
w=windmatlab;
[~,stocks]=xlsread('D:\Trading\WFT\stocks.xlsx');
newStocks=w.wset('sectorconstituent');
newStocks=newStocks(:,2);
newAdd=setdiff(newStocks,stocks);
stocks=[stocks;newAdd];
xlswrite('D:\Trading\WFT\stocks.xlsx',stocks);
fileName='E:\MinuteData\';
L=length(stocks);

for i=1:L
    tic;   
    stockCode=stocks{i};
    if length(stockCode)==8
        stockName=stockCode(1:end-4);        
    elseif strcmp(stockCode(end-1:end),'SH') && stockCode(1)~='6'
        stockName=[stockCode(1:end-3),stockCode(end-1:end)];
    else
        stockName=stockCode(1:end-3);
    end
    
    savefile=[fileName,stockName];
    try
        load(['E:\MinuteData\',stockName]);
        tradeDays=w.tdays(today-12,today-1);
        if datenum(datestr(time(end),'yyyy-mm-dd'))==datenum(tradeDays(end))
            continue;
        end
        startDate=datestr(time(end)+1,'yyyy-mm-dd');
        endDate=datestr(today-1,'yyyy-mm-dd');
        while 1
            [data0,~,~,time0,werrors]=w.wsi(stocks(i),'open,close,high,low,volume',[startDate,' 09:00:00'],[endDate,' 15:00:00'],'periodstart=09:30:00;periodend=15:00:00;PriceAdj=F');
            if length(time0)>1
                indTem=~isnan(data0(:,1));
                data0=data0(indTem,:);
                time0=time0(indTem);
                data=[data;data0];
                time=[time;time0];
                break;
            end
            display(strcat(stocks(i),' failed; error number: ',num2str(werrors)));
        end
    catch
        while 1
            [data0,~,~,time0,werrors]=w.wsi(stocks(i),'open,close,high,low,volume','2010-01-01 09:00:00',[datestr(today-1,'yyyy-mm-dd'),' 15:00:00'],'periodstart=09:30:00;periodend=15:00:00;PriceAdj=F');
            if length(time0)>1
                indTem=~isnan(data0(:,1));
                data=data0(indTem,:);
                time=time0(indTem);
                break;
            end
            display(strcat(stocks(i),' failed; error number: ',num2str(werrors)));
        end
    end
    save(savefile,'data','time');    
    timeTem=toc;
    display(strcat(stocks(i),' i= ',num2str(i),' 耗时：',num2str(round(timeTem,1)),' 秒'));
end

% function op=LoadWindData
% op=1;
% w=windmatlab;
% [~,stocks]=xlsread('D:\Trading\WFT\股票代码.xlsx');
% filename='E:\MinuteData\';
% L=length(stocks);
% 
% for i=1:L
%     tic;
%     filepath=strcat(filename,stocks(i));
%     while  1
%         [data0,~,~,time0,werrors]=w.wsi(stocks(i),'open,close,high,low,volume','2014-04-18 09:00:00','2017-4-17 15:00:00','periodstart=09:30:00;periodend=15:00:00;PriceAdj=F');
%         if length(time0)>1
%             indTem=~isnan(data0(:,1));
%             data=data0(indTem,:);
%             time=time0(indTem);
%             break;
%         end
%         display(strcat(stocks(i),' failed; error number: ',num2str(werrors)));
%     end
%     stockCode=stocks{i};
%     if length(stockCode)==8
%         save(filepath{1}(1:end-4),'data','time');
%     elseif strcmp(stockCode(end-1:end),'SH') && stockCode(1)~='6'
%         save([filepath{1}(1:end-3),filepath{1}(end-1:end)],'data','time');
%     else
%         save(filepath{1}(1:end-3),'data','time');
%     end    
%     timeTem=toc;
%     display(strcat(stocks(i),' i= ',num2str(i),' 耗时：',num2str(round(timeTem,1)),' 秒'));
% 
% end