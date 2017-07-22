function Fre=pyWDM(varargin) % the last/middle parameter: 'wd' test days of all weeks; 'md' means test days of all months; 'm' means means test each month of all years;
                           % 'lmd' means test Lunar day of all months; 'lm' means test Lunar months for all years; 's' means test solar terms of all years.
                           
Fre=[];

if nargin==2 
    stock=varargin{1};          
    typex=varargin{2};
elseif nargin==3
    stock=varargin{1};          
    typex=varargin{2};
    resevePy=varargin{3}; % for subwayPy
else
    display('numbers of parameters are wrong!');
    return;
end

w=windmatlab;
[close,~,~,wtime]=w.wsd(stock,'close','2009-01-01',today-1,'Fill=Previous','PriceAdj=F');
indTem=isnan(close)<1&close>0.1;
% indTem=isnan(close)<1;
close=close(indTem);
date=wtime(indTem);
% date=mat2cell(datestr(wtime,'yyyy-mm-dd'),ones(length(wtime),1),10);

nn=regexp(typex,',','split');
if any(strcmp(nn,'wd'))
    xn=weekday(date)-1;
    if nargin==2
        subws(close,stock,xn,1);
    else
        [aa1,Aa1,F1]=subwsPy(close,xn);
        FreTem=zeros(31,3);
        FreTem(1:5,1)=aa1;
        FreTem(1:5,2)=Aa1;
        FreTem(1:2,3)=F1;
        Fre=[Fre,FreTem];
    end
    
end
if any(strcmp(nn,'md'))
    xn=str2num(datestr(date,'dd'));
    if nargin==2
        subws(close,stock,xn,2);
    else
        [aa2,Aa2,F2]=subwsPy(close,xn);
        FreTem=zeros(31,3);
        FreTem(1:31,1)=aa2;
        FreTem(1:31,2)=Aa2;
        FreTem(1:2,3)=F2;
        Fre=[Fre,FreTem];
    end
end
if any(strcmp(nn,'m'))
    xn=str2num(datestr(date,'mm'));
    if nargin==2
        subws(close,stock,xn,3);
    else
        [aa3,Aa3,F3]=subwsPy(close,xn);
        FreTem=zeros(31,3);
        FreTem(1:12,1)=aa3;
        FreTem(1:12,2)=Aa3;
        FreTem(1:2,3)=F3;
        Fre=[Fre,FreTem];
    end
end
if any(strcmp(nn,'lmd')) || any(strcmp(nn,'lm')) || any(strcmp(nn,'s'))
    [varM,varD,varS]=arrayfun(@(x) LunarCalendar(x),date);
    if any(strcmp(nn,'lmd'))
        xn=varD;
        if nargin==2
            subws(close,stock,xn,'lmd');
        else
            [aa4,Aa4,F4]=subwsPy(close,xn);
            FreTem=zeros(31,3);
            FreTem(1:30,1)=aa4;
            FreTem(1:30,2)=Aa4;
            FreTem(1:2,3)=F4;
            Fre=[Fre,FreTem];
        end
    end
    if any(strcmp(nn,'lm'))
        xn=varM;
        if nargin==2
            subws(close,stock,xn,'lm');
        else
            [aa5,Aa5,F5]=subwsPy(close,xn);
            FreTem=zeros(31,3);
            FreTem(1:12,1)=aa5;
            FreTem(1:12,2)=Aa5;
            FreTem(1:2,3)=F5;
            Fre=[Fre,FreTem];
        end
    end
    if any(strcmp(nn,'s'))
        xn=varS;
        if nargin==2
            subws(close,stock,xn,'s');
        else
            [aa6,Aa6,F6]=subwsPy(close,xn);
            FreTem=zeros(31,3);
            FreTem(1:25,1)=aa6;
            FreTem(1:25,2)=Aa6;
            FreTem(1:2,3)=F6;
            Fre=[Fre,FreTem];
        end
    end  
end 
end


function [aa,Aa,F]=subwsPy(close,xn)
diff=close(2:end)./close(1:end-1)-1;
diff=[0;diff];
A=accumarray(xn,diff);
a=accumarray(xn,1);
Aa=A./a;
Diff=diff;
Diff(Diff>100*eps)=1;
Diff(Diff<-100*eps)=0;
aa=accumarray(xn,Diff);
aa=aa./a-0.5;
ratio=max(abs(Aa))/max(abs(aa));
Aa=Aa/ratio;

% if nn==6
%     varD=0:1:25;
%     varN={' ','XiaoHan','DaHan','LiChun','YuShui','JingZhe','ChunFen','QingMing','GuYu','LiXia','XiaoMan','MangZhong','XiaZhi','XiaoShu','DaShu','LiQiu','ChuShu','BaiLu','QiuFen','HanLu','ShuangJiang','LiDong','XiaoXue','DaXue','DongZhi','Others'};
%     set(gca,'XTick',varD,'XLim',[0 25]);
%     set(gca,'XTickLabel',varN,'XTickLabelRotation',60,'FontName','Times New Roman','FontSize',16);
% end

minL=0;
for ind=unique(xn')
    eval(['x' num2str(ind) '=diff(xn==' num2str(ind) ');']);
    L=length(eval(['x' num2str(ind)]));
    if minL==0
        minL=L;
    else
        if minL>L;
            minL=L;
        end
    end
end
xdata=zeros(minL,ind);
for ind=unique(xn')
    xx=eval(['x' num2str(ind)]);
    xdata(:,ind)=xx(1:minL);
end
[~,f,~]=anova1(xdata,[],'off');
F=[f{2,5};f{2,6}];
end


function subws(close,stock,xn,nn)

diff=close(2:end)./close(1:end-1)-1;
diff=[0;diff];
A=accumarray(xn,diff);
a=accumarray(xn,1);
Aa=A./a;
Diff=diff;
Diff(Diff>100*eps)=1;
Diff(Diff<-100*eps)=0;
aa=accumarray(xn,Diff);
aa=aa./a-0.5;
ratio=max(abs(Aa))/max(abs(aa));
Aa=Aa/ratio;
% figure('Visible','off')
% plot(rand(1,100))
% saveas(gcf,'myfigure.fig','fig')   
figure;
bar([aa,Aa]);
title(stock);
if nn=='s'
    varD=0:1:25;
    varN={' ','XiaoHan','DaHan','LiChun','YuShui','JingZhe','ChunFen','QingMing','GuYu','LiXia','XiaoMan','MangZhong','XiaZhi','XiaoShu','DaShu','LiQiu','ChuShu','BaiLu','QiuFen','HanLu','ShuangJiang','LiDong','XiaoXue','DaXue','DongZhi','Others'};
    set(gca,'XTick',varD,'XLim',[0 25]);
    set(gca,'XTickLabel',varN,'XTickLabelRotation',60,'FontName','Times New Roman','FontSize',16);
end

minL=0;
for ind=unique(xn')
    eval(['x' num2str(ind) '=diff(xn==' num2str(ind) ');']);
    L=length(eval(['x' num2str(ind)]));
    if minL==0
        minL=L;
    else
        if minL>L;
            minL=L;
        end
    end
end
xdata=zeros(minL,ind);
for ind=unique(xn')
    xx=eval(['x' num2str(ind)]);
    xdata(:,ind)=xx(1:minL);
end
[~,~,stats]=anova1(xdata);
figure;
multcompare(stats);
end






