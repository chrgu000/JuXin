function op=HedgeFH
w=windmatlab;
[IH,~,~,Date]=w.wsd('ih.cfe','close','20150416',today-1);
IF=w.wsd('if.cfe','close','20150416',today-1);

L=length(IH);
results=zeros(1,L);
plus=0;
minus=0;
for i=3:L  
    temLast=IF(i-1)/IF(i-2)-IH(i-1)/IH(i-2);
    tem=IF(i)/IF(i-1)-IH(i)/IH(i-1);
    wd=weekday(Date(i))-1;
    Lresults=sum(results~=0);
    switch wd
        case 1
            if temLast>=-0.0082  % hold status on monday;
                results(i)=-tem;
            else
                results(i)=tem;
            end
        case 2
            if temLast>=-0.0213
                results(i)=tem;
            else
                results(i)=-tem;
            end
        case 3
            results(i)=tem;
        case 4
            results(i)=tem;
%             if temLast>=-0.0344
%                 results(i)=tem;
%             else 
%                 results(i)=-tem;
%             end
        case 5
            if temLast>=-0.03
                results(i)=tem;
            else
                %results(i)=-tem;
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
[AX,H1,H2]=plotyy(1:L,[IF,IH],1:L,y*100);
title('IF和IH多空完全对冲','fontsize',16);
xlabel('时间','fontsize',12);
set(AX(1),'xTick',1:20:L);
Date=datestr(Date,'yyyy-mm-dd');
dateTarget=mat2cell(Date,ones(size(Date,1),1),size(Date,2));
set(AX(1),'xTicklabel',dateTarget(1:20:L),'XTickLabelRotation',60);
set(get(AX(1),'ylabel'),'string','股指期货指数','fontsize',12);
set(get(AX(2),'ylabel'),'string','策略涨跌指数（%）','fontsize',12);
set(AX(2), 'YColor', 'r')
set(H2,'color','k');
legend('IF连续','IH连续','策略曲线','location','NorthOutside','Orientation','horizontal');
grid on;
axes(AX(2));
hold on;
plot(maxInd,y(maxInd)*100,'r*');
hold off;
end

