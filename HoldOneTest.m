function HoldOneTest
%% prepare for data
% w=windmatlab;
% % [data,~,~,Date]=w.wsd('ic.cfe','open,high,low,close,volume','20100416',today-1,'PriceAdj=F');
% [data,~,~,Date]=w.wsd('al.shf','open,high,low,close,volume','20100416',today-1,'PriceAdj=F');
% ind=isnan(data(:,1));
% data=data(~ind,:);
% Date=Date(~ind);
% save al data Date;
%% code 
stock='al';
load(stock)
longP=[]; %delete 5 for modifying maxDrawback; close(i+2):3,,2; open(i+3):2
shortP=[4];   %close(i+2):4  ; open(i+3):3,4

Open=data(:,1);
High=data(:,2);
Low=data(:,3);
Close=data(:,4);
L=length(High);
results=zeros(1,L);
plus=0;
minus=0;
     
for i=1:L-3
    pastDiff=max(High(i)-Close(i),Close(i)-Low(i))*0.1;
    base=Close(i);
    wd=weekday(Date(i))-1;
    if High(i+1)>base+pastDiff && Low(i+1)>base-pastDiff && sum(longP==wd)
        results(i)=Close(i+2)/(Close(i+1))-1-0.001;
%         results(i)=(Close(i+1))/Close(i+2)-1-0.001;
    elseif Low(i+1)<base-pastDiff && High(i+1)<base+pastDiff && sum(shortP==wd)
         results(i)=(Close(i+1))/Close(i+2)-1-0.001;
    end
   
    if results(i)>0
        plus=plus+1;
    elseif results(i)<0
        minus=minus+1;
    end
end
resultsCopy=results(results~=0);
y=cumsum(results);
maxDown=0;
for i=2:length(y)
    maxTem=max(y(1:i))-y(i);
    if maxTem>maxDown
        maxDown=maxTem;
        maxInd=i;
    end
end

display(['winRatio:',num2str(plus/(plus+minus)),' gain:',num2str(y(end)),' sharpe:',num2str(mean(resultsCopy)/std(resultsCopy)),...
    ' maxDraw:',num2str(maxDown),' allOrders:',num2str(plus+minus)]);
[AX,H1,H2]=plotyy(1:L,Close,1:L,y*100);
xlabel('时间','fontsize',12);
set(AX(1),'xTick',1:50:L);

set(get(AX(1),'ylabel'),'string','股指期货指数','fontsize',12);
set(get(AX(2),'ylabel'),'string','策略涨跌指数（%）','fontsize',12);
set(AX(2), 'YColor', 'r')
set(H2,'color','k');
lege=legend(stock,'策略曲线','location','NorthWest','Orientation','horizontal');
set(lege,'Fontsize',12);
grid on;
axes(AX(2));
hold on;
plot(maxInd,y(maxInd)*100,'r*');
set(AX(2),'xTick',1:length(y));
hold off;
end
