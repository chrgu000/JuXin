function scan( varargin)   % put in date in varargin to decide which day as final day.
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

% trace the gas between the target stock and other for a little long time
% when you want to buy it. buy it only when the gas' change shows the
% target becomes up strong from week.

% syms b c x1 x2 y1 y2
% ex1 = b*x1+c-y1;
% ex2 = b*x2+c-y2;
% [b,c] = solve(ex1,ex2,'b,c');
% % 求出直线方程
% A = [1 2];
% B = [5 6];
% x1 = A(1); x2 = B(1);
% y1 = A(2); y2 = B(2);
% b = subs(b)
% c = subs(c)
% % 作图验证
% syms x y
% ezplot(b*x+c-y);
% hold on
% plot(x1,y1,'ro');
% plot(x2,y2,'ro');
% grid on
% hold off

global date high low close open vol atr;
numF=0; % record the numbers of selected stocks;

if nargin==0
    args='all';
    datend=0;
else
    if ischar(varargin{end})
        datend=varargin(1);
        if nargin==1
            args='all';
        else
            args=cell2mat(varargin(1:end-1));
        end
    else
        datend=0;
        args=cell2mat(varargin);
    end
end

% args=cell2mat(varargin(1:end-1))
% if nargin~=0 && min(args)>3
%     warndlg('There is not required models!');
%     return;
% end


% LatestTD=input('Plese put in the latest trading date(''11/06/2015''):');
% LTD=datenum(LatestTD);
% LTD=datenum(date);

n=input('Plese put in times of selected models for one stock:'); 
backday=input('Plese put back days:');

load IDNames.mat;
for i=1:length(IDNames)/10
    name_f=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\AllStocks\',IDNames{i},'.txt');
    fid=fopen(name_f);
    Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
    fclose(fid);
    if isnumeric(datend)
        L=length(Data{1})-1;
    else
        L=strmatch(datend,Data{1});
    end
    
    
    L=L-backday;
    date=Data{1}(1:L);
    open=Data{2}(1:L);
    high=Data{3}(1:L);
    low=Data{4}(1:L);
    close=Data{5}(1:L);
    vol=Data{6}(1:L);
    if L>0
        atr=ATR(L);
    end
    
    clear X2 Y2 X3 Y3 X4 Y4 Ord Udlen;
    X1=0;
    X2(2,10)=0;
    Y2(2,10)=0;
    X3(3,10)=0;
    Y3(3,10)=0;
    X4(4,10)=0;
    Y4(4,10)=0;
    Ord(10,3)=0;
    Udlen(15,3)=0;
if L>80 % & datenum(date{L})==LTD
%% Model_UpLine: Up-Line-BreakOut; Model  Number:1
if 0 %strcmp(args,'all') || any(args==1)
    [x1,x2,x3,ord]=Model_UpLine(high,low,close,vol);
    if x1>0
        X1=X1+x1;
        if X2==0
            X2(:,1)=x2(1,:)';
            Y2(:,1)=x2(2,:)';
        else
            rowA=sum(sum(X2)~=0)+1;
            X2(:,rowA)=x2(1,:)';
            Y2(:,rowA)=x2(2,:)';
        end
        if X3==0
            X3(:,1)=x3(1,:)';
            Y3(:,1)=x3(2,:)';
        else
            rowA=sum(sum(X3)~=0)+1;
            X3(:,rowA)=x3(1,:)';
            Y3(:,rowA)=x3(2,:)';
        end
        Ord(1:2,:)=ord;
    end
