function HedgeZnM  %Îå¿óÒ»À¿×Ó½»Ò× test6 ²âÊÔÃÜÂë£ºqwe123!@#
try 
    load HedgeZnM;
catch
    w=windmatlab;
    [Xminutes,~,~,Time]=w.wsi('zn.shf','close','20150426 09:00:00','20170426 15:01:00',...
        'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
    indTem=~isnan(Xminutes);
    Xminutes=Xminutes(indTem);
    Time=Time(indTem);
    TimeR=floor(Time);
    step=sum(TimeR(1)==TimeR);
    save HedgeZnM Xminutes Time step;
end

% w=windmatlab;
% todayStr=datestr(today-1,'yyyymmdd');
% [Xminutes,~,~,Time]=w.wsi('zn.shf','close','20170427 09:00:00',[todayStr,' 15:01:00'],...
%         'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
% indTem=~isnan(Xminutes);
% Xminutes=Xminutes(indTem);
% Time=Time(indTem);
% TimeR=floor(Time);
% step=sum(TimeR(1)==TimeR);

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
            results=[results,diffUp(173)-diffUp(188)];%WinRatio: 0.66, Sharpe: 0.388, Return: 8.6%, MaxDraw: 0.9%
            results=[results,diffUp(71)-diffUp(48)];%WinRatio: 0.61, Sharpe: 0.241, Return: 6.7%, MaxDraw: 1.0%
            results=[results,diffUp(28)-diffUp(37)];%WinRatio: 0.60, Sharpe: 0.201, Return: 5.7%, MaxDraw: 1.1%
        case 2
            Matrix2=[Matrix2;diffUp'];
            results=[results,diffUp(10)-diffUp(61)];%WinRatio: 0.63, Sharpe: 0.311, Return: 14.0%, MaxDraw: 1.3%
        case 3
            Matrix3=[Matrix3;diffUp'];
            results=[results,diffUp(220)-diffUp(159)];%WinRatio: 0.66, Sharpe: 0.227, Return: 9.8%, MaxDraw: 1.6%
            results=[results,diffUp(100)-diffUp(125)];%WinRatio: 0.62, Sharpe: 0.222, Return: 7.4%, MaxDraw: 1.3%
            results=[results,diffUp(40)-diffUp(85)];%WinRatio: 0.65, Sharpe: 0.317, Return: 11.5%, MaxDraw: 1.8%
        case 4
            Matrix4=[Matrix4;diffUp'];
            results=[results,diffUp(184)-diffUp(195)];%WinRatio: 0.58, Sharpe: 0.250, Return: 5.0%, MaxDraw: 0.8%
            results=[results,diffUp(136)-diffUp(127)];%WinRatio: 0.64, Sharpe: 0.367, Return: 8.5%, MaxDraw: 0.6%
            results=[results,diffUp(73)-diffUp(80)];%WinRatio: 0.66, Sharpe: 0.374, Return: 5.5%, MaxDraw: 0.4%
            results=[results,diffUp(71)-diffUp(53)];%WinRatio: 0.57, Sharpe: 0.238, Return: 6.2%, MaxDraw: 1.4%
        case 5
            Matrix5=[Matrix5;diffUp'];
            results=[results,diffUp(225)-diffUp(211)];%WinRatio: 0.66, Sharpe: 0.308, Return: 7.1%, MaxDraw: 0.6%
            results=[results,diffUp(196)-diffUp(201)];%WinRatio: 0.54, Sharpe: 0.301, Return: 4.6%, MaxDraw: 0.5%
            results=[results,diffUp(185)-diffUp(174)];%WinRatio: 0.64, Sharpe: 0.286, Return: 5.7%, MaxDraw: 0.7%
            results=[results,diffUp(129)-diffUp(86)];%WinRatio: 0.64, Sharpe: 0.289, Return: 8.0%, MaxDraw: 1.2%
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


