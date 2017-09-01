function LSG(stock)
w=windmatlab;
data=w.wsd(stock,'open,close,high,low','ED-1000TD',today-1,'Fill=Previous','PriceAdj=F');
open=data(:,1);
close=data(:,2);
high=data(:,3);
low=data(:,4);
L=length(open);
upline=zeros(1,L);
downline=zeros(1,L);
atr=zeros(1,L);
ema3=zeros(1,L);
ema25=zeros(1,L);
for i=31:L %获取上线，下线，atr序列值,ema值
    upline(i)=max(high(i-6:i));
    downline(i)=min(low(i-6:i));
    atr0=zeros(1,9);
    for j=0:8
        atr1=high(i-j)-low(i-j);
        atr2=abs(close(i-j-1)-high(i-j));
        atr3=abs(close(i-j)-low(i-j));
        atr0(j+1)=max([atr1,atr2,atr3]);
    end 
    atr(i)=mean(atr0);
    ema3(i)=mean(close(i-2:i));
    ema25(i)=mean(close(i-24:i));
end
Popen=0; %开仓价格
Pstop=0; %止损价格
Return=zeros(1,L-25);
for i=31:L %开始回测
    if Popen==0 && ema3(i)>ema25(i) && high(i)>upline(i-1) %满足开多条件
        Popen=upline(i)+0.01;     
        Pstop=upline(i)-2.5*atr(i);
    end
    if Popen~=0 
        if low(i)<Pstop % 此处止损出场，还应该加加入止盈出场条件；
            returnTem=(Pstop-Popen)/Popen;
            Return(i)=returnTem;
            Pstop=0;
            Popen=0;
        else 
            returnTem=(close(i)-Popen)/Popen;
            Return(i)=returnTem;
        end
    end
    if Popen==0 && Return(i-1)~=0
        Return(i)=Return(i-1);
    end   
end

plot(Return); %画出资金曲线

end