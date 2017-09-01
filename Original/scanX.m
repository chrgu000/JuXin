function varargout=scanX( varargin)   % put in date in varargin to decide which day as final day. 
global date high low close open vol atr;
numF=0; % record the numbers of selected stocks;

if nargin==0
    args='all';
    datend=0;
else
    if ischar(varargin{end})
        datend=varargin{end};
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
n=input('Plese put in times of selected models for one stock:');
backday=input('Plese put back-days:');
tic;
if isempty(n)
    n=1;
end
if isempty(backday)
    backday=0;
end
h=waitbar(0,'Wait for data in ...');

w=windmatlab;
w_wset_data=w.wset('SectorConstituent','Id=a001010100000000');
stocks=w_wset_data(:,2);
stocks=[stocks',{'000300.sh','510050.sh','000905.sh','000016.sh','512510.sh','IF00.CFE','IC00.CFE','IH00.CFE'}];
if nargin>0 && (varargin{end}=='w'||varargin{end}=='W')
    [Open,~,~,Date]=w.wsd(stocks,'open','ED-600TD',today,'Period=W','Fill=Previous','PriceAdj=F');
    Close=w.wsd(stocks,'close','ED-600TD',today,'Period=W','Fill=Previous','PriceAdj=F');
    High=w.wsd(stocks,'high','ED-600TD',today,'Period=W','Fill=Previous','PriceAdj=F');
    Low=w.wsd(stocks,'low','ED-600TD',today,'Period=W','Fill=Previous','PriceAdj=F');
    Vol=w.wsd(stocks,'volume','ED-600TD',today,'Period=W','Fill=Previous','PriceAdj=F');
else
    load scanXData;
    if isequal(Date(end),today)
        Open(end,:)=w.wsq(stocks,'rt_open')';
        Close(end,:)=w.wsq(stocks,'rt_latest')';
        High(end,:)=w.wsq(stocks,'rt_high')';
        Low(end,:)=w.wsq(stocks,'rt_low')';
        Vol(end,:)=w.wsq(stocks,'rt_vol')';  
    else
        [Open,~,~,Date]=w.wsd(stocks,'open','ED-120TD',today,'Fill=Previous','PriceAdj=F');
        Close=w.wsd(stocks,'close','ED-120TD',today,'Fill=Previous','PriceAdj=F');
        High=w.wsd(stocks,'high','ED-120TD',today,'Fill=Previous','PriceAdj=F');
        Low=w.wsd(stocks,'low','ED-120TD',today,'Fill=Previous','PriceAdj=F');
        Vol=w.wsd(stocks,'volume','ED-120TD',today,'Fill=Previous','PriceAdj=F');
        if isequal(High(end-1,:),High(end,:)) % run on non-trading time;
            Open=Open(1:end-1,:);
            Close=Close(1:end-1,:);
            High=High(1:end-1,:);
            Low=Low(1:end-1,:);
            Vol=Vol(1:end-1,:);
        end
        if all(isnan(High(end,:))) % run on trading time;
            Open(end,:)=w.wsq(stocks,'rt_open')';
            Close(end,:)=w.wsq(stocks,'rt_latest')';
            High(end,:)=w.wsq(stocks,'rt_high')';
            Low(end,:)=w.wsq(stocks,'rt_low')';
            Vol(end,:)=w.wsq(stocks,'rt_vol')';    
        end
        save scanXData Date Open Close High Low Vol stocks
    end
end

if strcmp(args,'all') || any(args==5)
    load up4plusdown1Data 
    stocksM5={};
    closeM5=[]; % save selected stocks' close price;
end
% stocks=stocks(1:6);
ind_stocks=ones(size(stocks));
for i=1:length(stocks)
% for i=1902:1902
    vol=Vol(:,i);
    if vol(end-backday)<1
        continue;
    end
    open=Open(:,i);
    tem=sum(isnan([open,vol]),2)<1;
    open=open(tem);
    L=length(open);
    if L<30
        ind_stocks(i)=0;
        continue;
    end
    close=Close(:,i);
    high=High(:,i);
    low=Low(:,i);
    close=close(tem);
    high=high(tem);
    low=low(tem);
    vol=vol(tem);
    date=Date(tem);   
    if isequal([open(end),close(end),high(end),low(end),vol(end)],[open(end-1),close(end-1),high(end-1),close(end-1),vol(end-1)])
        ind_stocks(i)=0;
        continue;
    end
    
    if ~isnumeric(datend)&&datend~='w'&&datend~='W'
        L=strmatch(datenum(datend),date);
        open=open(1:L);
        close=close(1:L);
        high=high(1:L);
        low=low(1:L);
        vol=vol(1:L);
        date=date(1:L);
    end
    if backday~=0
        L=L-backday;
        open=open(1:L);
        close=close(1:L);
        high=high(1:L);
        low=low(1:L);
        vol=vol(1:L);
        date=date(1:L);        
    end   

    if L>0
        atr=ATR(L);
    end
    
    clear X2 Y2 X3 Y3 X4 Y4 Ord Udlen Ratio;
    X1=0;
    X2(2,10)=0;
    Y2(2,10)=0;
    X3(3,10)=0;
    Y3(3,10)=0;
    X4(4,10)=0;
    Y4(4,10)=0;
    Ord(10,3)=0;
    Udlen(15,3)=0;
    Ratio(10,3)=0;
%if L>80 % & datenum(date{L})==LTD
%% Model_DownUpDown3 : nDowns-nUps-nDowns
if any(args==0)
    [x1,x2]=Model_Test;
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
%% Model_UpDown : Up and Down bars are the same; Model Number:22
if strcmp(args,'all') || any(args==22)
    [x1,x3,y3,ord,ratio]=Model_UpDown_Half2;
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
        
        rowA=sum(sum(ratio')~=0);
        rowO=sum(sum(Ratio')~=0);
        Ratio(rowO+1:rowO+rowA,:)=ratio(1:rowA,:);
        
    end
end
%% Model_UpDown : Up and Down bars are the same; Model Number:2
if strcmp(args,'all') || any(args==2)
    [x1,x3,y3,ord,ratio]=Model_UpDown;
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
        
        rowA=sum(sum(ratio')~=0);
        rowO=sum(sum(Ratio')~=0);
        Ratio(rowO+1:rowO+rowA,:)=ratio(1:rowA,:);
        
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
if 0 %strcmp(args,'all') || any(args==4)
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
%% Model_up4plusdown1: serial more than 4 days and 1 big down; Model number:5
if strcmp(args,'all') || any(args==5)
    if find(strcmp(stocksGroup5,stocks(i)))
        L5=length(open);
        downNow=max(high(L5-4:L5-1))-low(L5);
        downs=[max(high(L5-4:L5-2))-low(L5-1),max(high(L5-4:L5-3))-low(L5-2),max(high(L5-5:L5-4))-low(L5-3),high(L5-5)-low(L5-4)];
        if close(L5-1)>open(L5-1) && close(L5-2)>open(L5-2) && close(L5-3)>open(L5-3) && close(L5-4)>open(L5-4) &&...% continuous ups(close>open)
                downNow>1*max(downs)&&low(L5)>min(low(L5-4:L5-1))&&...%big down happens;
                close(L5)<low(L5)+0.25*(high(L5)-low(L5)) %&& low(L5)<low(L5-1) %&& vol(L5)/vol(L5-1)<=0.65 && low(L5)<low(L5-1) %&&high(L5-1)>=high(L5)
            stocksM5=[stocksM5,stocks(i)];
            closeM5=[closeM5,close(L5)];
            X1=X1+1;
        end
    end
end
%% Model_PointSymmetry: one point,left and right symmetry; Model number:6
if strcmp(args,'all') || any(args==6)
    L6=length(open);
    for ii=3:10
        centerB=L6-ii;
        rightHB=highest(centerB,L6);
        leftHB=highest(centerB-ii,centerB);
        [~,leftHInd]=sort(high(leftHB:centerB));
        [~,rightHInd]=sort(high(centerB:rightHB));
        [~,leftLInd]=sort(low(leftHB:centerB));
        [~,rightLInd]=sort(low(centerB:rightHB));
        if L6>30
        if low(centerB)==min(low(centerB-ii:L6))&& rightHB+leftHB==centerB*2 && ...
                low(centerB-ii)==min(low(centerB-3*ii:leftHB)) && low(L6)==min(low( rightHB:L6 ))&&rightHB~=L6 &&...
                max(high(leftHB:rightHB)-low(leftHB:rightHB))>1.2*max([high(centerB-ii:leftHB-1)-low(centerB-ii:leftHB-1);high(rightHB+1:L6)-low(rightHB+1:L6)])&&...
                ( all(leftHInd'==centerB-leftHB+1:-1:1) || all(leftLInd'==centerB-leftHB+1:-1:1) )&&...
                ( all(rightHInd'==1:rightHB-centerB+1)  || all(rightLInd'==1:rightHB-centerB+1) )
            X1=X1+1;
            if X3==0
                X3(:,1)=[L6-2*ii;L6-ii;L6];
                Y3(:,1)=[low(L6-2*ii);low(L6-ii);low(L6)];
            else
                rowA=sum(sum(X3)~=0)+1;
                X3(:,rowA)=[L6-2*ii;L6-ii;L6];
                Y3(:,rowA)=[low(L6-2*ii);low(L6-ii);low(L6)];
            end
            break;
        end
        end
    end
end
%% Model_Gap2: two gaps make isolate bars; Model number:6
if 1%strcmp(args,'all') || any(args==6)
    [x1,x2]=Model_Gap2;
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
%% Drawing Figures;
if X1>=n
    numF=numF+1;
    if 1 % 0 means no figures and 1 means figures;
        srsz=get(0,'ScreenSize');
        figure('Position',[srsz(3)/8,srsz(4)/8,srsz(3)*3/4,srsz(4)*3/4]);
        subplot(3,1,[1,2]);
        candle(high,low,close,open);
        title(stocks(i));
        grid on;
        try
            Boll(close);
        end
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
        rowO=sum(sum(Ratio')~=0);
        Ratio=Ratio(1:rowO,:);
        if rowO>1
            Ratio=sortrows(Ratio,2);
            for i=2:rowO
                Ratio(i,2)=Ratio(i,2)*(1.02^i);
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
        text(Ratio(:,1),Ratio(:,2),num2str(Ratio(:,3)),'FontSize',8,'Color','k'); 
        text(Udlen(:,1),Udlen(:,2),num2str(Udlen(:,3)),'FontSize',8,'Color','r'); 
        subplot(3,1,3);
        MACD(close);
        grid on;
    end
end
tem=i/length(stocks);
waitbar(tem,h,['Scaning: Completed...',num2str(roundn(100*tem,-2)),'%']);
end
waitbar(1,h,'Completed...100%');
pause(1);
delete(h);
IgnoredNum=sum(ind_stocks==0);
if IgnoredNum>0
    display([num2str(IgnoredNum),' stocks are ignored!']);
end
display(numF);

if strcmp(args,'all') || any(args==5)
    display('stocks which fit model 5:-------------');
    display('Remember: if next open price is lower than current close price, long another this stock!');
    if nargin>0 && (varargin{end}=='w'||varargin{end}=='W')
        display(stocksM5');
    else
        LTem=length(stocksM5);
        stocksTem={};
        valuesTem=[];
        for i=1:LTem
            indTem=find(strcmp(stocksGroup5,stocksM5(i)),1);
            valuesTem=[valuesTem;resultsGroup5(indTem)];
            stocksTem=[stocksTem;strcat(stocksM5(i),':',mat2str(roundn(resultsGroup5(indTem,:),-3)),...
                ',Buy:',mat2str(round(500/LTem/closeM5(i))*100))];
        end
        [~,ind]=sort(valuesTem);
        if nargout==1
            varargout{1}=stocksTem(ind);
            display('selected stocks are save on varargout 1st!');
        else
            display(stocksTem(ind));
        end
        %     for i=1:LTem
        %         indTem=find(strcmp(stocksGroup5,stocksM5(i)),1);
        %         display(strcat(stocksM5(i),':',mat2str(roundn(resultsGroup5(indTem,:),-3))));
        %     end
    end
    display('--------------------------------------');
    
toc;
end





% don't show figure;
% figure('Visile','off');
% plot(rand(1,100));
% saveas(gcf,'myfigure.fig','fig')