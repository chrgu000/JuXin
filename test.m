function test %建模平行四边形 锌 5分钟 2017-5-5； 该工作未结束；
w=windmatlab;
% data=w.wsi('ru1709.shf','high,low,close,open','2017-05-04 09:00:00','2017-05-05 13:07:27','BarSize=5;PriceAdj=F');
data=w.wsi('000001.sh','high,low,close,open','2017-05-04 09:00:00','2017-05-05 13:07:27','BarSize=5;PriceAdj=F');
ind=data(:,1)==data(:,2);
data=data(~ind,:);
high=data(end-44:end-27,1);
low=data(end-44:end-27,2);
close=data(end-44:end-27,3);
open=data(end-44:end-27,4);
L=length(open);
x=[1:L]';
y=low;
p=fittype('poly1');
f=fit(x,y,p);
figure;
subplot(211);
candle(high,low,close,open);
hold on;
plot(f,'y');
yFit=f(x);
diff=yFit-y;
ind=diff>0;
x=x(ind);
y=y(ind);
f=fit(x,y,p);
plot(f,'g');
numberP=length(x);

while numberP>3
    f=fit(x,y,p);
    yFit=f(x);
    diff=abs(yFit-y);
    [~,ind]=sort(diff);
    x=x(ind(1:end-1));
    y=y(ind(1:end-1));
    numberP=numberP-1;  
end

f=fit(x,y,p);
plot(f,'b');
plot(x,y,'r*')

Y=f(1:L);
Diff=low-Y; % abs is less effective;
mean(Diff./close)
subplot(212);
bar(Diff);


end