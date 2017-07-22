function [op1,op3,op31,ord,ratio]=Model_UpDown
global high low close vol;
op1=0;
op3=0;
op31=0;
ord(10,3)=0;
ratio(10,3)=0;
cycleD=24;
X(3,5)=0;
Y(3,5)=0;
L=length(high);

% xxx=0;

if low(lowest(L-2,L))>=low(L) && L>4*cycleD
    kline=0;
    for j=7:50     
        if L-j-4 <=0
            break;
        end
        pointH=highest(L-j,L);    
        ratio_tem=(high(pointH)-low(L))/(high(pointH)-low(L-j));
        if low(lowest(L-floor(j/2),L-j-4))>=low(L-j) && low(L)<=low(lowest(L-ceil(j/2),L)) ...  %L-j,L-2*j-4
                   && abs(L-pointH-j/2)<2  ...  % && low(L)>=low(L-j) && L-j<pointH && L>pointH
                   && close(L)>=(low(L-j)+high(pointH))/2 && ratio_tem<0.37 ...
                   %&& ATR_X(L-j,L)<ATR_X(L-2*j,L-j)/2
                   
                   % && low(lowest(L-2*cycleD,L-4*cycleD))<=low(lowest(L-2*cycleD,L)) && high(highest(L-2*cycleD,L-4*cycleD))<=high(highest(L-2*cycleD,L)) 
            barN=j;
            ATR_X(L-j,L);
            ATR_X(L-2*j,L-j);
            kline=kline+1;
            X(1,kline)=L-j;        Y(1,kline)=low(L-j);
            X(2,kline)=pointH;   Y(2,kline)=high(pointH);
            X(3,kline)=L;     Y(3,kline)=low(L);
            
            ord1=mean(vol(L-j:pointH));
            ord2=mean(vol(pointH:L));
            ordM=high(pointH)*1.05;
            if ord==0
                ord(1:2,:)=[(L-j+pointH)/2-2,ordM,10;(L+pointH)/2,ordM,roundn(ord2*10/ord1,-1)];
                ratio(1,:)=[L+1,low(L),roundn(ratio_tem,-3)];
            else
                rowN=sum(sum(ord')~=0);
                ord(rowN+1:rowN+2,:)=[(L-j+pointH)/2-2,ordM,10;(L+pointH)/2,ordM,roundn(ord2*10/ord1,-1)];
                ratio(rowN+1,:)=[L+1,low(L),roundn((high(pointH)-low(L))/(high(pointH)-low(L-j)),-3)];
            end
%             
%             if (ord1-ord2)/ord1>=0.45
%                 xxx=10;
%             end
%         
        end
    end
    if kline>=1
        op1=1; %barN;
        op3=X(:,1:kline);
        op31=Y(:,1:kline);
    end
end
end