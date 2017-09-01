function betaValue=BetaX
w=windmatlab;
% w_wset_data=w.wset('SectorConstituent','date=20170117;Id=a001010100000000');
w_wset_data=w.wset('SectorConstituent','a001010100000000');
h=waitbar(0,'请稍等，正在准备计算BetaX');
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
% rt=price(2:end,:)./repmat(price(1,:),size(price,1)-1,1)-1;
% rft=1.00013652*ones(size(rt));
% rft=cumprod(rft)-1;

rt=price(2:end,:)./price(1:end-1)-1;
rft=0.00001386*ones(size(rt));

y=rt-rft;
ss300price=w.wsd('000300.sh','close','ED-252TD',today-1,'Fill=Previous','PriceAdj=F');
Rt=ss300price(2:end)./repmat(ss300price(1,:),size(ss300price,1)-1,1)-1;
f=@(x)0.5.^(x/63);
wt=flipud(f(1:252)');
tem=200/(200+length(x_stock));
waitbar(tem,h,['BetaX: 已完成...',num2str(roundn(100*tem,-2)),'%']);
Ltem=size(y,2);
value=arrayfun(@(rt,y,wt,num,h) oddX(rt,y,wt,num,h),num2cell(repmat(Rt,1,Ltem),1),...
    num2cell(y,1),num2cell(repmat(wt,1,Ltem),1),num2cell([1:Ltem;repmat(Ltem,1,Ltem)],1),repmat(h,1,Ltem),'UniformOutput',false);%是一行值，每个值对应一个股票的HSIGMA值；
waitbar(1,h,'已完成...100%');
pause(1);
delete(h);
betaValue={x_stock,cell2mat(value')}; % each line of value is : beta, alpha and e;
save Beta betaValue
end

function value=oddX(Rt,y,wt,num,h)
myfunc=@(beta,x) beta(1)*x+beta(2);
[beta,r]=nlinfit(Rt{:},y{:},myfunc,[1,1],'Weights',wt{:});
value=[beta,std(r)];
tem=roundn((num{:}(1)+200)/(200+num{:}(2)),-4);
waitbar(tem,h,['BetaX: 已完成...',num2str(100*tem),'%']);
end

% function betaValue=BetaX % %%如果启用，请添加,'Fill=Previous','PriceAdj=F'以获取复权价格；处理cumsum函数；
% w=windmatlab;
% w_wset_data=w.wset('SectorConstituent','date=20170117;Id=a001010100000000');
% h=waitbar(0,'请稍等，正在准备计算BetaX');
% x_stock=w_wset_data(:,2);
% % x_stock=x_stock(1:5);
% price=zeros(253,length(x_stock));%22行3065列对应着3065个股票的近22个交易日的收盘价;
% % time=zeros(253,length(x_stock));
% for i=1:2000:length(x_stock)
%     if i+1999<length(x_stock)
%         stocksTem=x_stock(i:i+1999);
%         priceTem=w.wsd(stocksTem,'close','ED-252TD',today-1);
%         price(:,i:i+1999)=priceTem;
%     else
%         stocksTem=x_stock(i:end);
%         priceTem=w.wsd(stocksTem,'close','ED-252TD',today-1);
%         price(:,i:end)=priceTem;
%     end
% end
% ind_price=sum(isnan(price))==0;
% price=price(:,ind_price);
% x_stock=x_stock(ind_price);
% rt=price(2:end,:)./price(1:end-1,:)-1;
% rt=cumsum(rt);
% rft=1.00013652*ones(size(rt));
% rft=cumprod(rft)-1;
% y=rt-rft;
% [ss300price,~,~,ss300time,~,~]=w.wsd('000300.sh','close','ED-500TD',today-1);
% Rt=zeros(501,1);
% Rt(2:end)=ss300price(2:end)./ss300price(1:end-1)-1;
% Rt=cumsum(Rt);
% myfunc=@(beta,x) beta(1)*x+beta(2);
% % myfunc=@(x)a*x+b;
% % wt=zeros(252,1);
% % for i=1:252
% %     wt(i)=0.5^(i/63);
% % end
% f=@(x)0.5.^(x/63);
% wt=flipud(f(1:252)');
% value=zeros(length(x_stock),3);
% tem=200/(200+length(x_stock));
% waitbar(tem,h,['BetaX: 已完成...',num2str(roundn(100*tem,-2)),'%']);
% for i=1:length(x_stock)
%     [~,~,~,time]=w.wsd(x_stock(i),'close','ED-252TD',today-1);
%     [~,tem,~]=intersect(ss300time,time(2:end));
%     Rttem=Rt(tem);
%     [beta,r]=nlinfit(Rttem,y(:,i),myfunc,[1,1],'Weights',wt);
%     value(i,:)=[beta,std(r)];
%     tem=(i+200)/(200+length(x_stock));
%     waitbar(tem,h,['BetaX: 已完成...',num2str(roundn(100*tem,-2)),'%']);
% end
% waitbar(1,h,'已完成...100%');
% pause(1);
% delete(h);
% 
% betaValue={x_stock,value}; % each line of value is : beta, alpha and e;
% % save Beta betaValue
% end

% function betaValue=BetaX
% load bank % bankrate and bankdate are created;
% load ss300
% w = windmatlab;
% % [w_wset_data,w_wset_codes,w_wset_fields,w_wset_times,w_wset_errorid,w_wset_reqid]=w.wset('SectorConstituent','date=20160801;sectorId=a001010100000000');
% [w_wset_data,~,~,~,~,~]=w.wset('SectorConstituent','date=20170117;sectorId=a001010100000000');
% x_stock = w_wset_data(:,2);
% % x_stock=x_stock(1:3);
% result=zeros(length(x_stock),1);
% ind_stock=ones(length(x_stock),1);
% for i=1:length(x_stock)
% %     [w_wsi_data,w_wsi_codes,w_wsi_fields,w_wsi_times,w_wsi_errorid,w_wsi_reqid]=w.wsi(x_stock{a},'close','2016-08-01 09:00:00','2016-11-06 09:00:00');
%     [price,~,~,time,~,~]=w.wsd(x_stock{i},'close','ED-252TD','20170117');
%     oddnum=sum(isnan(price))+1;
%     price=price(oddnum:end);
%     time=time(oddnum:end);
%     rt=(price(2:end)-price(1:end-1))./price(1:end-1);
%     time=time(2:end);
%     if length(rt)~=252
%         ind_stock(i)=0;
%         display(x_stock(i));
%         continue;
%     end
%     rft=zeros(length(rt),1);
%     for j=1:length(bankdate)
%         tem=time>=bankdate(j)&rft==0;
%         rft(tem)=bankrate(j);
%     end
%     [~,tem,~]=intersect(ss300time,time);
%     Rttemp=Rt(tem);
%     try
%         p=fittype('a*x+b','independent','x');
%         opt=fitoptions(p);
%         opt.StartPoint=[1,0];
%         f=fit(Rttemp,rt-rft,p,opt);
%         result(i)=f.a;
%     catch
%         ind_stock(i)=0;
%         disp([x_stock(i),', index is: ',num2str(i)]);
%     end
% end
% betaValue={x_stock(ind_stock>0),result(ind_stock>0)};
% save Beta betaValue
% end