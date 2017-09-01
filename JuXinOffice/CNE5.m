% function CNE5
% load PrepareCNE5;
% w=windmatlab;
% stocks=prepareCNE5Value{1};
% Volume=w.wsd(stocks,'volume','ED-252TD',today-1,'priceAdj=F','cycle=D');
% ind=sum(Volume>0)>200;
% stocks=stocks(ind);
% Price=w.wsd(stocks,'close','ED-252TD',today-1,'priceAdj=F','cycle=D');
% y=Price(2:end,:)./repmat(Price(1,:),size(Price,1)-1,1)-1;
% X=prepareCNE5Value{2}(ind,:); % 6 columns in all; 1--Beta,2--momentum,3--size,4--residualVolatility,5--booktoprice,6--liquidity;
% % Xstd=mapstd(X);
% 
% 
% [f,~,u]=regress(y,X);
% end
w=windmatlab;
w_wset_data=w.wset('SectorConstituent');
stocks=w_wset_data(:,2);
for i=450:-20:300
    Volume=w.wsd(stocks(1:i),'volume','ED-510TD',today-1,'Fill=Previous','PriceAdj=F');
    if size(Volume,1)>2
        i
        break;
    end
end