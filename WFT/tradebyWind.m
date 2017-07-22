function tradebyWind
w=windmatlab;
%%log on and close orders for M5;
pause(3);
[Data,Fields,ErrorCode]=w.tlogon('0000', '0', 'W115294100301', '*********', 'SHSZ'); % logon account;
% [Data,Fields,ErrorCode]=w.tlogon('21230401', '0', '17000003516','******', 'SHSZ'); %five mines
logId=Data{1};
%% close all orders;
data= w.tquery('Position');% query stocks which were hold;
stocksHold=data(:,1);% stocks which are holding;
sharesAvailable=data(:,4);% how many shares for hold stocks;
Ltem=length(stocksHold);
for i=1:Ltem
     [~,~,ErrorCode]=w.torder(stocksHold(i), 'Sell', '0', sharesAvailable(i), ['OrderType=B5TC;','LogonID=',num2str(logId)]);
end

%% open order for M5 and log out account;
Data=scanX(5);
Ltem=length(Data);
stocksBuy=[];
sharesBuy=[];
for i=1:Ltem
    stocksBuy=[stocksBuy;Data{i}(1:9)];
    tem=Data{i}(end-3:end);
    if tem(1)==':'
        tem=tem(2:end);
    end
    tem={tem};
    sharesBuy=[sharesBuy;tem];        
end
stocksBuy=cellstr(stocksBuy);
sharesBuy=cellstr(sharesBuy);
% basePrice=w.wsd(stocksBuy,'close');
Ltem=length(stocksBuy);
for i=1:Ltem
    [Data,Fields,ErrorCode]=w.torder(stocksBuy(i),'Buy','0',sharesBuy(i),['OrderType=B5TC;','LogonID=',num2str(logId)])
end
[Data,Fields,ErrorCode]=w.tlogout(num2str(logId));% logoff account;

%% trade for stocks future;



end
