function [data,stock]=test_Reverse(StockName) % modify stop loss point : when up over middle high point, modify stop loss as high point.

global high low close open date vol;
if ischar(StockName)
    stockname=StockName;
else
    stockname=StockName{:};
end
file=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest\',stockname,'.txt');
fid=fopen(file);
Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
fclose(fid);
L=length(Data{1})-1;
firstbar=1;
lastbar=L;
date=Data{1}(firstbar:lastbar);
open=Data{2}(firstbar:lastbar);
high=Data{3}(firstbar:lastbar);
low=Data{4}(firstbar:lastbar);
close=Data{5}(firstbar:lastbar);
vol=Data{6}(firstbar:lastbar);

Sig(6)=0;
Capi(L)=0;
CapiRaw(L)=0;
Lcapi=1; % capital's index;
ind=0;  % index of line which show one trade;
linex(2,500)=0; 
liney(2,500)=0;
winN=0; % win trades' number;
lossN=0; % loss trades' number;

stopX(1000)=0;
stopY(1000)=0;


for i=200:L 
    
    if Sig(1)==0   % if there is not order which is hold.
        re1=Model_Reverse(i); % tested function;
%         WD=weekday(date(i))-1;
        if re1>0  % && WD==4

            Sig(1)=re1;
            Sig(2)=re1; % open price
            Sig(3)=re1*0.98; %low(lowest(i-3,i))*0.97;  % stop price
            Sig(4)=i;   % open bar;
            Sig(5)=i; % stop bar;
%             Sig(6)=highest(i-re1,i); % high bar between low and high points.
                      
            lx=sum(stopX~=0);
            stopX(lx+1)=Sig(5);
            stopY(lx+1)=Sig(3);
    
        end
    end
    
    

    if Sig(1)>0
        if  i-Sig(5)>10 && open(i)>Sig(2) % more days to stay, more profit to get; it is really amazing!
            Cprice=close(i);
            if Sig(2)>0.5
                addC=(Cprice-Sig(2))/Sig(2)-0.005;
                if Lcapi==1
                    Capi(Lcapi)=addC;
                else
                    Capi(Lcapi)=Capi(Lcapi-1)+addC;
                end
                Lcapi=Lcapi+1;
            end
            if Cprice>Sig(2)*1.005
                winN=winN+1;
            else
                lossN=lossN+1;
            end
            
            ind=ind+1;
            linex(1,ind)=Sig(4);
            linex(2,ind)=i;
            liney(1,ind)=Sig(2);
            liney(2,ind)=Cprice;
            Sig(1:5)=0;
        end 
        
        if low(i)<Sig(3) && i-Sig(4)>0
            Cprice=min(open(i),Sig(3));
            if Sig(2)>0.5
                addC=(Cprice-Sig(2))/Sig(2)-0.005;
                if Lcapi==1
                    Capi(Lcapi)=addC;
                else
                    Capi(Lcapi)=Capi(Lcapi-1)+addC;
                end
                Lcapi=Lcapi+1;
            end
            if Cprice>Sig(2)*1.005
                winN=winN+1;
            else
                lossN=lossN+1;
            end
            ind=ind+1;
            linex(1,ind)=Sig(4);
            linex(2,ind)=i;
            liney(1,ind)=Sig(2);
            liney(2,ind)=Cprice;
            Sig(1:5)=0;
        end
        
    end
    
    
    if i==L && Sig(1)>0
        if Sig(2)>0.5
            addC=(close(i)-Sig(2))/Sig(2)-0.005;
            if Lcapi==1
                Capi(Lcapi)=addC;
            else
                Capi(Lcapi)=Capi(Lcapi-1)+addC;
            end
            Lcapi=Lcapi+1;
        end
        if close(i)>Sig(2)*1.005
            winN=winN+1;
        else
            lossN=lossN+1;
        end
        ind=ind+1; 
        linex(1,ind)=Sig(4);
        linex(2,ind)=i;
        liney(1,ind)=Sig(2);
        liney(2,ind)=close(i);
        Sig(1:6)=0;
    end
    if Lcapi==1
        temp=1;
    else
        temp=Lcapi-1;
    end
    CapiRaw(i)=Capi(temp);
end

    orders=sum(Capi~=0);
    Orders=winN+lossN;
    if orders>5 % just consider the situation of generating at least 15 orders.
        win=roundn(winN/Orders,-3);
        if orders==0
            capi=0;
        else
            capi=roundn(Capi(orders),-3);
        end
        profitP=roundn(capi/orders,-3);
        
        drawB=0;
        if orders>1
            for i=1:orders-1
                mindiff=Capi(i)-min(Capi(i+1:orders));
                if drawB<mindiff
                    drawB=mindiff;
                end
            end
        end
    else
        win=-1;
        capi=-1;
        profitP=-1;
        drawB=-1;        
    end
    drawB=roundn(drawB,-3);
    data=[profitP,capi,orders,win,drawB];
    stock=stockname;
    
    if ischar(StockName)
        figure;
        candle(high,low,close,open);
        line(linex(:,1:ind),liney(:,1:ind),'Color','r','LineWidth',3);
        hold on;
        plot(stopX,stopY,'>');
        hold off;
        grid on; 
        
        figure;
        plot(CapiRaw);
        
        figure;
        plot(Capi(Capi~=0));
        text(min(get(gca,'XTick')),max(get(gca,'YTick')),num2str([lossN+winN,win,profitP,drawB]),'Color','r'); 
    end
    
end