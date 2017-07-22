function ArbitrageOFCommodity(option) % sugar:SR709C/P6100.czc,SR709.czc;bean pulp:M1709-C/P-2500.dce,M1709.dce;
option1=option;
option2=option;
future=option;
price=str2double(option(end-7:end-4));
if option(6)=='-'
    future(end-10:end-4)=[];
    bos=option(7);
    tem=7;%location for 'Buy' or 'Sell'
else
    future(end-8:end-4)=[];
    bos=option(6);
    tem=6;
end

if bos=='C'
    option2(tem)='P';
else
    option2(tem)='C';
end
w=windmatlab;
[Opt1,~,~,Date]=w.wsd(option1,'high,low,close,open','ED-200TD',today-1);
Opt2=w.wsd(option2,'high,low,close,open','ED-200TD',today-1);
Fut=w.wsd(future,'high,low,close,open','ED-200TD',today-1);
realNO=sum(~isnan(Opt1(:,1)))-1;
realNF=sum(~isnan(Fut(:,1)))-1;
realN=min(realNO,realNF);
Opt1=Opt1(end-realN:end,:);
Opt2=Opt2(end-realN:end,:);
Fut=Fut(end-realN:end,:);
Date=Date(end-realN:end,:);
L=length(Date);

if bos=='C'
    diff=Fut(:,3)-price-Opt1(:,3)+Opt2(:,3);
else
    diff=price-Opt1(:,3)+Opt2(:,3)-Fut(:,3);
end

% subplot(211);
plot(diff);
set(gca,'xtick',1:L);
Date=cellstr(datestr(Date,'yyyy-mm-dd'));
set(gca,'xticklabel',Date(1:L));
title(['商品期货-期权套利',' (',option(1:end-4),')'],'FontSize',16,'FontWeight','bold','Color','r');
xlabel('时间','FontSize',12,'FontWeight','bold','Color','r');
ylabel('套利空间（元）','FontSize',12,'FontWeight','bold','Color','r');
grid on;
% subplot(212);
% diffS=abs(diff)-4090;
% plot(diffS);
% set(gca,'xtick',1:241:L);
% set(gca,'xticklabel',Date(1:241:L));
% title('套利盈亏情况');
% grid on;