function [up,aver,down]=Boll(close)
L=length(close);
if L<13
    return;
end
N=20;
dotN(L-N)=0;
averL(L-N)=0;
upL(L-N)=0;
downL(L-N)=0;
for i=N:L
    dotN(i-N+1)=i;
    averL(i-N+1)=mean(close(i-N+1:i));
    diff=std(close(i-N+1:i));
    upL(i-N+1)=averL(i-N+1)+2*diff;
    downL(i-N+1)=averL(i-N+1)-2*diff;
end
if nargout==0
    hold on;
    plot(dotN',[upL' averL' downL'],'--','LineWidth',0.1);
    hold off;
else
    up=[zeros(1,N) upL];
    aver=[zeros(1,N) averL];
    down=[zeros(1,N) downL];
end
end