w=windmatlab;
[~,stocks]=xlsread('C:\Users\Administrator\Desktop\文档\EXCEL数据文件\股票代码.xlsx');
[~,stocks2]=xlsread('C:\Users\Administrator\Desktop\文档\EXCEL数据文件\股票代码2.xlsx');
[~,index]=xlsread('C:\Users\Administrator\Desktop\文档\EXCEL数据文件\指数.xlsx');
step=7;
%data=zeros(177144,6);
filename='E:\All_data2(2001-3000)\';
for i=2233:3000
    tic
    open=w.wsi(stocks(i),'open','2011-04-07 09:00:00','2014-04-06 15:30:00');
    close=w.wsi(stocks(i),'close','2011-04-07 09:00:00','2014-04-06 15:30:00');
    high=w.wsi(stocks(i),'high','2011-04-07 09:00:00','2014-04-06 15:30:00');
    low=w.wsi(stocks(i),'low','2011-04-07 09:00:00','2014-04-06 15:30:00');
    [volume,w_wsi_codes,w_wsi_fields,w_wsi_times,w_wsi_errorid,w_wsi_reqid]=w.wsi(stocks(i),'volume','2011-04-07 09:00:00','2014-04-06 15:30:00'); 
%     open=w.wsi(stocks(i),'open','2003-04-07 09:00:00','2014-04-06 15:30:00');
%     close=w.wsi(stocks(i),'close','2003-04-07 09:00:00','2014-04-06 15:30:00');
%     high=w.wsi(stocks(i),'high','2003-04-07 09:00:00','2014-04-06 15:30:00');
%     low=w.wsi(stocks(i),'low','2003-04-07 09:00:00','2014-04-06 15:30:00');
%     [volume,w_wsi_codes,w_wsi_fields,w_wsi_times,w_wsi_errorid,w_wsi_reqid]=w.wsi(stocks(i),'volume','2003-04-07 09:00:00','2014-04-06 15:30:00');
%     [w_wsi_data,w_wsi_codes,w_wsi_fields,w_wsi_times,w_wsi_errorid,w_wsi_reqid]=w.wsi(stocks(i),'open,close,high,low,volume','2016-04-06 09:00:00','2014-04-06 15:30:00');
try  
data=[open,close,high,low,volume,w_wsi_times];
catch
    if size(open)==[1,1]
         open=w.wsi(stocks(i),'open','2011-04-07 09:00:00','2014-04-06 15:30:00');
    end
    if size(close)==[1,1]
         close=w.wsi(stocks(i),'open','2011-04-07 09:00:00','2014-04-06 15:30:00');   
    end
     if size(high)==[1,1]
         high=w.wsi(stocks(i),'open','2011-04-07 09:00:00','2014-04-06 15:30:00');   
     end
     if size(low)==[1,1]
         low=w.wsi(stocks(i),'open','2011-04-07 09:00:00','2014-04-06 15:30:00');   
     end
     if size(volume)==[1,1]
        [volume,w_wsi_codes,w_wsi_fields,w_wsi_times,w_wsi_errorid,w_wsi_reqid]=w.wsi(stocks(i),'volume','2011-04-07 09:00:00','2014-04-06 15:30:00'); 
     end
    data=[open,close,high,low,volume,w_wsi_times]; 
end

  filepath=strcat(filename,[char(stocks2(i))]);
  save(filepath,'data');
  %delete(h);
  toc
end