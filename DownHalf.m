function op=DownHalf(varargin)
global high low;
stock=varargin{1};
w=windmatlab;
[rawData,~,~,date]=w.wsd(stock,'open,high,low,close,volume','2010-10-01',today-1,'Fill=Previous','PriceAdj=F');
% [rawData,~,~,date]=w.wsi(stock,'open,high,low,close,volume','2017-01-10 09:00:00','2017-04-20 15:15:22',...
%     'BarSize=30;periodstart=09:30:00;periodend=15:00:00;Fill=Previous;PriceAdj=F');
open=rawData(:,1);
indTem=sum(isnan(open))+1;
open=open(indTem:end);
date=date(indTem:end);
high=rawData(indTem:end,2);
low=rawData(indTem:end,3);
close=rawData(indTem:end,4);
vol=rawData(indTem:end,5);
L=length(open);
x=zeros(1,L);
y=zeros(1,L);
results=zeros(1,L);
j=1;
for i=35:L-3
    for ii=4:30
        lowB_1=i-ii;
        lowB_2=i;
        if low(lowB_1)==min(low(lowB_1-3:lowB_2)) % low point 1: i-ii; high point:highBar; low point 2: i; 
            highB=highest(lowB_1,lowB_2); % confirm high point
            halfRatio=(high(highB)/low(lowB_1)-1)/2;
            target=high(highB)*(1-halfRatio); % target price for half draw back;
%             target=(high(highB)+low(lowB_1))/2; % target price for half draw back;
            if lowB_2==highB
                continue;
            end

            diffLeft=highB-lowB_1;
            diffLeftT=diffLeft*4;
            if lowB_1-diffLeftT<1
                startBH=1;
            else
                startBH=lowB_1-diffLeftT;
            end
            if 2*lowB_1-lowB_2<1
                startBL=1;
            else
%                 startBL=2*lowB_1-lowB_2;
                startBL=lowB_1-3;
            end
            if low(lowB_1)<=min(low(startBL:lowB_1))... % confirm first low point is less than long time low point;
                    && high(highB)>max(high(startBH:lowB_1))... % confirm current high point is more than long time high point;
                    && low(i) == min(low(highB:i)) ... % confirm current low ;
                    && abs(low(i)-target)/target<0.005... % difference between target price and current low is less than 0.07 points;    
%                     && high(highB)/low(lowB_1)>1.1
                x(j)=i;
                y(j)=low(i);
                results(j)=close(i+1)/close(i)-1;
                j=j+1;
            end            
        end
    end
end
if nargin<2
    figure;
    ax1=subplot(4,1,1:3);
    candle(high,low,close,open);
    step=12;
    dateStr=cellstr(datestr(date,'yyyy-mm-dd'));
    set(gca,'XTick',[1:step:L,L]);
    set(gca,'Xticklabel',dateStr(1:step:L));
    hold on;
    plot(x(1:j-1),y(1:j-1),'*','Color','r')
    hold off;
    grid on;
    ax2=subplot(4,1,4);
    bar(vol);
    set(gca,'XTick',[1:step:L,L]);
    linkaxes([ax1,ax2],'x');
    grid on;
end
plus=sum(results>0);
winRatio=plus/(j-1);
results=results(1:j-1);
resultsRaw=results;
resultsSum=cumsum(results);
if ~isempty(resultsSum)
    sharpe=mean(resultsRaw)/std(resultsRaw);
    op=[winRatio,sharpe,j-1];
    if nargin<2
        figure;
        plot(1:j-1,resultsSum);
        set(gca,'XTick',1:j-1);
        grid on;
    end
else
    op=[0,0,0];
    display('There is not k line which fits to this module!');
end

end