function WDMStat(varargin) % the last parameter: 1 test days of all weeks; 2 means test days of all months; 3 means means test each month of all years;
global name_p DIY typex;         % 4 means test Lunar day of all months; 5 means test Lunar months for all years; 6 means test solar terms of all years.
DIY=0;
if nargin==0
    typex=0;
else
    typex=varargin{end};
end
if isstr(typex)
    typex=123456;
end
if nargin==0 || length(varargin{1})~=8
    path=uigetdir;
    name_p=strcat(path,'\');
    name_f=dir(strcat(name_p,'*.txt'));
else 
    name_p='E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest\';
    name_f=varargin;
    DIY=1;
end
func=@(x) weekstati(x);
arrayfun(func,name_f);
end


function weekstati(namefile)
global name_p DIY typex;
if DIY==1
    file=strcat(name_p,namefile{:},'.txt');
    fid=fopen(file);
else
    fid=fopen(strcat(name_p,namefile.name));
end
if fid<=0
    warndlg('This file cant be found or opened!');
    return;
end
Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);
fclose(fid);
date=Data{1}(1:end-1);
open=Data{2}(1:end-1);
close=Data{5}(1:end-1);  

ind=find(close<1.5);
close(ind)=[];
open(ind)=[];
date(ind)=[];

n1=floor(typex/100000);
n2=floor(mod(typex,100000)/10000);
n3=floor(mod(typex,10000)/1000);
n4=floor(mod(typex,1000)/100);
n5=floor(mod(typex,100)/10);
n6=mod(typex,10);
nn=[n1 n2 n3 n4 n5 n6];
if any(nn==1)
    xn=weekday(date)-1;
    subws(close,DIY,namefile,xn,1);
end
if any(nn==2)
    xn=str2num(datestr(date,'dd'));
    subws(close,DIY,namefile,xn,2);
end
if any(nn==3)
    xn=str2num(datestr(date,'mm'));
    subws(close,DIY,namefile,xn,3);
end
if any(nn==4) || any(nn==5) || any(nn==6)
    [varM,varD,varS]=arrayfun(@(x) LunarCalendar(x),date);
    if any(nn==4)
        xn=varD;
        subws(close,DIY,namefile,xn,4);
    end
    if any(nn==5)
        xn=varM;
        subws(close,DIY,namefile,xn,5);
    end
    if any(nn==6)
        xn=varS;
        subws(close,DIY,namefile,xn,6);
    end        
end 
% if any(nn==5)
%     [xn,~]=arrayfun(@(x) LunarCalendar(x),date);
%     subws(close,DIY,namefile,xn);
% end
end

function subws(close,DIY,namefile,xn,nn)
% diff=(close-open)./close;
diff=(close(2:end)-close(1:end-1))./close(2:end);
diff=[0;diff];

% xlswrite('C:\Users\caofa\Desktop\output.xls',[wn,diff])
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
figure;
bar([aa,Aa]);
if DIY==1
    title(namefile{:});
else
    title(namefile.name);
end
if nn==6
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
xdata(minL-2,ind)=0;
for ind=unique(xn')
    xx=eval(['x' num2str(ind)]);
    xdata(:,ind)=xx(2:minL-1);
end
[~,~,stats]=anova1(xdata);
figure;
multcompare(stats);

end
