function residualVolatilityValue=ResidualVolatilityX
w=windmatlab;
% w_wset_data=w.wset('SectorConstituent','date=20170118;Id=a001010100000000');
w_wset_data=w.wset('SectorConstituent','a001010100000000');
h=waitbar(0,'请稍等，正在准备计算ResidualVolatilityX');
x_stock=w_wset_data(:,2);
% x_stock=x_stock(1:5);
price=w.wsd(x_stock,'close','ED-252TD',today-1,'Fill=Previous','PriceAdj=F');
if size(price,1)<2
    price=zeros(253,length(x_stock));%22行3065列对应着3065个股票的近22个交易日的收盘价;
    for i=1:2000:length(x_stock)
        if i+1999<length(x_stock)
            stocksTem=x_stock(i:i+1999);
            priceTem=w.wsd(stocksTem,'close','ED-252TD',today-1,'Fill=Previous','PriceAdj=F');
            price(:,i:i+1999)=priceTem;
        else
            stocksTem=x_stock(i:end);
            priceTem=w.wsd(stocksTem,'close','ED-252TD',today-1,'Fill=Previous','PriceAdj=F');
            price(:,i:end)=priceTem;
        end
    end
end
ind_price=sum(isnan(price))==0;
price=price(:,ind_price);
x_stock=x_stock(ind_price);
% rt=price(2:end,:)./repmat(price(1,:),size((price),1)-1,1)-1;
% rft=1.00001386*ones(252,1);
% rft=cumprod(rft)-1;
rt=price(2:end,:)./price(1:end-1)-1;
rft=0.00001386*ones(size(rt));


f=@(x)0.5.^(x/42);
wt=flipud(f(1:252)');
y=bsxfun(@minus,rt,rft);
DASTD=std(y,wt);%是一行值，每个值对应一个股票的DASTD值；

ind_tem=21:21:252;
rt21=rt(ind_tem,:);
rft21=rft(ind_tem,:);
Z=log( bsxfun(@rdivide,(1+rt21),(1+rft21)) );
Z=cumsum(Z);
CMRA=max(Z)-min(Z); %是一行值，每个值对应一个股票的CMRA值；
ss300price=w.wsd('000300.sh','close','ED-252TD',today-1,'Fill=Previous','PriceAdj=F');
Rt=ss300price(2:end)./repmat(ss300price(1,:),size(ss300price,1)-1,1)-1;
f=@(x)0.5.^(x/63);
wt=flipud(f(1:252)');
tem=roundn(300/(300+length(x_stock)),-4);
waitbar(tem,h,['ResidualVolatilityX: 已完成...',num2str(100*tem),'%']);
Ltem=size(y,2);
HSIGMA=arrayfun(@(rt,y,wt,num,h) oddX(rt,y,wt,num,h),num2cell(repmat(Rt,1,Ltem),1),...
    num2cell(y,1),num2cell(repmat(wt,1,Ltem),1),num2cell([1:Ltem;repmat(Ltem,1,Ltem)],1),repmat(h,1,Ltem));%是一行值，每个值对应一个股票的HSIGMA值；
waitbar(1,h,'已完成...100%');
pause(1);
delete(h);
value=0.74*DASTD+0.16*CMRA+0.1*HSIGMA;
residualVolatilityValue={x_stock,value'};
save ResidualVolatility residualVolatilityValue;
end

function re=oddX(Rt,y,wt,num,h)
myfunc=@(beta,x) beta(1)*x+beta(2);
[~,r]=nlinfit(Rt{:},y{:},myfunc,[1,1],'Weights',wt{:});
re=std(r);
tem=roundn((num{:}(1)+300)/(300+num{:}(2)),-4);
waitbar(tem,h,['ResidualVolatilityX: 已完成...',num2str(100*tem),'%']);
end

% function residualVolatilityValue=ResidualVolatilityX %%如果使用请添加,'Fill=Previous','PriceAdj=F'，以获取复权价格；处理cumsum函数；
% 
% w=windmatlab;
% w_wset_data=w.wset('SectorConstituent','date=20170118;Id=a001010100000000');
% h=waitbar(0,'请稍等，正在准备计算ResidualVolatilityX');
% x_stock=w_wset_data(:,2);
% % x_stock=x_stock(1:5);
% price=w.wsd(x_stock,'close','ED-252TD',today-1);
% ind_price=sum(isnan(price))==0;
% price=price(:,ind_price);
% x_stock=x_stock(ind_price);
% rt=price(2:end,:)./price(1:end-1,:)-1;
% rt=cumsum(rt);
% rft=1.00013652*ones(252,1);
% rft=cumprod(rft)-1;
% f=@(x)0.5.^(x/42);
% wt=flipud(f(1:252)');
% y=bsxfun(@minus,rt,rft);
% DASTD=std(y,wt);
% 
% % wt=wt/sum(wt);
% % ymean=mean(y);
% % DASTD=bsxfun(@minus,y,ymean).^2;
% % DASTD=sum(bsxfun(@times,DASTD,wt)).^0.5; %是一行值，每个值对应一个股票的DASTD值；
% 
% ind_tem=21:21:252;
% rt21=rt(ind_tem,:);
% rft21=rft(ind_tem,:);
% Z=log( bsxfun(@rdivide,(1+rt21),(1+rft21)) );
% Z=cumsum(Z);
% CMRA=max(Z)-min(Z); %是一行值，每个值对应一个股票的CMRA值；
% 
% 
% [ss300price,~,~,ss300time,~,~]=w.wsd('000300.sh','close','ED-500TD',today-1);
% Rt=zeros(501,1);
% Rt(2:end)=ss300price(2:end)./ss300price(1:end-1)-1;
% Rt=cumsum(Rt);
% myfunc=@(beta,x) beta(1)*x+beta(2);
% f=@(x)0.5.^(x/63);
% wt=flipud(f(1:252)');
% HSIGMA=zeros(1,length(x_stock)); %是一行值，每个值对应一个股票的HSIGMA值；
% tem=roundn(300/(300+length(x_stock)),-4);
% waitbar(tem,h,['ResidualVolatilityX: 已完成...',num2str(100*tem),'%']);
% for i=1:length(x_stock)
%     [~,~,~,time]=w.wsd(x_stock(i),'close','ED-252TD',today-1);
%     [~,tem,~]=intersect(ss300time,time(2:end));
%     Rttem=Rt(tem);
%     [~,r]=nlinfit(Rttem,y(:,i),myfunc,[1,1],'Weights',wt);
%     HSIGMA(i)=std(r);
%     tem=roundn((i+300)/(300+length(x_stock)),-4);
%     waitbar(tem,h,['ResidualVolatilityX: 已完成...',num2str(100*tem),'%']);
% end
% waitbar(1,h,'已完成');
% pause(1);
% delete(h);
% 
% value=0.74*DASTD+0.16*CMRA+0.1*HSIGMA;
% residualVolatilityValue={x_stock,value'};
% save ResidualVolatility residualVolatilityValue;
% 
% end
