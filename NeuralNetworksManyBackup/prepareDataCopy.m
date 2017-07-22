function prepareDataCopy( varargin) 

global date high low close open vol;

% load IDNames_copy.mat;
load IDNames.mat;
delete('dataML.txt');
for i=1:length(IDNames)
    if IDNames{i}(3)=='X'
%     if IDNames{i}(3)=='6'
%     if IDNames{i}(3)~='3'
%     if IDNames{i}(3)~='0'
%     if IDNames{i}(3)~='6'
        continue;
    end
    try 
        name_f=strcat('D:\StockData\AllStocks\',IDNames{i},'.txt');
        %     name_f=strcat('D:\StockData\BackTest\',IDNames{i},'.txt');
        fid=fopen(name_f);
        Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
        fclose(fid);
    catch
        display(IDNames{i});
        continue;
    end
    L=length(Data{1})-1;
    if L<50
        continue;
    end
    date=Data{1}(1:L);
    open=Data{2}(1:L);
    high=Data{3}(1:L);
    low=Data{4}(1:L);
    close=Data{5}(1:L);
    vol=Data{6}(1:L);
    x=zeros(5000,6);
    y=zeros(5000,1);
    for j=15:L-5
        if close(j)<2
            continue;
        end
        highPoint=highest(j-12,j);
        lowPoint=lowest(j-12,j);
        x(j-14,1)=(close(j)-close(j-1))/close(j-1);
        x(j-14,2)=double(vol(j)-vol(j-1))/double(vol(j-1));
        everPrice=mean(close(j-11:j));
        x(j-14,3)=(close(j)-everPrice)/everPrice;
        everVol=double(mean(vol(j-11:j)));
        x(j-14,4)=double(vol(j)-everVol)/everVol;
        x(j-14,5)=(j-highPoint)/12;
        x(j-14,6)=(j-lowPoint)/12;
        if low(j)<low(lowest(j+1,j+4))&& datenum(date(j+4))-datenum(date(j))<=10&&low(lowest(j-2,j))<=low(lowest(j-12,j))
            upratio=( high(highest(j+1,j+4))-close(j) )/close(j);
            if upratio>0.25
                y(j-14)=1;
%                 figure;
%                 candle(high(1:j),low(1:j),close(1:j),open(1:j));
            end
        end                                      
    end

x0=x(y(1:L-19)==0,:);
x0=x0(~all(x0==0,2),:);
x1=x(y==1,:);

for i=2:L-19
    if i<=5
        if sum(y(1:i-1))>0&&y(i)==1
            y(i)=0;
        end
    else
        if y(i)==1&&sum(y(i-5:i-1))>0
            y(i)=0;
        end
    end
end

tem=8*sum(y);
temRand=randperm(size(x0,1));
x0=x0(temRand(1:tem),:);


x0=[x0,zeros(size(x0,1),1)];
x1=[x1,ones(size(x1,1),1)];
dlmwrite('dataML.txt', [x0;x1], 'newline','pc','-append');
end

end










% function prepareData( varargin) 
% 
% global date high low close open vol;
% 
% % load IDNames_copy.mat;
% load IDNames.mat;
% delete('dataML.txt');
% for i=1:length(IDNames)
%     if IDNames{i}(3)=='X'
% %     if IDNames{i}(3)=='6'
% %     if IDNames{i}(3)~='3'
% %     if IDNames{i}(3)~='0'
% %     if IDNames{i}(3)~='6'
%         continue;
%     end
%     name_f=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\AllStocks\',IDNames{i},'.txt');
% %     name_f=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest\',IDNames{i},'.txt');
%     fid=fopen(name_f);
%     Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
%     fclose(fid);
%     L=length(Data{1})-1;
%     if L<50
%         continue;
%     end
%     date=Data{1}(1:L);
% %     open=Data{2}(1:L);
%     high=Data{3}(1:L);
%     low=Data{4}(1:L);
%     close=Data{5}(1:L);
%     vol=Data{6}(1:L);
%     x=zeros(5000,6);
%     y=zeros(5000,1);
%     for j=15:L-5
%         if close(j)<2
%             continue;
%         end
%         highPoint=highest(j-12,j);
%         lowPoint=lowest(j-12,j);
%         x(j-14,1)=(close(j)-close(j-1))/close(j-1);
%         x(j-14,2)=double(vol(j)-vol(j-1))/double(vol(j-1));
%         everPrice=mean(close(j-11:j));
%         x(j-14,3)=(close(j)-everPrice)/everPrice;
%         everVol=double(mean(vol(j-11:j)));
%         x(j-14,4)=double(vol(j)-everVol)/everVol;
%         x(j-14,5)=(j-highPoint)/12;
%         x(j-14,6)=(j-lowPoint)/12;
%         if low(j)<low(lowest(j+1,j+4))&& datenum(date(j+4))-datenum(date(j))<=10&&low(lowest(j-2,j))<=low(lowest(j-12,j))
%             upratio=(high(highest(j+1,j+4))-low(j))/low(j);
%             if upratio>0.15 && upratio<0.3
%                 y(j-14)=1;
%             elseif upratio>=0.3
%                 y(j-14)=2;
%             end
%         end                                      
%     end
% 
% x0=x(y(1:L-19)==0,:);
% x0=x0(x0(:,1)~=0&x0(:,2)~=0,:);
% x1=x(y==1,:);
% x2=x(y==2,:);
% 
% % x0=[x0,zeros(size(x0,1),1)];
% % x1=[x1,ones(size(x1,1),1)];
% % x2=[x2,2*ones(size(x2,1),1)];
% % dlmwrite('dataML.txt', [x0;x1;x2], 'newline','pc','-append');
% y(y==2)=1;
% for i=2:L-19
%     if i<=5
%         if sum(y(1:i-1))>0&&y(i)==1
%             y(i)=0;
%         end
%     else
%         if y(i)==1&&sum(y(i-5:i-1))>0
%             y(i)=0;
%         end
%     end
% end
% tem=sum(y);
% temRand=randperm(size(x0,1));
% x0=x0(temRand(1:tem),:);
% x1=x(y==1,:);
% 
% x0=[x0,zeros(size(x0,1),1)];
% x1=[x1,ones(size(x1,1),1)];
% dlmwrite('dataML.txt', [x0;x1], 'newline','pc','-append');
% end
% % save dataML X Y
% % dlmwrite('dataML.txt',[X,Y],'newline','pc');
% end
% 
% % [num, text, raw] = xlsread(fileName);
% % [rowN, columnN]=size(raw);
% % sheet=1;
% % xlsRange=['A',num2str(rowN+1)];
% % xlswrite(fileName,data,sheet,xlsRange);
% 
% 
