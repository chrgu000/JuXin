function [op1,op3,op31,ord,ratio]=Model_UpDown_Half
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
selected=false;
if low(lowest(L-2,L))>=low(L) %&& L>4*cycleD
    kline=0;
    for j=3:50     
        if L-j-4 <=0
            break;
        end
        if j<15
            pointH=highest(L-4*j+3,L); %big high point
            pointl=lowest(L-j-1,L-j);%small low point
            pointlen=L-pointH; 
            if pointlen>0&&L-2*pointlen-10>0
                pointL=lowest(L-2*pointlen-1,L-2*pointlen+1); %big low point
            else
                continue
            end
            pointh=highest(L-ceil(j/2),L-floor(j/2));%small high point for mod(j,2)==1
            ratio_tem=(high(pointH)-low(lowest(pointH,L)))/(high(pointH)-low(pointL));
            if ( (mod(j,2)==0&&high(L-j/2)>=high(highest(L-j,L))&&low(lowest(L-j-1,L-j+1))<=low(lowest(pointH,L-j/2)) && low(lowest(L-j/2,L))>=low(lowest(L-j-2,L-j/2))-0.01)... % small up_down
                    || (mod(j,2)==1&& high(pointh)>=high(highest(L-j,L)) &&low(lowest(L-j-1,L-j))<=low(lowest(L-2*j,pointh))&&low(lowest(L-pointh,L))>=low(lowest(L-j-2,L-pointh))-0.01 )  )...
                    && low(pointL)<=low(lowest(L-2*pointlen-10,L))&&high(pointH)>=high(highest(L-2*pointlen,L)) ...% confirm big low point and high point;
                    && abs((L-pointH)-2*(L-pointl))<=2 && ratio_tem<0.62
                selected=true;
                J=2*pointlen;  
            end
        end
        if j>=7
            pointH=highest(L-j,L);
            ratio_tem=(high(pointH)-low(L))/(high(pointH)-low(L-j));
            if low(lowest(L-floor(j/2),L-j-4))>=low(L-j) && low(L)<=low(lowest(L-ceil(j/2),L)) ...  %L-j,L-2*j-4
                   && abs(L-pointH-j/2)<2  ...  % && low(L)>=low(L-j) && L-j<pointH && L>pointH
                   && close(L)>=(low(L-j)+high(pointH))/2 && ratio_tem<0.51
               selected=true;
               J=j;
            end
            bars_len=Model_DownUpDown_Call;
            if sum(bars_len)>0
                for tem=1:5
                    if bars_len(tem)>0 && L-3*bars_len(tem)>0
                        firstH=L-2*bars_len(tem);
                        if high(highest(firstH-3,firstH+3))>=high(highest(firstH-bars_len(tem),firstH+ceil(bars_len(tem)/2)))...
                                &&low(lowest(firstH,L-bars_len(tem)))<=low(lowest(L-bars_len(tem),L))...
                                &&abs(high(highest(firstH-3,firstH+3))-high(highest(L-bars_len(tem)-2,L-bars_len(tem)+2)))/high(L-bars_len(tem))<0.05
                            J=2*bars_len(tem);
                            pointH=L-bars_len(tem);
                            kline=kline+1;
                            X(1,kline)=L-J;        Y(1,kline)=high(L-J);
                            X(2,kline)=pointH;   Y(2,kline)=high(pointH);
                            X(3,kline)=L;     Y(3,kline)=low(L);    
                        end
                    end
                end
            end
        end
                   
        if selected
            barN=J;
            if L-2*J>0
                ATR_X(L-J,L);
                ATR_X(L-2*J,L-J);
            end
            kline=kline+1;
            X(1,kline)=L-J;        Y(1,kline)=low(L-J);
            X(2,kline)=pointH;   Y(2,kline)=high(pointH);
            X(3,kline)=L;     Y(3,kline)=low(L);
            
            ord1=mean(vol(L-J:pointH));
            ord2=mean(vol(pointH:L));
            ordM=high(pointH)*1.05;
            if ord==0
                ord(1:2,:)=[(L-J+pointH)/2-2,ordM,10;(L+pointH)/2,ordM,roundn(ord2*10/ord1,-1)];
                ratio(1,:)=[L+1,low(L),roundn(ratio_tem,-3)];
            else
                rowN=sum(sum(ord')~=0);
                ord(rowN+1:rowN+2,:)=[(L-J+pointH)/2-2,ordM,10;(L+pointH)/2,ordM,roundn(ord2*10/ord1,-1)];
                ratio(rowN+1,:)=[L+1,low(L),roundn((high(pointH)-low(L))/(high(pointH)-low(L-J)),-3)];
            end
            selected=false;
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