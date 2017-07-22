function tester(stockname,fun1) % modify stop loss point : when up over middle high point, modify stop loss as high point.
global high low close open date vol;

file=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest\',stockname,'.txt');
fid=fopen(file);
Data=textscan(fid,'%s %f %f %f %f %d %d','headerlines',2);  
fclose(fid);
Date=Data{1}(1:end-1);
Open=Data{2}(1:end-1);
High=Data{3}(1:end-1);
Low=Data{4}(1:end-1);
Close=Data{5}(1:end-1);
Vol=Data{6}(1:end-1);
L=length(Date);
Sig(6)=0;
Capi(L)=0;
Lcapi=2; % capital's index;
ind=0;  % index of line which show one trade;
linex(2,500)=0; 
liney(2,500)=0;
winN=0; % win trades' number;
lossN=0; % loss trades' number;
X3(3,1000)=0;
Y3(3,1000)=0;

stopX(1000)=0;
stopY(1000)=0;

for i=200:L % 30 is changed into 300;
    date=Date(1:i);
    high=High(1:i);
    low=Low(1:i);
    close=Close(1:i);
    open=Open(1:i);
    vol=Vol(1:i);

    if Sig(1)>0
        
        for j=i-20:i-7 % seek for bottom support;
            lowB=lowest(j,i);
            temp=low(lowB)*0.98;
            if low(lowB)<=low(lowest(lowB-4,i)) && i-lowB>2 && temp>Sig(3) && temp <close(i)
                Sig(3)=temp;
                Sig(5)=lowB;
                
                lx=sum(stopX~=0);
                stopX(lx+1)=Sig(5);
                stopY(lx+1)=Sig(3);
            end
        end
        
%         holdD=i-Sig(4);
%         if holdD>=2 && holdD<re1/2
%             if Sig(3)<Sig(2) && high(highest(Sig(5),i))>high(Sig(4))*1.05 % && close(i)>Sig(2)*1.03
%                 Sig(3)=high(highest(Sig(5),i))*0.98;
%                 Sig(5)=i;
%             end
%             
%             if low(i)<low(i-1)*0.995 % && high(i)-close(i)>(high(i)-low(i))*3/4% high(i)<mean(high(i-5:i-1)) % && high(highest(Sig(4),i))<beginH
%                 Capi(Lcapi)=Capi(Lcapi-1)+(close(i)-Sig(2))/abs(Sig(2));
%                 Lcapi=Lcapi+1;
%                 if close(i)>Sig(2)
%                     winN=winN+1;
%                 else
%                     lossN=lossN+1;
%                 end
%                 
%                 ind=ind+1;
%                 linex(1,ind)=Sig(4);
%                 linex(2,ind)=i;
%                 liney(1,ind)=Sig(2);
%                 liney(2,ind)=close(i);
%                 Sig(1:5)=0;
%             end
%         end
        
        
        if Sig(3)>low(i) % stop loss;
            Capi(Lcapi)=Capi(Lcapi-1)+(Sig(3)-Sig(2))/abs(Sig(2));            
            Lcapi=Lcapi+1;
            
            if Sig(3)>Sig(2)
                winN=winN+1;
            else
                lossN=lossN+1;
            end

            ind=ind+1;            
            linex(1,ind)=Sig(4);
            linex(2,ind)=i;
            liney(1,ind)=Sig(2);
            liney(2,ind)=Sig(3);
            
            Sig(1:6)=0;
        end
        
    end
    
    if Sig(1)==0   % if there is not order which is hold.
        [re1,x3,y3]=fun1(); % tested function;
        if re1>0 && close(i)~=0 % && weekday(date(i))-1==5  % && mean(close(i-re1:i))>mean(close(temp:i)) 

            Sig(1)=re1;
            Sig(2)=close(i); % open price
            Sig(3)=low(i)*0.98; %low(lowest(i-3,i))*0.97;  % stop price
            Sig(4)=i;   % open bar;
            Sig(5)=i; % stop bar;
            Sig(6)=highest(i-re1,i); % high bar between low and high points.
            
            Temp=sum(sum(X3)~=0);
            temp=sum(sum(x3)~=0);
            X3(:,Temp+1:Temp+temp)=x3;
            Y3(:,Temp+1:Temp+temp)=y3;
            
            lx=sum(stopX~=0);
            stopX(lx+1)=Sig(5);
            stopY(lx+1)=Sig(3);
        end
    end
    
    if i==L && Sig(1)>0
        Capi(Lcapi)=Capi(Lcapi-1)+(close(i)-Sig(2))/abs(Sig(2));  
        ind=ind+1; 
        linex(1,ind)=Sig(4);
        linex(2,ind)=i;
        liney(1,ind)=Sig(2);
        liney(2,ind)=close(i);
        Sig(1:6)=0;
    end    
end

figure;
candle(high,low,close,open);
line(linex(:,1:ind),liney(:,1:ind),'Color','r','LineWidth',3);
columnN=sum(sum(X3)~=0);
line(X3(:,1:columnN),Y3(:,1:columnN),'Color','r');

hold on;
plot(stopX,stopY,'>');
hold off;

figure;
plot(Capi(Capi~=0));
text(min(get(gca,'XTick')),max(get(gca,'YTick')),num2str([lossN+winN roundn(winN/(lossN+winN),-3)]),'Color','r'); 

end