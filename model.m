function re1=model(I)
global open high low close vol;
re1=0;
if low(I)<low(I-1) && low(I-1)<low(I-2) && high(I)<high(I-1) && high(I-1)<high(I-2)&&... 
     high(I-3)>high(I-4) && low(I-5)<low(I-6)&&...
     close(I-1)<open(I-1)&&close(I-2)<open(I-2)&&close(I-3)>open(I-3) && close(I-4)>open(I-4) && close(I)>open(I)
    re1=1;
end
end





% function [op1,op3,op31,ord]=Model_UpDown(I)
% global high low close vol;
% op1=0;
% op3=0;
% op31=0;
% ord(10,3)=0;
% cycleD=24;
% X(3,5)=0;
% Y(3,5)=0;
% 
% % xxx=0;
% 
% if low(lowest(I-2,I))>=low(I) && I>4*cycleD
%     kline=0;
%     for j=4:80     
%         if I-j-4 <=0
%             break;
%         end
%         pointH=highest(I-j,I);         
%         if low(lowest(I-floor(j/2),I-j-4))>=low(I-j) && low(I)<=low(lowest(I-ceil(j/2),I)) ...  %I-j,I-2*j-4
%                    && abs(I-pointH-j/2)<2  ...  % && low(I)>=low(I-j) && I-j<pointH && I>pointH
%                    && low(lowest(I-2*cycleD,I-4*cycleD))<=low(lowest(I-2*cycleD,I)) && high(highest(I-2*cycleD,I-4*cycleD))<=high(highest(I-2*cycleD,I)) 
%             barN=j;                    
%             kline=kline+1;
%             X(1,kline)=I-j;        Y(1,kline)=low(I-j);
%             X(2,kline)=pointH;   Y(2,kline)=high(pointH);
%             X(3,kline)=I;     Y(3,kline)=low(I);
%             
%             ord1=mean(vol(I-j:pointH));
%             ord2=mean(vol(pointH:I));
%             ordM=high(pointH)*1.05;
%             if ord==0
%                 ord(1:2,:)=[(I-j+pointH)/2-2,ordM,10;(I+pointH)/2,ordM,roundn(ord2*10/ord1,-2)];
%             else
%                 rowN=sum(sum(ord')~=0);
%                 ord(rowN+1:rowN+2,:)=[(I-j+pointH)/2-2,ordM,10;(I+pointH)/2,ordM,roundn(ord2*10/ord1,-2)];
%             end
% %             
% %             if (ord1-ord2)/ord1>=0.45
% %                 xxx=10;
% %             end
% %         
%         end
%     end
%     if kline>=1
%         op1=barN;
%         temp=sum(sum(X)~=0);
%         op3=X(:,temp);
%         op31=Y(:,temp);
%     end
% end
% end