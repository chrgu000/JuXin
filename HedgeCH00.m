function HedgeCH00
forwardTest=1;
reset=0;
if reset
    delete HedgeCH00Train.mat HedgeCHminutes00Train.mat  HedgeCH00Test.mat HedgeCHminutes00Test.mat
end
if forwardTest
    loops=1;
else
    loops=2;
end
for loop=1:loops
    if loop==1 && ~forwardTest % back test this strategy;
        try
            load HedgeCH00Train;
        catch
            w=windmatlab;
            dayT=datestr(today-180,'yyyymmdd');
            [IH,~,~,Date]=w.wsd('ih00.cfe','open,close','20150416',dayT);
            IC=w.wsd('ic00.cfe','open,close','20150416',dayT);
            clear w;
            save HedgeCH00Train IH Date IC;
        end
        try 
            load HedgeCHminutes00Train;
        catch
            w=windmatlab;
            dayT=datestr(today-180,'yyyymmdd');
            [IHminutes,~,~,Time]=w.wsi('ih00.cfe','close','20150416 09:00:00',[dayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            ICminutes=w.wsi('ic00.cfe','close','20150416 09:00:00',[dayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            clear w;
            save HedgeCHminutes00Train IHminutes ICminutes Time;
        end
    elseif  loop==2 && ~forwardTest% forward test this strategy;
        try
            load HedgeCH00Test;
        catch
            w=windmatlab;
            dayT=datestr(today-179,'yyyymmdd');
            [IH,~,~,Date]=w.wsd('ih00.cfe','open,close',dayT,today-1);
            IC=w.wsd('ic00.cfe','open,close',dayT,today-1);
            clear w;
            save HedgeCH00Test IH Date IC;
        end
        try 
            load HedgeCHminutes00Test;
        catch
            w=windmatlab;
            dayT=datestr(today-179,'yyyymmdd');
            todayT=datestr(today-1,'yyyymmdd');
            [IHminutes,~,~,Time]=w.wsi('ih00.cfe','close',[dayT,' 09:00:00'],[todayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            ICminutes=w.wsi('ic00.cfe','close',[dayT,' 09:00:00'],[todayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            clear w;
            save HedgeCHminutes00Test IHminutes ICminutes Time;
        end
    elseif forwardTest
        w=windmatlab;
        load HedgeCH00Test;
        dayT=datestr(Date(end),'yyyymmdd');
        [IH,~,~,Date]=w.wsd('ih00.cfe','open,close',dayT,today-1);
        IC=w.wsd('ic00.cfe','open,close',dayT,today-1);
        todayT=datestr(today-1,'yyyymmdd');
        [IHminutes,~,~,Time]=w.wsi('ih00.cfe','close',[dayT,' 09:00:00'],[todayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
        ICminutes=w.wsi('ic00.cfe','close',[dayT,' 09:00:00'],[todayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
        clear w;         
    end
    IHOpen=IH(:,1);
    IHClose=IH(:,2);
    ICOpen=IC(:,1);
    ICClose=IC(:,2);
    L=length(IHOpen);
    results=zeros(1,L);
    plus=0;
    minus=0;
    for i=3:L-1  
        temLast=ICClose(i-1)/ICClose(i-2)-IHClose(i-1)/IHClose(i-2);
        tem=ICClose(i)/ICClose(i-1)-IHClose(i)/IHClose(i-1);
        wd=weekday(Date(i))-1;

        ii=i-1;
        ICMup=ICminutes(ii*241+1:ii*241+241)/ICClose(i-1);
        IHMup=IHminutes(ii*241+1:ii*241+241)/IHClose(i-1);
        diffUp=ICMup-IHMup;   

        switch wd
            case 1 % hold status on monday; 
                stoploss=-0.00729;
                results(i)=-tem;
                for j=1:240                 
                    if -diffUp(j)<=stoploss
                        results(i)=-diffUp(j)+...                        
                            (ICminutes(ii*241+242)-ICminutes(ii*241+j))/ICminutes(ii*241+j)+...
                            (IHminutes(ii*241+j)-IHminutes(ii*241+242))/IHminutes(ii*241+j);
                        break;                  
                    end                
                end
            case 2
                stoploss=-0.011;%-0.011
                if temLast>=-0.05 && temLast<=0.075 % -5%  <= diff <= 7.5%
                    results(i)=tem;
                    for j=1:240
                        if diffUp(j)<stoploss  
                            results(i)=diffUp(j);%+(ICminutes(ii*241+242)-ICminutes(ii*241+j))/ICminutes(ii*241+j)+(IHminutes(ii*241+j)-IHminutes(ii*241+242))/IHminutes(ii*241+j);
                            break;
                        end
                    end
                else
                    results(i)=-tem;
                    for j=1:240      
                        if -diffUp(j)<=stoploss
                            results(i)=-diffUp(j)+...     
                                (ICminutes(ii*241+242)-ICminutes(ii*241+j))/ICminutes(ii*241+j)+...
                                (IHminutes(ii*241+j)-IHminutes(ii*241+242))/IHminutes(ii*241+j);
                            break;                  
                        end
                    end
                end
            case 3          
                if temLast>=-0.006 %  0.6% <= diff
                    results(i)=-tem;
                else  % this item is perfect;
                    results(i)=tem;
                    stopprofit=0.0122;
                    for j=1:240
                        if diffUp(j)>=stopprofit
                            results(i)=diffUp(j);
                            break;
                        end
                    end
                end
            case 40
                stopprofit=0.228;
                results(i)=tem;
                for j=1:240
                    if diffUp(j)>=stopprofit
                        results(i)=diffUp(j);
                        break;
                    end
                end
            case 50 % delete this item to make max drawback from 0.0967 up to 0.0766;
                results(i)=tem;
                stoploss=-0.001;
%                 for j=1:240
%                     if diffUp(j)<stoploss
%                         results(i)=diffUp(j)%-...
%                             ( (ICminutes(ii*241+242)-ICminutes(ii*241+j))/ICminutes(ii*241+j)+...
%                             (IHminutes(ii*241+j)-IHminutes(ii*241+242))/IHminutes(ii*241+j) ); 
%                         break;
%                     end
%                 end
    %             stoploss=0.002;
    %             for j=1:240
    %                 if diffUp(j)<stoploss
    %                     results(i)=-( (ICminutes(ii*241+242)-ICminutes(ii*241+j))/ICminutes(ii*241+j)+...
    %                         (IHminutes(ii*241+j)-IHminutes(ii*241+242))/IHminutes(ii*241+j) ); 
    %                     break;
    %                 end
    %             end
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
    fprintf('winRatio:%.1f%%,result:%.2f,sharpe:%.3f,maxDown:%.1f%%,orders:%d\n',plus*100/(plus+minus),y(end),mean(resultsCopy)/std(resultsCopy),maxDown*100,length(resultsCopy));
    figure;
    [AX,H1,H2]=plotyy(1:L,[IHClose,ICClose],1:L,y*100);%AX stand by two figures; H1 and H2 stand by two lines;
    title('IH和IC多空完全对冲','fontsize',16);
    xlabel('时间','fontsize',12);
    step=floor(L/24);
    set(AX(1),'xTick',1:step:L);
    Date=datestr(Date,'yyyy-mm-dd');
    dateTarget=mat2cell(Date,ones(size(Date,1),1),size(Date,2));
    set(AX(1),'xTicklabel',dateTarget(1:step:L),'XTickLabelRotation',60);
    set(get(AX(1),'ylabel'),'string','股指期货指数','fontsize',12);
    set(get(AX(2),'ylabel'),'string','策略涨跌指数（%）','fontsize',12);
    set(AX(2), 'YColor', 'r')
    set(H2,'color','k');
    legend('IH连续','IC连续','策略曲线','location','NorthOutside','Orientation','horizontal');
    grid on;
    axes(AX(2));
    hold on;
    plot(maxInd,y(maxInd)*100,'r*');
    hold off;
end
end


% function HedgeCH00
% testback=0;
% if testback
%     try
%         load HedgeCH00;
%     catch
%         w=windmatlab;
%         [IH,~,~,Date]=w.wsd('ih00.cfe','open,close','20150416',today-1);
%         IC=w.wsd('ic00.cfe','open,close','20150416',today-1);
%         clear w;
%         save HedgeCH00 IH Date IC;
%     end
%     try 
%         load HedgeCHminutes00;
%     catch
%         w=windmatlab;
%         todayT=datestr(today-1,'yyyymmdd');
%         [IHminutes,~,~,Time]=w.wsi('ih00.cfe','close','20150416 09:00:00',[todayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
%         ICminutes=w.wsi('ic00.cfe','close','20150416 09:00:00',[todayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
%         clear w;
%         save HedgeCHminutes00 IHminutes ICminutes Time;
%     end
% else
%     w=windmatlab;
%     [IH,~,~,Date]=w.wsd('ih00.cfe','open,close','20170511',today-1);
%     IC=w.wsd('ic00.cfe','open,close','20170511',today-1);
%     todayT=datestr(today-1,'yyyymmdd');
%     [IHminutes,~,~,Time]=w.wsi('ih00.cfe','close','20170511 09:00:00',[todayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
%     ICminutes=w.wsi('ic00.cfe','close','20170511 09:00:00',[todayT,' 15:01:00'],'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
%     clear w;    
% end
% IHOpen=IH(:,1);
% IHClose=IH(:,2);
% ICOpen=IC(:,1);
% ICClose=IC(:,2);
% L=length(IHOpen);
% results=zeros(1,L);
% plus=0;
% minus=0;
% for i=3:L  
%     temLast=ICClose(i-1)/ICClose(i-2)-IHClose(i-1)/IHClose(i-2);
%     tem=ICClose(i)/ICClose(i-1)-IHClose(i)/IHClose(i-1);
%     wd=weekday(Date(i))-1;
%     
%     ii=i-1;
%     ICMup=ICminutes(ii*241+1:ii*241+241)/ICClose(i-1);
%     IHMup=IHminutes(ii*241+1:ii*241+241)/IHClose(i-1);
%     diffUp=ICMup-IHMup;
%     
%     switch wd
%         case 1 % hold status on monday;            
%             if temLast>=-0.0180 && temLast<=0.0279 %  -1.8% <= diff <= 2.79%
%                 results(i)=-tem;
%             elseif temLast<0.037 % diff <= 3.7%
%                 results(i)=tem;
%             end
%         case 2
%             if temLast>=-0.05 && temLast<=0.075 % -5%  <= diff <= 7.5%
%                 results(i)=tem;
%             else
%                 results(i)=-tem;
%             end
%         case 3
%             if temLast>=-0.006 %  0.6% <= diff
%                 results(i)=-tem;
%             else
%                 results(i)=tem;
%             end
%         case 40
%             if temLast>=-0.065 %  6.5% <= diff
%                 results(i)=tem;
%             else
%                 results(i)=-tem;
%             end
%         case 50 % delete this item to make max drawback from 0.0967 up to 0.0766;
%             if temLast>=0.031 % 3.1% <= diff
%                 results(i)=-tem;
%             else
%                 results(i)=tem;
%             end
%     end
%     
%     stopLoss=-0.011; % if loss more than 1.1%, close this order;
%     if results(i)==tem && wd~=3
%         if diffUp(1)<stopLoss
%             results(i)=diffUp(1);
%         elseif min(diffUp)<stopLoss
%             results(i)=stopLoss;
%         end
%     elseif results(i)==-tem && wd~=3
%         diffUp=-diffUp;
%         if diffUp(1)<stopLoss
%             results(i)=diffUp(1);
%         elseif min(diffUp)<stopLoss
%             results(i)=stopLoss;
%         end        
%     end   
%     
%     if results(i)>0
%         plus=plus+1;
%     elseif results(i)<0
%         minus=minus+1;
%     end
% end
% resultsCopy=results(results~=0);
% y=cumsum(results);
% maxDown=0;
% for i=2:length(y)
%     maxTem=max(y(1:i))-y(i);
%     if maxTem>maxDown
%         maxDown=maxTem;
%         maxInd=i;
%     end
% end
% fprintf('winRatio:%.1f%%,result:%.2f,sharpe:%.3f,maxDown:%.1f%%\n',plus*100/(plus+minus),y(end),mean(resultsCopy)/std(resultsCopy),maxDown*100);
% figure;
% [AX,H1,H2]=plotyy(1:L,[IHClose,ICClose],1:L,y*100);%AX stand by two figures; H1 and H2 stand by two lines;
% title('IH和IC多空完全对冲','fontsize',16);
% xlabel('时间','fontsize',12);
% set(AX(1),'xTick',1:20:L);
% Date=datestr(Date,'yyyy-mm-dd');
% dateTarget=mat2cell(Date,ones(size(Date,1),1),size(Date,2));
% set(AX(1),'xTicklabel',dateTarget(1:20:L),'XTickLabelRotation',60);
% set(get(AX(1),'ylabel'),'string','股指期货指数','fontsize',12);
% set(get(AX(2),'ylabel'),'string','策略涨跌指数（%）','fontsize',12);
% set(AX(2), 'YColor', 'r')
% set(H2,'color','k');
% legend('IH连续','IC连续','策略曲线','location','NorthOutside','Orientation','horizontal');
% grid on;
% axes(AX(2));
% hold on;
% plot(maxInd,y(maxInd)*100,'r*');
% hold off;
% end

