function op=HedgeCF
w=windmatlab;
[IC,~,~,Date]=w.wsd('ic.cfe','close','20150416',today-1);
IF=w.wsd('if.cfe','close','20150416',today-1);

L=length(IC);
results=zeros(1,L);
plus=0;
minus=0;
for i=3:L  
    temLast=IC(i-1)/IC(i-2)-IF(i-1)/IF(i-2);
    tem=IC(i)/IC(i-1)-IF(i)/IF(i-1);
    wd=weekday(Date(i))-1;
    Lresults=sum(results~=0);
    switch wd
        case 1
            if temLast>=-0.014 % hold status on monday;
                results(i)=-tem;
            else
                results(i)=tem;
            end
        case 2
            if temLast>=-0.0131
                results(i)=tem;
            else
                results(i)=-tem;
            end
        case 3
            if temLast>=-0.0054 
%                 if temLast>=0.026
                results(i)=-tem;
            else
                results(i)=tem;
            end
        case 4
            if temLast>=-0.031
                results(i)=tem;
            else
                results(i)=-tem;
            end
        case 5
            if temLast>=0.021
                results(i)=-tem;
            else
                results(i)=tem;
            end
    end
    indTem=results~=0;
    if sum(indTem)>Lresults
        tem=results(indTem);
        if tem(end)>0
            plus=plus+1;
        else
            minus=minus+1;
        end
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
figure;
[AX,H1,H2]=plotyy(1:L,[IF,IC],1:L,y*100);
title('IF和IC多空完全对冲','fontsize',16);
xlabel('时间','fontsize',12);
set(AX(1),'xTick',1:20:L);
Date=datestr(Date,'yyyy-mm-dd');
dateTarget=mat2cell(Date,ones(size(Date,1),1),size(Date,2));
set(AX(1),'xTicklabel',dateTarget(1:20:L),'XTickLabelRotation',60);
set(get(AX(1),'ylabel'),'string','股指期货指数','fontsize',12);
set(get(AX(2),'ylabel'),'string','策略涨跌指数（%）','fontsize',12);
set(AX(2), 'YColor', 'r')
set(H2,'color','k');
legend('IF连续','IC连续','策略曲线','location','NorthOutside','Orientation','horizontal');
grid on;
axes(AX(2));
hold on;
plot(maxInd,y(maxInd)*100,'r*');
hold off;

end