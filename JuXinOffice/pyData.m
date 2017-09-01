function varargout=pyData(stocks,indicators,timeStart,timeEnd,index)

if nargin==2
    timeStart='2016-01-01';
    timeEnd=datestr(today,'yyyy-mm-dd');
    index=0;
elseif nargin==3
    timeEnd=datestr(today,'yyyy-mm-dd');
    index=0;
elseif nargin==4
    index=0;
else
    display('Number of parameters must be 2,3,or4');
    display('Program has stopped!');
    return;
end
save('D:\pyData.mat','stocks','indicators','timeStart','timeEnd','index')
pythonFile='python D:\Trading\Python\pyData.py';
system(pythonFile);
indicators=regexp(indicators,',','split');
Lind=length(indicators);
j=1;
for i=1:Lind
    if strfind(['open','high','low','close','volume'],indicators(i))>0
        dataTem=xlsread('D:\pyData.xlsx',indicators{i});
        varargout{j}=dataTem(:,2:end);
        j=j+1;
    end
end
delete('D:\pyData.xlsx');
end







