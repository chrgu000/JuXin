function sizeValue=SizeX
w = windmatlab;
% [w_wset_data,w_wset_codes,w_wset_fields,w_wset_times,w_wset_errorid,w_wset_reqid]=w.wset('SectorConstituent','date=20160801;sectorId=a001010100000000');
w_wset_data=w.wset('SectorConstituent','a001010100000000');
x_stock = w_wset_data(:,2);
shares= w.wss(x_stock,'float_a_shares');
price=w.wsd(x_stock,'close');
Value=log(shares.*price );
sizeValue={x_stock,Value};
save Size sizeValue
end
