function re=AboveHalf(len)
global high low close;
L=length(high);
if L-len<=0
    re=0;
    return
end
L0=lowest(L-len,L);
H0=highest(L-len,L);
if (high(H0)-low(L0))/2+low(L0)<close(L)*1.05
    re=1;
else
    re=0;
end