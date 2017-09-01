function industry=GetIndustry
w=windmatlab;
w_wset_data=w.wset('SectorConstituent','a001010100000000');
x_stock=w_wset_data(:,2);
data=w.wss(x_stock,'industry_sw','industryType=1'); % 'industry_gics','industryType=3'
L=length(data);
indexCell=arrayfun(@(k) isnan(data{k}),1:L,'un',0);
indexTem=arrayfun(@(k) sum(indexCell{k}),1:L,'un',0);
indexTem=cell2mat(indexTem)<1;
x_stock=x_stock(indexTem);
data=data(indexTem);
[dataUnique,~,indexMap]=unique(data);
Ldata=length(data);
Lunique=length(dataUnique);
Indicators=zeros(Ldata,Lunique);
for i=1:Ldata
    Indicators(i,indexMap(i))=1;
end
industry={x_stock,dataUnique,Indicators}; % 'x_stock' saves all stocks; 'dataUnique' saves each industry; 'Indicators' is an matrix: number of stocks X kinds of Industries;
save GetIndustry industry;
end
