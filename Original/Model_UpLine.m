function [op1,op2,op3,ord]=Model_UpLine(High,Low,Close,Vol)
%  Model_UpLine Summary of this function goes here
%  move up for a long time and then move with a little fluctuation for a
%  long time.
global high low;
op1=0;
op2=0;
op3=0;
ord=0;
high=High;
low=Low;
close=Close;
vol=Vol;
L=length(high);
if high(L)>high(L-1) && L>55
    Kh=highest(L-45,L-1);
    for i=Kh:-1:L-floor(5*Kh/2)
        if i<=0 || i<3*Kh-2*L
            break;
        end
        lastL=lowest(Kh,L);
        if low(i)<=low(lowest(i,Kh)) && high(highest(i,Kh))<=high(Kh) && low(i)+(high(Kh)-low(i))*0.5<=low(lastL)

            z=((high(Kh)-low(i))/(Kh-i))*((i:Kh)-i)+low(i);
            if sum(z'-low(i:Kh)) < 0
                break;
            end
            
            x(1)=0;
            n=1;
            for j=Kh:5:L-1
                if j+6 >L 
                    break;
                end
                x(n)=highest(j,j+5); 
                if  high(x(n))>= high(highest(x(n)-1,x(n)+1))
                    y(n)=high(x(n));
                    n=n+1;
                end
            end
            if  n>2 && length(x)==length(y) % it means at least one point have been selected. 
                hi_l=highest(j+1,L-1);
                if j+1<L-1
                    if high(hi_l)>=high(highest(hi_l-1,hi_l+1))
                        x(n)=hi_l;
                        y(n)=high(x(n));
                    end
                end   
                x=x';y=y';
                if length(x)<=1
                    break;
                end

%                     x1=x(1);
%                     y1=y(1);
%                     f=fit(x,y,fittype('a*(x-x1)+y1','independent','x'));
                f=fit(x,y,'poly1','weights',[1000,ones(1,length(x)-1)]); % keep the first one point;
                dif=abs(f(x)-y);
                while length(dif)>2 % delete the differentest points so that the length of 'dif' is within 2 points.
                    [~,b]=max(dif);
                    x(b)='';
                    y(b)='';
                    dif(b)='';
                end
                    
                k=(y(2)-y(1))/(x(2)-x(1));
                dome0=k*(L-x(1)+2)+y(1);
                dome1=k*(L-x(1))+y(1);
                dome2=k*(L-1-x(1))+y(1);                
                if close(L)>dome1 && close(L-1)<=dome2
                    op1=1;
                    op2=[x(1) L+2;y(1) dome0;x';y'];
                    op3=[i,Kh,L;low(i),high(Kh),high(L)];
                    
                    ord1=mean(vol(i:Kh));
                    ord2=mean(vol(Kh:L));
                    ord=[(i+Kh)/2,high(Kh),10;(Kh+L)/2,high(Kh),roundn(ord2*10/ord1,-2)];
                    if abs((ord1-ord2)/ord1)>0.45
                        op1=2;
                    end

%                     srsz=get(0,'ScreenSize');
%                     figure('Position',[srsz(3)/8,srsz(4)/8,srsz(3)*3/4,srsz(4)*3/4]);
%                     subplot(3,1,[1,2]);
%                     Kplot(open,high,low,close);
%                     title(IDName);
%                     grid on;
%                     hold on;
%                     plot([i;Kh;L],[low(i);high(Kh);high(L)]);
%                     line([x(1) L+2],[y(1) dome0],'color','r'); % 也可以用ezplot('3*x+6');
%                     plot(x,y,'*');
%                     subplot(3,1,3);
%                     MACD(close);
                end
                break;
            end
        end
    end
end
end