function HedgeRuM 
% try 
%     load HedgeRuM;
% catch
%     w=windmatlab;
%     [Xminutes,~,~,Time]=w.wsi('ru.shf','close','20140516 09:00:00','20170426 15:01:00',...
%         'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
%     indTem=~isnan(Xminutes);
%     Xminutes=Xminutes(indTem);
%     Time=Time(indTem);
%     TimeR=floor(Time);
%     step=sum(TimeR(1)==TimeR);
%     save HedgeRuM Xminutes Time step;
% end

w=windmatlab;
todayStr=datestr(today-1,'yyyymmdd');
[Xminutes,~,~,Time]=w.wsi('ru.shf','close','20170427 09:00:00',[todayStr,' 15:01:00'],...
        'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
indTem=~isnan(Xminutes);
Xminutes=Xminutes(indTem);
Time=Time(indTem);
TimeR=floor(Time);
step=sum(TimeR(1)==TimeR);

L=length(Time);
Matrix1=[];
Matrix2=[];
Matrix3=[];
Matrix4=[];
Matrix5=[];

results=[];
for i=step:step:L-step  
    diffUp=Xminutes(i+1:i+step)/Xminutes(i);
%     diffUp=diffUp/max(abs(diffUp));
    wd=weekday(Time(i+1))-1;   
    switch wd
        case 1            
            Matrix1=[Matrix1;diffUp'];
            results=[results,diffUp(159)-diffUp(171)];%WinRatio: 0.62, Sharpe: 0.234, Return: 8.2%, MaxDraw: 1.2%
            results=[results,diffUp(151)-diffUp(139)];%WinRatio: 0.59, Sharpe: 0.206, Return: 11.5%, MaxDraw: 1.7%
            results=[results,diffUp(116)-diffUp(109)];%WinRatio: 0.58, Sharpe: 0.215, Return: 6.6%, MaxDraw: 1.2%
            results=[results,diffUp(62)-diffUp(70)];%WinRatio: 0.59, Sharpe: 0.205, Return: 7.5%, MaxDraw: 1.1%
        case 2
            Matrix2=[Matrix2;diffUp'];
            results=[results,diffUp(91)-diffUp(126)];%WinRatio: 0.67, Sharpe: 0.256, Return: 17.0%, MaxDraw: 1.6%
            results=[results,diffUp(75)-diffUp(64)];%WinRatio: 0.67, Sharpe: 0.270, Return: 11.4%, MaxDraw: 1.3%
            results=[results,diffUp(23)-diffUp(61)];%WinRatio: 0.60, Sharpe: 0.263, Return: 27.7%, MaxDraw: 2.8%
        case 3
            Matrix3=[Matrix3;diffUp'];
            results=[results,diffUp(195)-diffUp(182)];%WinRatio: 0.62, Sharpe: 0.302, Return: 11.4%, MaxDraw: 1.1%
            results=[results,diffUp(101)-diffUp(112)];%WinRatio: 0.63, Sharpe: 0.278, Return: 14.0%, MaxDraw: 1.0%
            results=[results,diffUp(101)-diffUp(96)];%WinRatio: 0.60, Sharpe: 0.236, Return: 7.5%, MaxDraw: 0.7%
            results=[results,diffUp(48)-diffUp(63)];%WinRatio: 0.60, Sharpe: 0.237, Return: 12.3%, MaxDraw: 1.3%
            results=[results,diffUp(25)-diffUp(34)];%WinRatio: 0.57, Sharpe: 0.217, Return: 10.8%, MaxDraw: 1.3%
        case 4
            Matrix4=[Matrix4;diffUp'];
            results=[results,diffUp(72)-diffUp(80)];%WinRatio: 0.57, Sharpe: 0.235, Return: 10.3%, MaxDraw: 1.4%
            results=[results,diffUp(25)-diffUp(33)];%WinRatio: 0.61, Sharpe: 0.221, Return: 9.4%, MaxDraw: 1.4%
            results=[results,diffUp(15)-diffUp(10)];%WinRatio: 0.60, Sharpe: 0.256, Return: 11.0%, MaxDraw: 1.5%
        case 5
            Matrix5=[Matrix5;diffUp'];                    
            results=[results,diffUp(75)-diffUp(81)];%WinRatio: 0.67, Sharpe: 0.220, Return: 9.3%, MaxDraw: 2.0%
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
figure;
plot(results);
hold on;
plot(indx,results(indx),'r*');
grid on;
fprintf('WinRatio: %.2f, Sharpe: %.3f, Return: %.1f%%, MaxDraw: %.1f%%\n',winratio,sharpe,results(end)*100,maxdraw*100);
% display([winratio,sharpe,results(end),maxdraw]);
hold off;

% figure;
% plot(mean(Matrix1));
% set(gca,'xtick',1:5:226);
% grid on;
% figure;
% plot(mean(Matrix2));
% set(gca,'xtick',1:5:226);
% grid on;
% figure;
% plot(mean(Matrix3));
% set(gca,'xtick',1:5:226);
% grid on;
% figure;
% plot(mean(Matrix4));
% set(gca,'xtick',1:5:226);
% grid on;
% figure;
% plot(mean(Matrix5));
% set(gca,'xtick',1:5:226);
% grid on;

% [~,f1,~]=anova1(Matrix1)
% [~,f2,~]=anova1(Matrix2)
% [~,f3,~]=anova1(Matrix3)
% [~,f4,~]=anova1(Matrix4)
% [~,f5,~]=anova1(Matrix5)
end


