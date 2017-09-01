function HoldOne(stock)
% w=windmatlab;
% [data,~,~,date]=w.wsd(stock,'open,high,low,close,volume','20150416',today-1);
switch stock
    case 'ic.cfe'
        load ic;
        longP=[3,5];
        shortP=[1,4];
    case 'if.cfe'
        load if
        longP=[3];
        shortP=[2,4];
    case 'ih.cfe'
        load ih
        longP=[1,3]; %delete 5 for modifying maxDrawback;
        shortP=[3,4];
    case 'ru.shf'
        load ru
        longP=[]; %delete 5 for modifying maxDrawback;
        shortP=[4];
    case 'al.shf'
        load al
        longP=[]; %delete 5 for modifying maxDrawback;
        shortP=[4];
end
Open=data(:,1);
High=data(:,2);
Low=data(:,3);
Close=data(:,4);
L=length(High);
results=zeros(1,L);
plus=0;
minus=0;
    
for i=1:L-3
    pastDiff=max(High(i)-Close(i),Close(i)-Low(i))*0.08;
    base=Close(i);
    wd=weekday(Date(i))-1;
    if High(i+1)>base+pastDiff && Low(i+1)>base-pastDiff && sum(longP==wd)
        results(i)=Close(i+2)/(Close(i+1))-1-0.001;
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
% figure;
clf;
[AX,H1,H2]=plotyy(1:L,Close,1:L,y*100);
xlabel('时间','fontsize',12);
step=floor(L/10);
set(AX(1),'xTick',1:step:L);
dateStr=cellstr(datestr(Date,'yyyy-mm-dd'));
set(AX(1),'XTicklabel',dateStr(1:step:L));
y1Min=min(Close);
y1Max=round(max(Close)*1.1,0);
y1Step=(y1Max-y1Min)/10;
set(AX(1),'ylim',[y1Min,y1Max]);
set(AX(1),'yTick',round(y1Min:y1Step:y1Max,0));
set(get(AX(1),'ylabel'),'string','股指期货指数','fontsize',12);
grid on;

y2Min=min(y)*100;
y2Max=round(max(y)*110,1);
y2Step=(y2Max-y2Min)/10;
set(AX(2),'ylim',[y2Min,y2Max]);
set(AX(2),'yTick',round(y2Min:y2Step:y2Max,1));
set(get(AX(2),'ylabel'),'string','策略涨跌指数（%）','fontsize',12);
set(AX(2), 'YColor', 'r')
set(H2,'color','k');
lege=legend(stock,'策略曲线','location','NorthWest','Orientation','horizontal');
set(lege,'Fontsize',12);
axes(AX(2));
hold on;
plot(maxInd,y(maxInd)*100,'r*');
hold off;
end

% % Draw a two-different X-axes figure;
% tp=(0:100)/100*5;yp=8+4*(1-exp(-0.8*tp).*cos(3*tp)); % 压力数据
% tt=(0:500)/500*40;yt=120+40*(1-exp(-0.05*tt).*cos(tt)); % 温度数据
% % 产生双坐标系图形
% clf reset,h_ap=axes('Position',[0.13,0.13,0.7,0.75]); %<4>
% set(h_ap,'Xcolor','b','Ycolor','b','Xlim',[0,5],'Ylim',[0,15]);
% nx=10;ny=6; %<6>
% pxtick=0:((5-0)/nx):5;pytick=0:((15-0)/ny):15; %<7>
% set(h_ap,'Xtick',pxtick,'Ytick',pytick,'Xgrid','on','Ygrid','on')
% h_linet=line(tp,yp,'Color','b'); %<9>
% set(get(h_ap,'Xlabel'),'String',' 时间 /rightarrow （分） ')
% set(get(h_ap,'Ylabel'),'String',' 压力 /rightarrow(/times10 ^{5} Pa )')
% h_at=axes('Position',get(h_ap,'Position')); %<12>
% set(h_at,'Color','none','Xcolor','r','Ycolor','r'); %<13>
% set(h_at,'Xaxislocation','top') %<14>
% set(h_at,'Yaxislocation','right','Ydir','rev') %<15>
% set(get(h_at,'Xlabel'),'String','/fontsize{15}/fontname{ 隶书 } 时间 /rightarrow （分） ')
% set(get(h_at,'Ylabel'),'String',' ( {/circ}C )/fontsize{15} /leftarrow /fontname{ 隶书 } 零下温度 ')
% set(h_at,'Ylim',[0,210]) %<18>
% line(tt,yt,'Color','r','Parent',h_at) %<19>
% xpm=get(h_at,'Xlim'); %<20>
% txtick=xpm(1):((xpm(2)-xpm(1))/nx):xpm(2); %<21>
% tytick=0:((210-0)/ny):210; %<22>
% set(h_at,'Xtick',txtick,'Ytick',tytick) %<23>