function topStocks=hsSGetStocks % get top 50 stocks according months' ups and downs;
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
[closeStat,~,~,dateStat]=w.wsd(stocks,'close','ED-200M','2016-12-31','Period=M','Fill=Previous'); 
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
    date=mat2cell(datestr(date,'yyyy-mm-dd'),ones(length(date),1),10);
    xn=str2num(datestr(date,'mm'));
    diff=close(2:end)./close(1:end-1)-1;
    A=accumarray(xn(2:end),diff);
    a=accumarray(xn(2:end),1);
    updownStocks(:,i)=A./a;
end
[~,ind]=sort(updownStocks,2);
topStocks=cell(12,50);
for i=1:12
    topStocks(i,:)=stocks(ind(i,1:50));
end
% xlswrite('E:\juxin\WFT\topNStocks.xlsx',topStocks);
xlswrite('D:\Trading\WFT\topNStocks.xlsx',topStocks);

% hs300=w.wsd('000300.SH','close','2013-01-01',today-1,'Fill=Previous','PriceAdj=F');
% hs300Di=hs300(2:end)./hs300(1:end-1);
% hs300Re=cumprod(hs300Di)-1;
% [closeTest,~,~,dateTem]=w.wsd(stocks,'close','2013-01-01',today-1,'Fill=Previous','PriceAdj=F');
% tem=datevec(dateTem);
% month=tem(:,2);
% L=length(month);
% results=zeros(L-1,1);
% monthExept=[2,3,4,5,7,9,10,11,12];
% for i=1:L
%     if i==1 || month(i)~=month(i-1)
%         indSort=ind(month(i),:);
%         indStock=indSort(end-49:end);
%     end
%     if i>1
%         if ~isempty(find(monthExept==month(i),1))
%             close=closeTest(i-1:i,indStock);
%             diff=close(2,:)./close(1,:)-1;
%             results(i-1)=0.66*sum(diff)/50-0.33*(hs300Di(i-1)-1);
%         else
%             results(i-1)=-0.2*(hs300Di(i-1)-1);
%         end
%     end
% end
% results=cumprod(results+1)-1;
% beta=results(end)/std(results);
% plot(results);
% hold on;
% plot(hs300Re);
% legend('策略资金曲线','沪深300走势曲线');
% hold off;
end



