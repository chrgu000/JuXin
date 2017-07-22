w=windmatlab;
[~,stocks]=xlsread('C:\Users\Administrator\Desktop\¹ÉÆ±´úÂë.xlsx');
filename='E:\All_data2_before20110406\';
L=length(stocks);
for i=1:L
    tic;
    filepath=strcat(filename,stocks(i));
    while  1
        display(strcat(stocks(i),': first 3-years'));
        [data1,~,~,time1,werrors]=w.wsi(stocks(i),'open,close,high,low,volume','2008-04-07 09:00:00','2011-04-06 15:30:00','PriceAdj=F');
        if length(time1)>1
            break;
        end
        werrors
    end
    indTem=sum(isnan(data1(:,1)));
    if indTem==0
        save data1;
        save time1;
    else
        data1=data1(indTem+1:end,:);
        time1=time1(indTem+1:end);
        data=data1;
        time=time1;
        save(filepath{1}(1:end-3),'data','time');
        continue;
    end
    
    while  1
        display(strcat(stocks(i),': second 3-years'));
        [data2,~,~,time2,werrors]=w.wsi(stocks(i),'open,close,high,low,volume','2005-04-07 09:00:00','2008-04-06 15:30:00','PriceAdj=F');
        if length(time2)>1
            break;
        end
        werrors
    end
    indTem=sum(isnan(data2(:,1)));
    if indTem>0
        data2=data2(indTem+1:end,:);
        time2=time2(indTem+1:end);
    end
    data=[data1;data2];
    time=[time1;time2];
    save(filepath{1}(1:end-3),'data','time');
    toc;  
end