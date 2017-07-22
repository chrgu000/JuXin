function HedgeZnRb % Zn vs Rb
try
    load HedgeZnRb;
catch
    w=windmatlab;
    [A,~,~,Date]=w.wsd('ZN.SHF','open,close','20140929',today-1);
    B=w.wsd('RB.SHF','open,close','20140929',today-1);
    AOpen=A(:,1);
    AClose=A(:,2);
    BOpen=B(:,1);
    BClose=B(:,2);
    save HedgeZnRb AOpen AClose BOpen BClose Date;
end
L=length(AOpen);
results=zeros(1,L);
plus=0;
minus=0;
for i=3:L  
    temLast=BClose(i-1)/BClose(i-2)-AClose(i-1)/AClose(i-2);
    tem=BClose(i)/BClose(i-1)-AClose(i)/AClose(i-1);
    wd=weekday(Date(i))-1;
    switch wd
        case 1 % hold status on monday;
            results(i)=tem;
        case 2
%             results(i)=tem;
        case 3
%             results(i)=-tem;
        case 40
            results(i)=-tem;
        case 5
%             results(i)=tem;
    end
    if results(i)>0
        plus=plus+1;
    elseif results(i)<0
        minus=minus+1;
    end
end
resultsCopy=results(results~=0);
y=cumsum(results);
maxDown=0;
for i=2:length(y)
    maxTem=max(y(1:i))-y(i);
    if maxTem>maxDown
        maxDown=maxTem;
        maxInd=i;
    end
end

display([plus/(plus+minus),y(end),mean(resultsCopy)/std(resultsCopy),maxDown]);
fprintf('winRatio: %.2f%%;return:%.3f;sharpe: %.3f; maxDown:%.1f%%\n',...
    plus/(plus+minus)*100,y(end),mean(resultsCopy)/std(resultsCopy),maxDown*100);
figure;
[AX,H1,H2]=plotyy(1:L,[AClose,BClose*(max(AClose)/max(BClose))],1:L,y*100);%AX stand by two figures; H1 and H2 stand by two lines;
title('A和B多空完全对冲','fontsize',16);
xlabel('时间','fontsize',12);
set(AX(1),'xTick',1:20:L);
Date=datestr(Date,'yyyy-mm-dd');
dateTarget=mat2cell(Date,ones(size(Date,1),1),size(Date,2));
set(AX(1),'xTicklabel',dateTarget(1:20:L),'XTickLabelRotation',60);
set(get(AX(1),'ylabel'),'string','股指期货指数','fontsize',12);
set(get(AX(2),'ylabel'),'string','策略涨跌指数（%）','fontsize',12);
set(AX(2), 'YColor', 'r')
set(H2,'color','k');
legend('A连续','B连续','策略曲线','location','NorthOutside','Orientation','horizontal');
grid on;
axes(AX(2));
hold on;
plot(maxInd,y(maxInd)*100,'r*');
hold off;
end
