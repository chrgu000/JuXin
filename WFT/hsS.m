function sharpe=hs300S % long stong and short hs300; two models: all month and whole hedge trading; only long trade for selected months and only short for hs300;
w=windmatlab;
dataTem=w.wset('sectorconstituent');
stocks=dataTem(:,2);
names=dataTem(:,3);
Lnames=length(names);
indTem=ones(Lnames,1);
for i=1:Lnames
    if names{i}(1)=='*' || strcmp(names{1}(1:2),'ST')
        indTem(i)=0;
    end
end
indTem=logical(indTem);
stocks=stocks(indTem);
% stocks=stocks(1:20);

[closeStat,~,~,dateStat]=w.wsd(stocks,'close','ED-200M','2012-12-31','Period=M','Fill=Previous'); 
%id=w.wsd('000300.SH,000016.SH,000100.SH','close','ED-9D','2017-03-13','Fill=Previous','PriceAdj=F'); for hs300,sh50,sh500
indTem=sum(isnan(closeStat))<1;
closeStat=closeStat(:,indTem);
stocks=stocks(indTem);
L=length(stocks);
updownStocks=zeros(12,L);
for i=1:L
    close=closeStat(:,i);
    date=dateStat;
    indTem=isnan(close)<1&close>1.0;
    close=close(indTem);
    date=date(indTem);
    dataTem=datevec(date);
    xn=dataTem(:,2);
    diff=close(2:end)./close(1:end-1)-1;
    A=accumarray(xn(2:end),diff);
    a=accumarray(xn(2:end),1);
    updownStocks(:,i)=A./a;
end
[~,ind]=sort(updownStocks,2);

hs300=w.wsd('000300.SH','close','2013-01-01',today-1,'Fill=Previous','PriceAdj=F');
hs300Di=hs300(2:end)./hs300(1:end-1);
% hs300Re=cumprod(hs300Di)-1;
hs300Re=cumsum(hs300Di-1);
[closeTest,~,~,dateTem]=w.wsd(stocks,'close','2013-01-01',today-1,'Fill=Previous','PriceAdj=F');
tem=datevec(dateTem);
month=tem(:,2);
L=length(month);
results=zeros(L-1,1);
% monthExept=[1,6,8,2,3,4,5,7,9,10,11,12];
monthExept=[2,3,4,5,7,9,10,11,12];
numberSelected=50; % select how many stocks to trade for each month;
for i=1:L
    if i==1 || month(i)~=month(i-1)
        indSort=ind(month(i),:);
        indStock=indSort(end-numberSelected+1:end);
    end
    if i>1
        if ~isempty(find(monthExept==month(i),1))
            close=closeTest(i-1:i,indStock);
            diff=close(2,:)./close(1,:)-1;
%             results(i-1)=0.5*sum(diff)/numberSelected-0.5*(hs300Di(i-1)-1);
            results(i-1)=0.5*sum(diff)/numberSelected-0*(hs300Di(i-1)-1);
        else
            close=closeTest(i-1:i,indStock);
            diff=close(2,:)./close(1,:)-1;
            results(i-1)=0.5*sum(diff)/numberSelected-0.5*(hs300Di(i-1)-1);
        end
    end
end
resultsRaw=results;
sharpe=mean(resultsRaw)/std(resultsRaw);
% results=cumprod(results+1)-1;
results=cumsum(results);
figure;
plot(results);
Ltem=length(hs300);
stepTem=floor(Ltem/10);
indTem=1:stepTem:Ltem;
indTem(end)=Ltem;
set(gca,'xtick',indTem);
dateStr=datestr(dateTem,'yyyy-mm-dd');
dateStr=cellstr(dateStr);
% dateStr=mat2cell(dateStr,ones(size(dateStr,1),1),size(dateStr,2));
dateTarget=dateStr(indTem);
set(gca,'xticklabel',dateTarget);
xtb = get(gca,'XTickLabel');
xt=get(gca,'XTick')+8;
yt=get(gca,'YTick');
% yt=(yt(1)-0.1)*ones(1,length(xt));
yt=(yt(1)-0.02)*ones(1,length(xt));
text(xt,yt,xtb,'HorizontalAlignment','right','rotation',45,'fontsize',10); 
set(gca,'xticklabel','');
hold on;
grid on;
plot(hs300Re);
tem=legend('策略资金曲线','沪深300走势曲线','Location','NorthWest');
set(tem,'Fontsize',12);
hold off;
end



