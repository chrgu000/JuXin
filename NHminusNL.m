function NHminusNL
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

load IDNames.mat;
L=length(IDNames);

data=arrayfun(@(x) getdata(x),IDNames,'UniformOutput',false); % get 'date','high' and 'low' of all stocks and save them in data;
dateX=data{1}(:,1); % get date of 'sh000001';
beginInd=find(dateX>=datenum('2005/1/1'),1);
endInd=length(dateX);
NH_L(endInd-beginInd+1)=0;
NH_LPer(endInd-beginInd+1)=0;

for i=beginInd:endInd
    DateI=dateX(i); % select one certain day;
    NH=0;
    NL=0;
    NM=0;
    for j=2:L
        if length(data{j})>200 && ismember(DateI,data{j}(:,1))
            dateJ=data{j}(:,1);
            highJ=data{j}(:,2);
            lowJ=data{j}(:,3);
            DateJ=DateI-360; % confirm the day before certain day one year ago;
            ind=find(dateJ>=DateJ & dateJ<=DateI);
            if dateJ(1)<DateJ
                NM=NM+1;
                if abs( highJ(ind(end))-max(highJ(ind)) )<eps
                    NH=NH+1;
                elseif abs( lowJ(ind(end))-min(lowJ(ind)) )<eps 
                    NL=NL+1;
                end
            end
        end
    end 
    NH_L(i-beginInd+1)=NH-NL; 
    NH_LPer(i-beginInd+1)=(NH-NL)/NM;
end
figure;
plotyy(1:endInd-beginInd+1,NH_L,1:endInd-beginInd+1,NH_LPer);

end


function data=getdata(stock)
file=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest\',stock{:},'.txt');
fid=fopen(file);
Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
fclose(fid);
date=Data{1}(1:end-1);
% Open=Data{2}(1:end-1);
high=Data{3}(1:end-1);
low=Data{4}(1:end-1);
% Close=Data{5}(1:end-1);
% Vol=Data{6}(1:end-1);
data=[datenum(date),high,low];
end


% 
% 
% 
% function NHminusNL0
% %UNTITLED Summary of this function goes here
% %   Detailed explanation goes here
% 
% global data dateX L;
% load IDNames.mat;
% L=length(IDNames);
% 
% data=arrayfun(@(x) getdata(x),IDNames,'UniformOutput',false); % get 'date','high' and 'low' of all stocks and save them in data;
% dateX=data{1}(:,1); % get date of 'sh000001';
% beginInd=find(dateX>=datenum('2005/1/1'),1);
% endInd=length(dateX);
% 
% NH_L=arrayfun(@(x) serialNHL(x),dateX(beginInd:endInd));
% 
% figure;
% plot(NH_L);
% end
% 
% function NHL=serialNHL(Dateind)
% global DateI L;
% DateI=Dateind; % select one certain day;
% temp=arrayfun(@(x) eachdayNHL(x),2:L);
% NHL=sum(temp); 
% end
% 
% 
% function UD=eachdayNHL(Dataind)
% global data DateI;
% UD=0;
% if length(data{Dataind})>200 && ismember(DateI,data{Dataind}(:,1))
%     dateJ=data{Dataind}(:,1);
%     highJ=data{Dataind}(:,2);
%     lowJ=data{Dataind}(:,3);
%     DateJ=DateI-360; % confirm the day before certain day one year ago;
%     ind=find(dateJ>=DateJ & dateJ<=DateI);
%     if abs( highJ(ind(end))-max(highJ(ind)) )<eps && dateJ(1)<DateJ
%         UD=1;
%     elseif abs( lowJ(ind(end))-min(lowJ(ind)) )<eps && dateJ(1)<DateJ
%         UD=-1;
%     end
% end
% end
% 
% 
% 
% function rawdata=getdata(stock)
% 
% file=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest\',stock{:},'.txt');
% fid=fopen(file);
% rawData=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
% fclose(fid);
% date=rawData{1}(1:end-1);
% % Open=rawData{2}(1:end-1);
% high=rawData{3}(1:end-1);
% low=rawData{4}(1:end-1);
% % Close=rawData{5}(1:end-1);
% % Vol=rawData{6}(1:end-1);
% rawdata=[datenum(date),high,low];
% end



