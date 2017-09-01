function booktopriceValue=BooktopriceX
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','a001010100000000');
x_stock=w_wset_data(:,2);
data=w.wss(x_stock,'close,bps_new','Fill=Previous','PriceAdj=F');
indexTem=sum(isnan(data),2)==0;
data=data(indexTem,:);
x_stock=x_stock(indexTem);
Value=data(:,2)./data(:,1);
booktopriceValue={x_stock,Value};
save Booktoprice booktopriceValue;
end