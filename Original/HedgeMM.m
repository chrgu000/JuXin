function HedgeMM % Dou Po
Matrix1=[];
Matrix2=[];
Matrix3=[];
Matrix4=[];
Matrix5=[];

f1=figure;
for j=1:2
    if j==1
        try 
            load HedgeMM;
        catch
            w=windmatlab;
            endStr=datestr(today-361,'yyyymmdd');
            [Xminutes,~,~,Time]=w.wsi('m.dce','close','20140101 09:00:00',[endStr,'15:01:00'],...
                'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            indTem=~isnan(Xminutes);
            Xminutes=Xminutes(indTem);
            Time=Time(indTem);
            TimeR=floor(Time);
            step=sum(TimeR(1)==TimeR);
            save HedgeMM Xminutes Time step;
        end    
    else
        try 
            load HedgeMMT;
        catch
            w=windmatlab;
            startStr=datestr(today-360,'yyyymmdd');
            endStr=datestr(today-1,'yyyymmdd');
            [Xminutes,~,~,Time]=w.wsi('m.dce','close',[startStr,' 09:00:00'],[endStr,' 15:01:00'],...
                'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            indTem=~isnan(Xminutes);
            Xminutes=Xminutes(indTem);
            Time=Time(indTem);
            TimeR=floor(Time);
            step=sum(TimeR(1)==TimeR);
            save HedgeMMT Xminutes Time step;
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
                results=[results,diffUp(192)-diffUp(201)];%WinRatio: 0.59, Sharpe: 0.109, Return: 3.4%, MaxDraw: 1.9%
                results=[results,diffUp(96)-diffUp(86)];%WinRatio: 0.56, Sharpe: 0.182, Return: 2.2%, MaxDraw: 0.6%
                results=[results,diffUp(76)-diffUp(86)];%WinRatio: 0.59, Sharpe: 0.261, Return: 3.2%, MaxDraw: 0.5%
            case 2
                Matrix2=[Matrix2;diffUp'];
            case 3
                Matrix3=[Matrix3;diffUp'];
            case 4
                Matrix4=[Matrix4;diffUp'];
                results=[results,diffUp(189)-diffUp(201)];%WinRatio: 0.58, Sharpe: 0.196, Return: 2.6%, MaxDraw: 1.0%
                results=[results,diffUp(151)-diffUp(157)];%WinRatio: 0.62, Sharpe: 0.231, Return: 2.2%, MaxDraw: 0.3%
                results=[results,diffUp(16)-diffUp(31)];%WinRatio: 0.57, Sharpe: 0.232, Return: 4.4%, MaxDraw: 0.9%
            case 5
                Matrix5=[Matrix5;diffUp'];    
                results=[results,diffUp(51)-diffUp(67)];%WinRatio: 0.60, Sharpe: 0.216, Return: 3.5%, MaxDraw: 0.8%
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
    
    if j==1
        figure;
        plotyy(1:226,mean(Matrix1),1:226,std(Matrix1));
        set(gca,'xtick',1:5:226);
        grid on;   
        
        figure;
        plotyy(1:226,mean(Matrix2),1:226,std(Matrix2));
        set(gca,'xtick',1:5:226);
        grid on;   
        
        figure;
        plotyy(1:226,mean(Matrix3),1:226,std(Matrix3));
        set(gca,'xtick',1:5:226);
        grid on;   
        
        figure;
        plotyy(1:226,mean(Matrix4),1:226,std(Matrix4));
        set(gca,'xtick',1:5:226);
        grid on;   
        
        figure;
        plotyy(1:226,mean(Matrix5),1:226,std(Matrix5));
        set(gca,'xtick',1:5:226);
        grid on;   
        
    end         
end


% [~,f1,~]=anova1(Matrix1)
% [~,f2,~]=anova1(Matrix2)
% [~,f3,~]=anova1(Matrix3)
% [~,f4,~]=anova1(Matrix4)
% [~,f5,~]=anova1(Matrix5)
end
