function momentumValue=MomentumX
w=windmatlab;
% w_wset_data=w.wset('SectorConstituent','date=20170118;sectorId=a001010100000000');
w_wset_data=w.wset('SectorConstituent','a001010100000000');
x_stock=w_wset_data(:,2);
price=w.wsd(x_stock,'close','ED-504TD',today-21,'Fill=Previous','PriceAdj=F');
if size(price,1)<2
    price=zeros(505,length(x_stock));%22行3065列对应着3065个股票的近22个交易日的收盘价;
    for i=1:2000:length(x_stock)
        if i+1999<length(x_stock)
            stocksTem=x_stock(i:i+1999);
            priceTem=w.wsd(stocksTem,'close','ED-504TD',today-21,'Fill=Previous','PriceAdj=F');
            price(:,i:i+1999)=priceTem;
        else
            stocksTem=x_stock(i:end);
            priceTem=w.wsd(stocksTem,'close','ED-504TD',today-21,'Fill=Previous','PriceAdj=F');
            price(:,i:end)=priceTem;
        end
    end
end
ind=sum(isnan(price))==0;
x_stock=x_stock(ind');
price=price(:,ind');
rt1=price(2:end,:)./repmat(price(1,:),size(price,1)-1,1)-1;%2016年活期存款日利率千分之1.19；
rft1=1.00001386*ones(size(rt1));
rft1=cumprod(rft1)-1;
f=@(x) 0.5.^(x/126);
wt=f(1:504)';
wt=repmat(flipud(wt),1,size(rt1,2));
RSTR=sum(wt.*log((1+rt1)./(1+rft1)));
momentumValue={x_stock,RSTR'};
save Momentum momentumValue;
end