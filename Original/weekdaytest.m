function weekdaytest(varargin)
global name_p DIY;
DIY=0;
if nargin==0
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
global name_p DIY;
if DIY==1
    file=strcat(name_p,namefile{:},'.txt');
    fid=fopen(file);
else
    fid=fopen(strcat(name_p,namefile.name));
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

wn=weekday(date)-1;

% diff=(close-open)./close;
diff=(close(2:end)-close(1:end-1))./close(2:end);
diff=[0;diff];

% xlswrite('C:\Users\caofa\Desktop\output.xls',[wn,diff])

A=accumarray(wn,diff);
a=accumarray(wn,1);
Aa=A./a;
Diff=diff;
Diff(Diff>100*eps)=1;
Diff(Diff<-100*eps)=0;
aa=accumarray(wn,Diff);
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
end
