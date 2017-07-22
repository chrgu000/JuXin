function [op1,op3,op31,ord]=Model_UpDown_T(L)
global high low close vol;
op1=0;
op3=0;
op31=0;
ord(10,3)=0;
cycleD=12;
X(3,5)=0;
Y(3,5)=0;

% xxx=0;

I=L;
if low(lowest(I-2,I))>=low(I) && I>4*cycleD
    kline=0;
    for j=4:80     
        if I-j-4 <=0
            break;
        end
        pointH=highest(I-j,I);   
        diffB=2*I-2*pointH-j;
        if   low(lowest(I-j-4,pointH))>=low(I-j) && low(I)<=low(lowest(pointH,I)) ...  
                   && (diffB==0 || diffB==-1 || (diffB==-2 && close(pointH)<close(pointH-1)))... 
%                    && low(lowest(I-2*cycleD,I-4*cycleD))<=low(lowest(I-2*cycleD,I)) && high(highest(I-2*cycleD,I-4*cycleD))<=high(highest(I-2*cycleD,I)) 
            barN=j;                    
            kline=kline+1;
            X(1,kline)=I-j;        Y(1,kline)=low(I-j);
            X(2,kline)=pointH;   Y(2,kline)=high(pointH);
            X(3,kline)=I;     Y(3,kline)=low(I);
            
            ord1=mean(vol(I-j:pointH));
            ord2=mean(vol(pointH:I));
            ordM=high(pointH)*1.05;
            if ord==0
                ord(1:2,:)=[(I-j+pointH)/2-2,ordM,10;(I+pointH)/2,ordM,roundn(ord2*10/ord1,-2)];
            else
                rowN=sum(sum(ord')~=0);
                ord(rowN+1:rowN+2,:)=[(I-j+pointH)/2-2,ordM,10;(I+pointH)/2,ordM,roundn(ord2*10/ord1,-2)];
            end
%             
%             if (ord1-ord2)/ord1>=0.45
%                 xxx=10;
%             end
%         
        end
    end
    if kline>=1
        op1=kline;
        op3=X(:,1:kline);
        op31=Y(:,1:kline);
    end
end
end