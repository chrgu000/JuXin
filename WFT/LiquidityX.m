function liquidityValue=LiquidityX
w=windmatlab;
% w_wset_data=w.wset('SectorConstituent','date=20170118;sectorId=a001010100000000');
w_wset_data=w.wset('SectorConstituent','a001010100000000');
x_stock=w_wset_data(:,2);
% x_stock=x_stock(1:2);

temVolume=w.wsd(x_stock,'volume','ED-255TD',today-1,'Fill=Previous','PriceAdj=F');
temNan=sum(isnan(temVolume));
temZero=sum(all(temVolume));
temIndex=temNan<1&temZero;
x_stock=x_stock(temIndex);
stom=STOM(w,x_stock,today-1); %一行多列，每一列代表一个股票的stom值；
stoq=zeros(size(stom));
for i=1:21:43
    stoq=stoq+exp(STOM(w,x_stock,today-i));
end
stoq=log(stoq/3);
stoa=zeros(size(stom));
for i=1:21:253
    stoa=stoa+exp(STOM(w,x_stock,today-i));
end
stoa=log(stoa/12);
Value=0.35*stom+0.35*stoq+0.3*stoa;
liquidityValue={x_stock,Value'};
save Liquidity liquidityValue;
end

function re=STOM(w,stocks,day)
Volume=w.wsd(stocks,'volume','ED-20TD',day);
shares= w.wss(stocks,'float_a_shares')';
Shares=repmat(shares,21,1);
re=log(sum(Volume./Shares));
end