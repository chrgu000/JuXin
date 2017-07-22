function prepareData( varargin) 

global date high low close open vol;

% load IDNames_copy.mat;
load IDNames.mat;
X=zeros(length(IDNames),6);
if nargin==0;
    backday=0;
else
    backday=varargin{1};
end
for i=1:length(IDNames)
    name_f=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\AllStocks\',IDNames{i},'.txt');
    fid=fopen(name_f);
    Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
    fclose(fid);
    L=length(Data{1})-1;
    if L<50
        continue;
    end
    if IDNames{i}(3)=='X'
%     if IDNames{i}(3)=='6'
%     if IDNames{i}(3)~='3'
%     if IDNames{i}(3)~='0'
%     if IDNames{i}(3)~='6'
        continue;
    end
    L=L-backday;
    high=Data{3}(1:L);
    low=Data{4}(1:L);
    close=Data{5}(1:L);
    vol=Data{6}(1:L);
    if close(L)<2
        continue;
    end
    highPoint=highest(L-12,L);
    lowPoint=lowest(L-12,L);
    X(i,1)=(close(L)-close(L-1))/close(L-1);
    X(i,2)=double(vol(L)-vol(L-1))/double(vol(L-1));
    everPrice=mean(close(L-11:L));
    X(i,3)=(close(L)-everPrice)/everPrice;
    everVol=double(mean(vol(L-11:L)));
    X(i,4)=double(vol(L)-everVol)/everVol;
    X(i,5)=(L-highPoint)/12;
    X(i,6)=(L-lowPoint)/12;
end
load all_theta
[value,pred]= predictOneVsAll(all_theta, X(~all(X==0,2),:));
tem=IDNames(pred==2&value>0.65);
display(tem)
end




