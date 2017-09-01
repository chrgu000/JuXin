function HedgeRuMNew
file1='HedgeRuMNew';
file2='HedgeHedgeRuMNewT';
future='ru.shf';
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
                results=[results,diffUp(214)-diffUp(223)];%WinRatio: 0.57, Sharpe: 0.218, Return: 9.5%, MaxDraw: 2.3%
                results=[results,diffUp(149)-diffUp(139)];%WinRatio: 0.55, Sharpe: 0.223, Return: 5.3%, MaxDraw: 0.8%
                results=[results,diffUp(129)-diffUp(123)];%WinRatio: 0.57, Sharpe: 0.228, Return: 4.5%, MaxDraw: 1.2%
                results=[results,diffUp(116)-diffUp(109)];%WinRatio: 0.53, Sharpe: 0.162, Return: 3.5%, MaxDraw: 1.2%
            case 2
                Matrix2=[Matrix2;diffUp'];
            case 3
                Matrix3=[Matrix3;diffUp'];
                results=[results,diffUp(195)-diffUp(182)];%WinRatio: 0.66, Sharpe: 0.369, Return: 8.9%, MaxDraw: 1.0%
                results=[results,diffUp(150)-diffUp(145)];%WinRatio: 0.62, Sharpe: 0.303, Return: 5.7%, MaxDraw: 0.6%
                results=[results,diffUp(101)-diffUp(112)];%WinRatio: 0.65, Sharpe: 0.308, Return: 10.1%, MaxDraw: 0.7%
            case 4
                Matrix4=[Matrix4;diffUp'];
                results=[results,diffUp(202)-diffUp(210)];%WinRatio: 0.62, Sharpe: 0.188, Return: 5.1%, MaxDraw: 1.1%
            case 5
                Matrix5=[Matrix5;diffUp'];    
                results=[results,diffUp(181)-diffUp(177)];%WinRatio: 0.53, Sharpe: 0.183, Return: 3.2%, MaxDraw: 1.0%
                results=[results,diffUp(75)-diffUp(83)];%WinRatio: 0.64, Sharpe: 0.196, Return: 5.7%, MaxDraw: 1.5%
                results=[results,diffUp(75)-diffUp(66)];%WinRatio: 0.59, Sharpe: 0.156, Return: 3.2%, MaxDraw: 0.9%
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
end
