function [op1,op2]=Model_Test
global open high low;
op1=0;
op2=0;
X(2,1)=0;
Y(2,1)=0;
L=length(high);
if L>30 && 0
    for i=5:15
        startP=low(L-i);
        endP=open(L);
        maxP=max(high(L-i+1:L-1));
%         minP=min(low(L-i+1:L-1));
        if startP>maxP+0.08 && endP>maxP+0.08&&...
                abs(startP-endP)<startP*0.1 %&& low(L-1)>min(low(L-i+1:L-2))
            op1=1;
            X(1,1)=L-i;  Y(1,1)=low(L-i);
            X(2,1)=L;     Y(2,1)=low(L);
            op2=[X,Y];
            break;
        end
    end
end
end