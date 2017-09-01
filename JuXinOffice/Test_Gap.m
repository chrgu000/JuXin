function op=Test_Gap(stock)
w=windmatlab;
rawData=w.wsd(stock,'open,high,low,close,volume','2000-01-01',today-1,'Fill=Previous','PriceAdj=F');
open=rawData(:,1);
indTem=sum(isnan(open))+1;
open=open(indTem:end);
high=rawData(indTem:end,2);
low=rawData(indTem:end,3);
close=rawData(indTem:end,4);
vol=rawData(indTem:end,5);
L=length(open);
x=zeros(1,L);
y=zeros(1,L);
results=zeros(1,L);
j=1;
for i=3:L-3
    if (low(i-1)-open(i))/close(i-1)>=0.01 && vol(i-1)>1  && vol(i-1)<vol(i-2)*0.8 %&& vol(i-1) > vol(i-2)*0.5
        x(j)=i;
        y(j)=high(i);
        results(j)=(open(i+1)-open(i))/open(i);
        j=j+1;
    end
end
% candle(high,low,close,open);
% hold on;
% plot(x(1:j-1),y(1:j-1),'*','Color','r')
plus=sum(results>0);
winRatio=plus/(j-1);
results=results(1:j-1)+1;
y=cumprod(results)-1;
beta=y(end)/std(y);
op=[winRatio,beta,j-1];
% figure;
% plot(1:j-1,y);
end



% function op=Test_Gap(stock)
% w=windmatlab;
% rawData=w.wsd(stock,'open,high,low,close,volume','2000-01-01',today-1,'Fill=Previous','PriceAdj=F');
% open=rawData(:,1);
% indTem=sum(isnan(open))+1;
% open=open(indTem:end);
% high=rawData(indTem:end,2);
% low=rawData(indTem:end,3);
% close=rawData(indTem:end,4);
% vol=rawData(indTem:end,5);
% L=length(open);
% x=zeros(1,L);
% y=zeros(1,L);
% results=zeros(1,L);
% j=1;
% for i=3:L-3
%     if (low(i-1)-open(i))/close(i-1)>=0.01 && vol(i-1)>1  && vol(i-1)<vol(i-2)*0.8 %&& vol(i-1) > vol(i-2)*0.5
%         x(j)=i;
%         y(j)=high(i);
%         results(j)=(open(i+1)-open(i))/open(i);
%         j=j+1;
%     end
% end
% % candle(high,low,close,open);
% % hold on;
% % plot(x(1:j-1),y(1:j-1),'*','Color','r')
% plus=sum(results>0);
% winRatio=plus/(j-1);
% results=results(1:j-1)+1;
% y=cumprod(results)-1;
% beta=y(end)/std(y);
% op=[winRatio,beta,j-1];
% % figure;
% % plot(1:j-1,y);
% end