function [op1,op2]=Model_12
global high low;
op1=0;
X(2,1)=0;
Y(2,1)=0;
L=length(high);
high_bar=highest(L-10,L-12);
low_bar=lowest(L-10,L-12);

if ( high_bar==highest(L-18,L) || (low_bar==lowest(L-18,L-6)&&low(low_bar)<=low(lowest(L-10,L))) ) && ...  % for the firt point;
        ( ( min(high(L-3:L-1))>=high(L) || min(low(L-3:L-1))>=low(L)) || ... % for the second point
        ( ( high(L) <=high(L-1)||low(L)<=low(L-1)) && (high(L) <=high(L-2)||low(L)<=low(L-2)) &&(high(L) <=high(L-3)||low(L)<=low(L-3)) )) && ... % for the second point
        low(L)<=mean(low(L-11:L))
    op1=1;
    X(1,1)=L-11;  Y(1,1)=high(L-11);
    X(2,1)=L;     Y(2,1)=low(L);
end
op2=[X,Y];
end