end
%% Model_UpDown : Up and Down bars are the same; Model Number:2
if 0 %strcmp(args,'all') || any(args==2)
    [x1,x3,y3,ord]=Model_UpDown_S(L);
    if x1>0
        X1=X1+x1;
        [~,colA]=size(x3);
        if X3==0
            X3(:,1:colA)=x3;
            Y3(:,1:colA)=y3;
        else
            rowA=sum(sum(X3)~=0)+1;
            X3(:,rowA:rowA+colA-1)=x3;
            Y3(:,rowA:rowA+colA-1)=y3;
        end
        
        rowA=sum(sum(ord')~=0);
        rowO=sum(sum(Ord')~=0);
        Ord(rowO+1:rowO+rowA,:)=ord(1:rowA,:);
        
    end
end
%% Model_DownUpDown : Two Downs'bars are the same and are different from Up's bars; Model Number:3
if strcmp(args,'all') || any(args==3)
    [x1,x4,y4,ord,udlen]=Model_DownUpDown;
    if x1>0
        X1=X1+x1;
        [~,colA]=size(x4);
        if X4==0
            X4(:,1:colA)=x4;
            Y4(:,1:colA)=y4;
        else
            rowA=sum(sum(X4)~=0)+1;
            X4(:,rowA:rowA+colA-1)=x4;
            Y4(:,rowA:rowA+colA-1)=y4;
        end
                    
            rowA=sum(sum(ord')~=0);
            rowO=sum(sum(Ord')~=0);
            Ord(rowO+1:rowO+rowA,:)=ord(1:rowA,:);
            rowA=sum(sum(udlen')~=0);
            rowO=sum(sum(Udlen')~=0);
            Udlen(rowO+1:rowO+rowA,:)=udlen(1:rowA,:);
            
    end
end
%% Model_12: 12 bars' cycle; Model number:4
if strcmp(args,'all') || any(args==4)
    [x1,x2]=Model_12;
    if x1>0
        X1=X1+x1;
        if X2==0
            X2(:,1)=x2(:,1);
            Y2(:,1)=x2(:,2);
        else
            rowA=sum(sum(X2)~=0)+1;
            X2(:,rowA)=x2(:,1);
            Y2(:,rowA)=x2(:,2);
        end
    end
end
end
    if X1>=n
        numF=numF+1;
        if 1 % 0 means no figures and 1 means figures;
            srsz=get(0,'ScreenSize');
            figure('Position',[srsz(3)/8,srsz(4)/8,srsz(3)*3/4,srsz(4)*3/4]);
            subplot(3,1,[1,2]);
            candle(high,low,close,open);
            title(IDNames{i});
            grid on;
            Boll(close);
            if X2(1,1)~=0
                line(X2,Y2,'Color','r','LineWidth',2);
            end
            if X3(1,1)~=0
                line(X3,Y3,'Color','b','LineWidth',2);
            end
            if X4(1,1)~=0
                line(X4,Y4,'Color','k','LineWidth',2);
            end
            rowO=sum(sum(Ord')~=0);
            Ord=Ord(1:rowO,:);
            if rowO>2
                Ord=sortrows(Ord,2);
                for i=3:rowO
                    indexn=ceil(i/2);
                    Ord(i,2)=Ord(i,2)*(1.02^indexn);
                end
            end

            rowO=sum(sum(Udlen')~=0);
            Udlen=Udlen(1:rowO,:);
            if rowO>3
                Udlen=sortrows(Udlen,2);
                for i=3:rowO
                    indexn=ceil(i/2);
                    Udlen(i,2)=Udlen(i,2)*(0.96^indexn);
                end
            end
            text(Ord(:,1),Ord(:,2),num2str(Ord(:,3)),'FontSize',8,'Color','k'); 
            text(Udlen(:,1),Udlen(:,2),num2str(Udlen(:,3)),'FontSize',8,'Color','r'); 
            subplot(3,1,3);
            MACD(close);
            grid on;
        end
    end
end
display(numF);
end

% get history data from yahoo;
% c=yahoo;
% D=fetch(c,'000001.ss',{'open' 'high' },'12/21/2000',datestr(floor(now))); % D=fetch(c,'000001.ss','12/21/2000',datestr(floor(now)));


% function MakeFigure(IDName)
% global open high low close fig;
% srsz=get(0,'ScreenSize');
% figure('Position',[srsz(3)/8,srsz(4)/8,srsz(3)*3/4,srsz(4)*3/4]);
% subplot(3,1,[1,2]);
% % Kplot(open,high,low,close);
% candle(high,low,close,open);
% % tsobj=fints(date,[open,high,low,close],{'open','high','low','close'});
% % candle(tsobj);        
% title(IDName);
% grid on;
% hold on;
% fig=1;
% end