function op = ATR_X(ip1,ip2)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
global high low close;
if ip1>ip2
    tem=ip2;
    ip2=ip1;
    ip1=tem;
end
HL=high(ip1:ip2)-low(ip1:ip2);
HC=abs(high(ip1:ip2)-close(ip1:ip2));
LC=abs(low(ip1:ip2)-close(ip1:ip2));
op=mean(max([HL;HC;LC]));
end

