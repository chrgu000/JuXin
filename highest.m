function op1= highest(ip1,ip2) % return the number of the highest bar from bar ip1 to ip2; 
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
global high;
x=ip1;
re=high(ip1);
if ip1>ip2
    d=-1;
else
    d=1;
end
for i=ip1:d:ip2
    if high(i)>re
        re=high(i);
        x=i;
    end
end
op1=x;
end

