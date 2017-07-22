function HedgeWhM % Wheet
Matrix1=[];
Matrix2=[];
Matrix3=[];
Matrix4=[];
Matrix5=[];

figure;
set(gcf, 'position', [500 600 1100 400]);
for j=1:2
    if j==1
        try 
            load HedgeWhM;
        catch
            w=windmatlab;
            endStr=datestr(today-361,'yyyymmdd');
            [Xminutes,~,~,Time]=w.wsi('wh.czc','close','20140101 09:00:00',[endStr,'15:01:00'],...
                'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            indTem=~isnan(Xminutes);
            Xminutes=Xminutes(indTem);
            Time=Time(indTem);
            TimeR=floor(Time);
            step=sum(TimeR(1)==TimeR);
            save HedgeWhM Xminutes Time step;
        end    
    else
        try 
            load HedgeWhMT;
        catch
            w=windmatlab;
            startStr=datestr(today-360,'yyyymmdd');
            endStr=datestr(today-1,'yyyymmdd');
            [Xminutes,~,~,Time]=w.wsi('wh.czc','close',[startStr,' 09:00:00'],[endStr,' 15:01:00'],...
                'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
            indTem=~isnan(Xminutes);
            Xminutes=Xminutes(indTem);
            Time=Time(indTem);
            TimeR=floor(Time);
            step=sum(TimeR(1)==TimeR);
            save HedgeWhMT Xminutes Time step;
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
                results=[results,diffUp(200)-diffUp(187)];%WinRatio: 0.65, Sharpe: 0.288, Return: 4.7%, MaxDraw: 0.7%
                results=[results,diffUp(144)-diffUp(149)];%WinRatio: 0.64, Sharpe: 0.276, Return: 2.8%, MaxDraw: 0.2%
                results=[results,diffUp(109)-diffUp(100)];%WinRatio: 0.70, Sharpe: 0.362, Return: 4.0%, MaxDraw: 0.4%
                results=[results,diffUp(25)-diffUp(20)];%WinRatio: 0.62, Sharpe: 0.184, Return: 2.5%, MaxDraw: 0.5%
                results=[results,diffUp(6)-diffUp(11)];%WinRatio: 0.63, Sharpe: 0.282, Return: 5.6%, MaxDraw: 0.5%
            case 2
                Matrix2=[Matrix2;diffUp'];
                results=[results,diffUp(132)-diffUp(145)];%WinRatio: 0.56, Sharpe: 0.148, Return: 3.2%, MaxDraw: 0.7%
                results=[results,diffUp(112)-diffUp(119)];%WinRatio: 0.63, Sharpe: 0.283, Return: 2.6%, MaxDraw: 0.3%
                results=[results,diffUp(21)-diffUp(9)];%WinRatio: 0.61, Sharpe: 0.257, Return: 7.0%, MaxDraw: 0.6%
                results=[results,diffUp(2)-diffUp(9)];%WinRatio: 0.62, Sharpe: 0.172, Return: 3.4%, MaxDraw: 1.1%
            case 3
                Matrix3=[Matrix3;diffUp'];
                results=[results,diffUp(220)-diffUp(212)];%WinRatio: 0.60, Sharpe: 0.181, Return: 2.8%, MaxDraw: 0.6%
                results=[results,diffUp(187)-diffUp(154)];%WinRatio: 0.62, Sharpe: 0.196, Return: 4.8%, MaxDraw: 0.8%
                results=[results,diffUp(65)-diffUp(72)];%WinRatio: 0.56, Sharpe: 0.225, Return: 3.1%, MaxDraw: 0.4%
            case 4
                Matrix4=[Matrix4;diffUp'];
                results=[results,diffUp(224)-diffUp(217)];%WinRatio: 0.58, Sharpe: 0.214, Return: 3.9%, MaxDraw: 0.8%
                results=[results,diffUp(196)-diffUp(203)];%WinRatio: 0.58, Sharpe: 0.196, Return: 2.5%, MaxDraw: 0.4%
                results=[results,diffUp(164)-diffUp(173)];%WinRatio: 0.63, Sharpe: 0.208, Return: 2.6%, MaxDraw: 0.4%
                results=[results,diffUp(118)-diffUp(129)];%WinRatio: 0.66, Sharpe: 0.326, Return: 3.9%, MaxDraw: 0.5%
                results=[results,diffUp(118)-diffUp(93)];%WinRatio: 0.61, Sharpe: 0.246, Return: 6.5%, MaxDraw: 0.5%
                results=[results,diffUp(13)-diffUp(17)];%WinRatio: 0.62, Sharpe: 0.283, Return: 4.1%, MaxDraw: 0.4%
            case 5
                Matrix5=[Matrix5;diffUp'];    
                results=[results,diffUp(202)-diffUp(213)];%WinRatio: 0.60, Sharpe: 0.169, Return: 2.1%, MaxDraw: 0.8%
                results=[results,diffUp(153)-diffUp(165)];%WinRatio: 0.60, Sharpe: 0.229, Return: 2.5%, MaxDraw: 0.6%
                results=[results,diffUp(135)-diffUp(143)];%WinRatio: 0.60, Sharpe: 0.235, Return: 4.8%, MaxDraw: 0.5%
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
    pf=120+j;
    subplot(pf);
    plot(results);
    hold on;
    plot(indx,results(indx),'r*');
    grid on;
    fprintf('WinRatio: %.2f, Sharpe: %.3f, Return: %.1f%%, MaxDraw: %.1f%%\n',winratio,sharpe,results(end)*100,maxdraw*100);
    % display([winratio,sharpe,results(end),maxdraw]);
    hold off;  
    
    length(Time)/226
%     if j==1
%         figure;
%         plot(mean(Matrix1));
%         set(gca,'xtick',1:5:226);
%         grid on;
%         figure;
%         plot(mean(Matrix2));
%         set(gca,'xtick',1:5:226);
%         grid on;
%         figure;
%         plot(mean(Matrix3));
%         set(gca,'xtick',1:5:226);
%         grid on;
%         figure;
%         plot(mean(Matrix4));
%         set(gca,'xtick',1:5:226);
%         grid on;
%         figure;
%         plot(mean(Matrix5));
%         set(gca,'xtick',1:5:226);
%         grid on;  
%         figure;      
%     end         
end


% [~,f1,~]=anova1(Matrix1)
% [~,f2,~]=anova1(Matrix2)
% [~,f3,~]=anova1(Matrix3)
% [~,f4,~]=anova1(Matrix4)
% [~,f5,~]=anova1(Matrix5)
end


