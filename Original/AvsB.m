function co=AvsB(varargin)
if nargin>3 || nargin <2
    warndlg('Parameters put in AvsB is not correct!');
    return;
end
A=varargin{1};
B=varargin{2};
if nargin==3
    pict=1;
else
    pict=0;
end

if size(A)~=size(B)
    warndlg('Please put in two stocks'' numbers at least!');
end
if varargin{end}=='c'
    path='E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest\';
else
    path='E:\360Synchronization\360Synchronization\MatLab\DataFromZX\AllStocks\';
end
if length(A{1})==8
    fileA=strcat(path,A{1},'.txt');
else
    fileA=strcat(path,A{1});
end
if length(B{1})==8
    fileB=strcat(path,B{1},'.txt');
else
    fileB=strcat(path,B{1});
end
fidA=fopen(fileA);
DataA=textscan(fidA,'%s %f %f %f %f %d %d','headerlines',2);
fclose(fidA);
dateA=DataA{1}(1:end-1);
% openA=DataA{2}(1:end-1);
closeA=DataA{5}(1:end-1);  

fidB=fopen(fileB);
DataB=textscan(fidB,'%s %f %f %f %f %d %d','headerlines',2);
fclose(fidB);
dateB=DataB{1}(1:end-1);
% openB=DataB{2}(1:end-1);
closeB=DataB{5}(1:end-1);  
[~,ia,ib]=intersect(dateA,dateB);
closeA=closeA(ia);
closeB=closeB(ib);
co=corr(closeA,closeB);
if pict==1
    dot=1:length(closeA);
    figure;
    plotyy(dot,closeA,dot,closeB);
    legend(A{1},B{1});
    hold off;
end
end

