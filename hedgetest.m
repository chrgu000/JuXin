function hedgetest(varargin) % draw each pair of stocks' difference to test its hedge result;
                             % if there is no varargin, it will test selected dir's stocks.
if nargin~=0
    filenames=strcat(varargin,'.txt');
else
    path=uigetdir;
    files=dir(strcat(path,'\*.txt'));
    filenames={files.name};
end
[C,L]=arrayfun(@(x) getclose(x),filenames);

stockN=length(C);
Lmin=min(L);
close(1:Lmin,stockN)=0;
for i=1:stockN
    close(:,i)=C{i}(end-Lmin+1:end);
end
ud=close(2:end,:)./close(1:end-1,:);

k=nchoosek(1:length(L),2);
Lk=size(k,1);
diff(Lmin-1,Lk)=0;

for i=1:Lk   % get diff of each pair of columns;
    diff(:,i)=ud(:,k(i,2))-ud(:,k(i,1));
end

diffAccum(Lmin-1,Lk)=0; % initialization
diffAccum(1,:)=diff(1,:); % get diffAccum's value;
for i=2:Lmin-1
    diffAccum(i,:)=diffAccum(i-1,:)+diff(i-1,:);
end

reverInd=diffAccum(end,:)<0; % reverse the negtive items;
diffAccum(:,reverInd)=-diffAccum(:,reverInd);

x=1:Lmin;
ratio=close(1,1)./close(1,2:end);
figure;

[~,H1,H2]=plotyy(repmat(x',1,stockN),close.*repmat([1 ratio],Lmin,1),repmat(x(1:end-1)',1,Lk),diffAccum); 
legend(H1,filenames(:));
legend(H2,num2str(k));

% H=plot(repmat(x(1:end-1)',1,Lk),diffAccum);
% legend(H,num2str(k));
% text(1,max(max(diffAccum)),filenames(:))

set(gca,'XTick',1:150:x(end));
grid on;

% averN=10;
% diffSum(Lmin-averN,Lk)=0;
% for i=averN:Lmin-1
%     diffSum(i-averN+1)=sum(diff(i-averN+1:i,:));
% end
% figure;
% [~,H1,H2]=plotyy(repmat(x',1,stockN),close.*repmat([1 ratio],Lmin,1),repmat(x(1:end-averN)',1,Lk),diffSum); 
% legend(H1,filenames(:));
% legend(H2,num2str(k));
% set(gca,'XTick',1:50:x(end));
% grid on;

end


function [C,L]=getclose(stockcode)
filename=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest\',stockcode{1});
fid=fopen(filename);
Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
fclose(fid);
C={Data{5}(1:end-1)};
L=length(C{:});
end