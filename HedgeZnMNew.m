function HedgeZnMNew  %Îå¿óÒ»À¿×Ó½»Ò× test6 ²âÊÔÃÜÂë£ºqwe123!@#
file1='HedgeZnMNew';
file2='HedgeHedgeZnMNewT';
future='zn.shf';
Matrix1=[];
Matrix2=[];
Matrix3=[];
Matrix4=[];
Matrix5=[];

f1=figure;
for j=1:2
    if j==1
        try 
            load(file1);
        catch
            w=windmatlab;
            endStr=datestr(today-361,'yyyymmdd');
            [Xminutes,~,~,Time]=w.wsi(future,'close','20140101 09:00:00',[endStr,'15:01:00'],...
                'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            indTem=~isnan(Xminutes);
            Xminutes=Xminutes(indTem);
            Time=Time(indTem);
            TimeR=floor(Time);
            step=sum(TimeR(1)==TimeR);
            save(file1, 'Xminutes', 'Time', 'step');
        end    
    else
        try 
            load(file2); % test your selected times;
        catch
            w=windmatlab;
            startStr=datestr(today-360,'yyyymmdd');
            endStr=datestr(today-1,'yyyymmdd');
            [Xminutes,~,~,Time]=w.wsi(future,'close',[startStr,' 09:00:00'],[endStr,' 15:01:00'],...
                'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            indTem=~isnan(Xminutes);
            Xminutes=Xminutes(indTem);
            Time=Time(indTem);
            TimeR=floor(Time);
            step=sum(TimeR(1)==TimeR);
            save(file2,'Xminutes','Time','step');
        end       
    end
    
    L=length(Time);
    results=[];
    for i=step:step:L-step  
        diffUp=Xminutes(i+1:i+step)/Xminutes(i);
        %     diffUp=diffUp/max(abs(diffUp));
        wd=weekday(Time(i+1))-1;   
        switch wd
            case 1   
                Matrix1=[Matrix1;diffUp'];
            case 2
                Matrix2=[Matrix2;diffUp'];
                results=[results,diffUp(69)-diffUp(80)];%WinRatio: 0.65, Sharpe: 0.242, Return: 3.6%, MaxDraw: 1.0%
                results=[results,diffUp(69)-diffUp(61)];%WinRatio: 0.55, Sharpe: 0.148, Return: 2.0%, MaxDraw: 0.8%
                results=[results,diffUp(26)-diffUp(45)];%WinRatio: 0.56, Sharpe: 0.276, Return: 4.9%, MaxDraw: 0.5%
            case 3
                Matrix3=[Matrix3;diffUp'];
                results=[results,diffUp(98)-diffUp(108)];%WinRatio: 0.57, Sharpe: 0.220, Return: 3.0%, MaxDraw: 0.8%
                results=[results,diffUp(56)-diffUp(63)];%WinRatio: 0.51, Sharpe: 0.181, Return: 2.4%, MaxDraw: 0.8%
            case 4
                Matrix4=[Matrix4;diffUp'];
                results=[results,diffUp(150)-diffUp(144)];%WinRatio: 0.65, Sharpe: 0.253, Return: 3.2%, MaxDraw: 0.4%
                results=[results,diffUp(86)-diffUp(80)];%WinRatio: 0.64, Sharpe: 0.284, Return: 2.8%, MaxDraw: 0.4%
                results=[results,diffUp(75)-diffUp(80)];%WinRatio: 0.65, Sharpe: 0.255, Return: 3.2%, MaxDraw: 0.5%
            case 5
                Matrix5=[Matrix5;diffUp'];    
        end
    end
    plus=sum(results>0);
    minus=sum(results<0);
    winratio=plus/(plus+minus);
    sharpe=mean(results)/std(results);
    results=cumsum(results);
    maxdraw=0;
    for i=2:length(results)
        tem=max(results(1:i))-results(i);
        if maxdraw<tem
            maxdraw=tem;
            indx=i;
        end
    end
    
    figure(f1);
    plot(results);
    hold on;
    plot(indx,results(indx),'r*');
    grid on;
    fprintf('WinRatio: %.2f, Sharpe: %.3f, Return: %.1f%%, MaxDraw: %.1f%%\n',winratio,sharpe,results(end)*100,maxdraw*100);
    
%     if j==1
%         figure;
%         plotyy(1:226,mean(Matrix1),1:226,std(Matrix1));
%         set(gca,'xtick',1:5:226);
%         grid on;   
%         
%         figure;
%         plotyy(1:226,mean(Matrix2),1:226,std(Matrix2));
%         set(gca,'xtick',1:5:226);
%         grid on;   
%         
%         figure;
%         plotyy(1:226,mean(Matrix3),1:226,std(Matrix3));
%         set(gca,'xtick',1:5:226);
%         grid on;   
%         
%         figure;
%         plotyy(1:226,mean(Matrix4),1:226,std(Matrix4));
%         set(gca,'xtick',1:5:226);
%         grid on;   
%         
%         figure;
%         plotyy(1:226,mean(Matrix5),1:226,std(Matrix5));
%         set(gca,'xtick',1:5:226);
%         grid on;            
%     end         

end


% [~,f1,~]=anova1(Matrix1)
% [~,f2,~]=anova1(Matrix2)
% [~,f3,~]=anova1(Matrix3)
% [~,f4,~]=anova1(Matrix4)
% [~,f5,~]=anova1(Matrix5)