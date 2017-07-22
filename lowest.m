function op1 = lowest(ip1,ip2) % return the bar number of the lowest bar from bar ip1 to ip2;
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
global low;
x=ip1;
re=low(ip1);
if ip1>ip2
    d=-1;
else
    d=1;
end
for i=ip1:d:ip2,
    if low(i)<re
        re=low(i);
        x=i;
    end
end
op1=x;
end

