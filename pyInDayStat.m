function Fre=pyInDayStat(varargin) % the last/middle parameter:5 for 5 minutes;10 for 10 minutes;60 for one hour;
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
period=['BarSize=',num2str(typex)];
startT=[datestr(today-800,'yyyy-mm-dd'),' 09:00:00'];
endT=[datestr(today-1,'yyyy-mm-dd'),' 15:01:00'];
[data,~,~,time]=w.wsi(stock,'open,close',startT,endT,period,'periodstart=09:00:01;periodend=15:01:00;PriceAdj=F');
close=data(:,2);
indTem=~isnan(close);
time=time(indTem);
open=data(indTem,1);
close=close(indTem);
Date=floor(time);
colN=sum(Date==Date(1));

if nargin==2
    diff=close(1:end)./open(1:end)-1;
    rowN=length(diff)/colN;
    Matrix=reshape(diff,[colN,rowN])';
    Aa=mean(Matrix);
    MatrixS=zeros(size(Matrix));
    MatrixS(Matrix>0)=1;
    aPlus=sum(MatrixS);
    MatrixS=zeros(size(Matrix));
    MatrixS(Matrix<0)=1;
    aMinus=sum(MatrixS);
    aa=aPlus./(aPlus+aMinus)-0.5;
%     ratio=max(Aa)/max(aa);
%     Aa=Aa/ratio;
    figure;
    title(stock);
    subplot(211);
    bar(aa);
    subplot(212);
    bar(Aa);
    [~,a2,~]=anova1(Matrix,[],'off');
    display(a2);
%     Fre=[aa',Aa'];
%     figure;
%     multcompare(stats);   
    
else
    [aa1,Aa1,F1]=subwsPy(close,xn);
    FreTem=zeros(31,3);
    FreTem(1:5,1)=aa1;
    FreTem(1:5,2)=Aa1;
    FreTem(1:2,3)=F1;
    Fre=[Fre,FreTem];
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
ratio=max(Aa)/max(aa);
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


