function drawK(stockname,n1,n2)
% function drawK(stockname)
global date high low close open vol;
file=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest\',stockname,'.txt');
fid=fopen(file);
Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
fclose(fid);
date=Data{1}(1:end-1);
open=Data{2}(1:end-1);
high=Data{3}(1:end-1);
low=Data{4}(1:end-1);
close=Data{5}(1:end-1);
vol=Data{6}(1:end-1);
L=length(date);

if nargin==3
    n12=n1:n2;
elseif nargin==1
    n12=1:L;
else
    warndlg('parameters'' number is wrong!');
    return;
end
high=high(n12);
low=low(n12);
close=close(n12);
open=open(n12);

atrange=ATR(length(high),12);

figure;
subplot(3,1,[1 2])
candle(high,low,close,open);
grid on;
subplot(3,1,3);
line(n12',atrange);
grid on;
end