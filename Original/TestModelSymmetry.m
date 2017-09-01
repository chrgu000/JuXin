function TestModelSymmetry %取最低点时候low(ii-x)<=min(low(ii-y:ii))， 变动y值对最终结果影响很大;今日最高点小于区间最高点；收盘价大于昨日收盘价；
%sort by week day;
tic; 
global high low close open vol;
try
    load allStocks1;
    load allStocks2;
catch
    w=windmatlab;
    dataTem=w.wset('sectorconstituent','a001010100000000');
    stocks=dataTem(:,2);
    Lt=length(stocks);
    Date=w.tdays('ED-3000TD',today-1);
    opens=[];
    closes=[];
    highs=[];
    lows=[];
    vols=[];
    for i=1:400:Lt
        if i+399<=Lt
            iend=i+399;
        else
            iend=Lt;
        end
        while 1
            openT=w.wsd(stocks(i:iend),'open','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
            if length(openT)>1
                break;
            end
        end
        while 1
            closeT=w.wsd(stocks(i:iend),'close','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
            if length(closeT)>1
                break;
            end
        end
        while 1
            highT=w.wsd(stocks(i:iend),'high','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
            if length(highT)>1
                break;
            end
        end
        while 1
            lowT=w.wsd(stocks(i:iend),'low','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
            if length(lowT)>1
                break;
            end
        end
        while 1
            volT=w.wsd(stocks(i:iend),'volume','ED-3000TD',today-1,'Fill=Previous','PriceAdj=F');
            if length(volT)>1
                break;
            end
        end       
        opens=[opens,openT];
        closes=[closes,closeT];
        highs=[highs,highT];
        lows=[lows,lowT];
        vols=[vols,volT];
    end    
    save allStocks1 stocks Date opens closes;
    save allStocks2 highs lows vols;
end
Lstocks=size(opens,2);
Rall={}; % save all stocks return by one cell to one stock;
Radd=[];
namesRall={};
iStart=1;
iEnd=Lstocks;%1980
% iStart=100; % draw picture;
% iEnd=500;
keyTest=4;

if iEnd-iStart<50
    fig=1;
else
    fig=0;
end
Days=0;
DaysAdd=0;
listCorr=[];
for i=iStart:iEnd
% for i=100:110
%     if i>1329
%         continue;
%     end
    open=opens(:,i);
    close=closes(:,i);
    high=highs(:,i);
    low=lows(:,i);
    vol=vols(:,i); 
    datei=Date;
    indTem=~isnan(open);
    open=open(indTem);
    close=close(indTem);
    high=high(indTem);
    low=low(indTem);
    vol=vol(indTem);
    datei=datei(indTem);

    L=length(high);
    indTarget=[];
    Target=[];
    Ri=[];
    indAdd={};
    Add={};
    
    for ii=80:L-10
        switch keyTest
            case  0
                if low(ii-keyTest+1)<=min(low(ii-keyTest*2:ii))&&high(ii)<max(high(ii-keyTest/2:ii-keyTest/2+1))
                    Tem=[high(ii-keyTest+1:ii-keyTest/2),low(ii-keyTest+1:ii-keyTest/2)];   
                    Tem=Tem(2:end,:)-Tem(1:end-1,:);        
                    Tem=sum(Tem>=0);                      
                    highL=Tem(1);
                    lowL=Tem(2);
                    Tem=low(ii-keyTest/2+1:ii);
                    Tem=Tem(2:end)-Tem(1:end-1);
                    Tem=sum(Tem<=0);
                    lowR=Tem;
                    Tem=high(ii-keyTest/2+1:ii-1);
                    Tem=Tem(2:end)-Tem(1:end-1);
                    Tem=sum(Tem<=0);
                    highR=Tem;
                    numbersConf=keyTest/2-2;
                    if highL>=numbersConf&&lowL>=numbersConf&&lowR>=numbersConf&&highR>=numbersConf-1&&close(ii)>close(ii-1)&&high(ii)<mean([max(high(ii-keyTest+1:ii)),min(low(ii-keyTest/2:ii))])&&...                
                            close(ii)/close(ii-1)<1.09 % for current bar   %close(ii)>=low(ii)+(high(ii)-low(ii))*0.5 &&
                        listUp=[low(ii-5),open(ii-5),close(ii-5),high(ii-5),low(ii-4),open(ii-4),close(ii-4),high(ii-4),low(ii-3),open(ii-3),close(ii-3),high(ii-3)];
                        listDown=[low(ii),close(ii),open(ii),high(ii),low(ii-1),close(ii-1),open(ii-1),high(ii-1),low(ii-2),close(ii-2),open(ii-2),high(ii-2)];
                        listCorri=[corr2(listUp(1:4),listDown(1:4)),corr2(listUp(5:8),listDown(5:8)),corr2(listUp(9:12),listDown(9:12))];
                        if 1%listCorri(3)<0.95
                            daysHold=1;
                            RTem=close(ii+daysHold)/close(ii)-1.003;
                            Ri=[Ri,RTem];
                            indTarget=[indTarget,[ii;ii+daysHold]];
                            Target=[Target,[close(ii);close(ii+daysHold)]];
                            Days=Days+daysHold;
                            listCorr=[listCorr;listCorri];
                            
%                             if close(ii+1)-open(ii+1)>=(high(ii)-low(ii))*1.1
%                                     RTem=close(ii+2)/close(ii)-1.003;
%                                     Ri(end)=RTem;
%                                     indTarget(end)=ii+2;
%                                     Target(end)=close(ii+2);
%                                     Days=Days+1;
%                                     Radd=[Radd,close(ii+2)/close(ii+1)-1.003];
%                                     DaysAdd=DaysAdd+1;
%                             end
% 
%                             if  close(ii+1)>=low(ii+1)+(high(ii+1)-low(ii+1))*0.9&&close(ii+1)>close(ii)*1.03
%                                     RTem=close(ii+2)/close(ii)-1.003;
%                                     Ri(end)=RTem;
%                                     indTarget(end)=ii+2;
%                                     Target(end)=close(ii+2);
%                                     Days=Days+1;
%                                     Radd=[Radd,close(ii+2)/close(ii+1)-1.003];
%                                     DaysAdd=DaysAdd+1;
%                             end
 
%                             addi=[];
%                             indAddi=[];
%                             Addi=[];
%                             daysHold=6;
%                             for i3=ii+1:ii+daysHold % seek for point which should close the order
%                                 tem=1-1/(i3-ii+1);
%                                 if close(i3)>=low(i3)+(high(i3)-low(i3))*tem 
%                                     RTem=close(i3+1)/close(ii)-1.002;
%                                     Ri(end)=RTem;
%                                     indTarget(end)=i3+1;
%                                     Target(end)=close(i3+1);
%                                     addi=[addi,close(i3)];
%                                     indAddi=[indAddi,i3-ii];
%                                     Addi=[Addi,close(i3)];
%                                     Days=Days+1;
%                                 else
%                                     break;
%                                 end
%                             end
%                             if ~isempty(addi) % add orders;
%                                 addi=close(i3)./addi-1.002;
%                                 Radd=[Radd,addi];
%                                 Lt=length(indAddi);
%                                 if i3==ii+daysHold
%                                     dateClose=i3+1;
%                                 else
%                                     dateClose=i3;
%                                 end
%                                 indAdd=[indAdd,[indAddi;ones(1,Lt)*(dateClose-ii)]];
%                                 Add=[Add,[Addi;ones(1,Lt)*close(dateClose)]];
%                             end

%                             stopP=low(ii);% stop loss
%                             if low(ii+1)<=stopP
%                                 if open(ii+1)<stopP
%                                     stopP=open(ii+1);
%                                 end
%                                 RTem=stopP/close(ii)-1.002;
%                                 Ri(end)=RTem;
%                                 indTarget(end)=ii+1;
%                                 Target(end)=stopP;
%                             end    
    
                        end                
                    end
                end
                
            case 3
%                 if low(ii-2)<=min(low(ii-6:ii)) && high(ii-1)>max(high([ii-2,ii]))&&low(ii-1)>low(ii)&&...                                  % 1100--IR:0.3855; winRatio(ratioWL):66.91%(1.41);
%                         close(ii-2)>open(ii-2)&&close(ii)>=close(ii-1)*1.025 &&...                                                        %   %  maxDraw:29.20%; profitP/profitPperDay: 1.7189%/1.5629%
%                         close(ii)>=low(ii)+(high(ii)-low(ii))*0.7 && close(ii)/close(ii-1)<1.09                
%                     listUp=[low(ii-2),open(ii-2),close(ii-2),high(ii-2)];
%                     listDown=[low(ii),close(ii),open(ii),high(ii)];
%                     listCorri=corr2(listUp,listDown);
% %                     if listCorri<0.9
% %                     else
% %                         continue;
% %                     end
%                     RTem=close(ii+1)/close(ii)-1.003;
%                     Ri=[Ri,RTem];
%                     indTarget=[indTarget,[ii;ii+1]];
%                     Target=[Target,[close(ii);close(ii+1)]];
%                     Days=Days+1;
%                     listCorr=[listCorr;listCorri];  
%                     
%                     if close(ii+1)-open(ii+1)>=(high(ii)-low(ii))*1.1                        
%                         RTem=close(ii+2)/close(ii)-1.003;
%                         Ri(end)=RTem;
%                         indTarget(end)=ii+2;
%                         Target(end)=close(ii+2);
%                         Days=Days+1;
%                         Radd=[Radd,close(ii+2)/close(ii+1)-1.003];
%                         DaysAdd=DaysAdd+1;
%                     end       
%                     
% %                     if RTem>0
% %                         RTem=close(ii+2)/close(ii)-1.002;
% %                         Ri(end)=RTem;
% %                         indTarget(end)=ii+2;
% %                         Target(end)=close(ii+2);
% %                     end
% 
% %                     stopP=low(ii);% stop loss
% %                     if low(ii+1)<=stopP
% %                         if open(ii+1)<stopP
% %                             stopP=open(ii+1);
% %                         end
% %                         RTem=stopP/close(ii)-1.002;
% %                         Ri(end)=RTem;
% %                         indTarget(end)=ii+1;
% %                         Target(end)=stopP;
% %                     end  
%                 end
%                 
                
                if low(ii-2)<=min(low(ii-6:ii))&&high(ii)<max(high(ii-2:ii-1)) &&...                                                     % % % 1800--IR:0.4632; winRatio(ratioWL):67.71%(1.66);
                        close(ii-2)>open(ii-2)&&close(ii-1)<open(ii-1)&&close(ii)>close(ii-1)*1.03&&...                                                        % maxDraw:28.56%; profitP/profitPperDay: 2.0130%/1.8046%;
                        close(ii)>=low(ii)+(high(ii)-low(ii))*0.7 && close(ii)/close(ii-1)<1.09 % for current bar
                    listUp=[low(ii-2),open(ii-2),close(ii-2),high(ii-2)];
                    listDown=[low(ii-1),close(ii-1),open(ii-1),high(ii-1)];
                    listCorri=corr2(listUp,listDown);
                    if weekday(datei(ii))-1~=3  %Orders:819; IR:0.8550; winRatio(ratioWL):81.81%(1.97);
                    else                       %maxDraw:12.51%; profitP/profitPperDay: 3.2258%/2.8842%
                        continue;
                    end

                    RTem=close(ii+1)/close(ii)-1.003;
                    Ri=[Ri,RTem];
                    indTarget=[indTarget,[ii;ii+1]];
                    Target=[Target,[close(ii);close(ii+1)]];
                    Days=Days+1;
                    listCorr=[listCorr;listCorri];
                    if close(ii+1)-open(ii+1)>=(high(ii)-low(ii))*1.1
                            RTem=close(ii+2)/close(ii)-1.003;
                            Ri(end)=RTem;
                            indTarget(end)=ii+2;
                            Target(end)=close(ii+2);
                            Days=Days+1;
                            Radd=[Radd,close(ii+2)/close(ii+1)-1.003];
                            DaysAdd=DaysAdd+1;
                            
                    end
                end

            case 4                      
%                 if low(ii-3)<=min(low(ii-7:ii)) && high(ii-2)>=max(high(ii-3:ii))&&low(ii-1)<low(ii-2)&&...                      % Orders:962; IR:0.4635; winRatio(ratioWL):66.63%(2.02);
%                         low(ii-2)>low(ii-1)&& close(ii)>=close(ii-1)*1.03 &&...                                                %   % % maxDraw:21.82%; profitP/profitPperDay: 1.7947%/1.5957%
%                         close(ii)>=low(ii)+(high(ii)-low(ii))*0.8 && close(ii)/close(ii-1)<1.09               
%                     listUp=[low(ii-3),open(ii-3),close(ii-3),high(ii-3)];
%                     listDown=[low(ii-1),close(ii-1),open(ii-1),high(ii-1)];
%                     listCorri=corr2(listUp,listDown);
%                     if listCorri<0.93
%                         RTem=close(ii+1)/close(ii)-1.003;
%                         Ri=[Ri,RTem];
%                         indTarget=[indTarget,[ii;ii+1]];
%                         Target=[Target,[close(ii);close(ii+1)]];
%                         Days=Days+1;
%                         listCorr=[listCorr;listCorri];  
%                         if close(ii+1)-open(ii+1)>=(high(ii)-low(ii))*1.1
%                             RTem=close(ii+2)/close(ii)-1.003;
%                             Ri(end)=RTem;
%                             indTarget(end)=ii+2;
%                             Target(end)=close(ii+2);
%                             Days=Days+1;
%                             Radd=[Radd,close(ii+2)/close(ii+1)-1.003];
%                             DaysAdd=DaysAdd+1;
%                         end       
% 
% %                         if RTem>0
% %                             RTem=close(ii+2)/close(ii)-1.002;
% %                             Ri(end)=RTem;
% %                             indTarget(end)=ii+2;
% %                             Target(end)=close(ii+2);
% %                         end
% 
% %                         stopP=low(ii);% stop loss
% %                         if low(ii+1)<=stopP
% %                             if open(ii+1)<stopP
% %                                 stopP=open(ii+1);
% %                             end
% %                             RTem=stopP/close(ii)-1.002;
% %                             Ri(end)=RTem;
% %                             indTarget(end)=ii+1;
% %                             Target(end)=stopP;
% %                         end  
% 
%                     end                    
%                 end
                
                if low(ii-3)<=min(low(ii-7:ii)) && high(ii-3)<high(ii-2)&&low(ii-3)<low(ii-2)&& high(ii)<high(ii-1)&&...                % % 1100---IR:0.3660; winRatio(ratioWL):62.80%(1.83);
                        low(ii)<low(ii-1)&&close(ii)>=close(ii-1)*1.015&&...                                                           %   % maxDraw:29.76%; profitP/profitPperDay: 1.5388%/1.3490%;
                        close(ii)>=low(ii)+(high(ii)-low(ii))*0.8 && close(ii)/close(ii-1)<1.09                                 
                    listUp=[low(ii-3),open(ii-3),close(ii-3),high(ii-3),low(ii-2),open(ii-2),close(ii-2),high(ii-2)];
                    listDown=[low(ii),close(ii),open(ii),high(ii),low(ii-1),close(ii-1),open(ii-1),high(ii-1)];
                    listCorri=[corr2(listUp(1:4),listDown(1:4)),corr2(listUp(5:8),listDown(5:8))];
                    if listCorri(1)<0.85&&listCorri(2)<0.9
                        RTem=close(ii+1)/close(ii)-1.003;
                        Ri=[Ri,RTem];
                        indTarget=[indTarget,[ii;ii+1]];
                        Target=[Target,[close(ii);close(ii+1)]];
                        Days=Days+1;
                        listCorr=[listCorr;listCorri];  
                        if close(ii+1)-open(ii+1)>=(high(ii)-low(ii))*1.1
                            RTem=close(ii+2)/close(ii)-1.003;
                            Ri(end)=RTem;
                            indTarget(end)=ii+2;
                            Target(end)=close(ii+2);
                            Days=Days+1;
                            Radd=[Radd,close(ii+2)/close(ii+1)-1.003];
                            DaysAdd=DaysAdd+1;
                        end       

%                         if RTem>0
%                             RTem=close(ii+2)/close(ii)-1.002;
%                             Ri(end)=RTem;
%                             indTarget(end)=ii+2;
%                             Target(end)=close(ii+2);
%                         end
                    end
                end
                
            case 5                    
                if low(ii-4)<=min(low(ii-10:ii)) && high(ii-2)>max([high(ii-4:ii-3);high(ii-1:ii)])&&...                                                % Orders:1837; IR:0.4824; winRatio(ratioWL):70.88%(2.02);
                       close(ii)>close(ii-1)*1.02&&low(ii)>=low(ii-4) &&...%&&close(ii)>min(close(ii-4:ii-1))*1.05 important;                         %   % maxDraw:25.25%; profitP/profitPperDay: 1.6214%/1.4615%;
                       close(ii)>=low(ii)+(high(ii)-low(ii))*0.8 && close(ii)/close(ii-1)<1.09                                                      %      %
                   
                   if mod(weekday(datei(ii))-1,2)==1 %Orders:1237; IR:0.5552; winRatio(ratioWL):75.67%(2.16);
                   else                              %maxDraw:25.25%; profitP/profitPperDay: 1.9444%/1.7442%
                       continue;
                   end
                   
                   listUp=[low(ii-4),open(ii-4),close(ii-4),high(ii-4),low(ii-3),open(ii-3),close(ii-3),high(ii-3)];                                 
                   listDown=[low(ii),close(ii),open(ii),high(ii),low(ii-1),close(ii-1),open(ii-1),high(ii-1)];
                   listCorri=[corr2(listUp(1:4),listDown(1:4)),corr2(listUp(5:8),listDown(5:8))];
                   if listCorri(1)>0.9
                       RTem=close(ii+1)/close(ii)-1.003;
                       Ri=[Ri,RTem];
                       indTarget=[indTarget,[ii;ii+1]];
                       Target=[Target,[close(ii);close(ii+1)]];
                       Days=Days+1;
                       listCorr=[listCorr;listCorri];  
                       if close(ii+1)-open(ii+1)>=(high(ii)-low(ii))*1.1
                           RTem=close(ii+2)/close(ii)-1.003;
                           Ri(end)=RTem;
                           indTarget(end)=ii+2;
                           Target(end)=close(ii+2);
                           Days=Days+1;
                           Radd=[Radd,close(ii+2)/close(ii+1)-1.003];
                           DaysAdd=DaysAdd+1; 
                       end                                       
                         
%                         if RTem>0
%                             RTem=close(ii+2)/close(ii)-1.002;
%                             Ri(end)=RTem;
%                             indTarget(end)=ii+2;
%                             Target(end)=close(ii+2);
%                         end
                   end
                end
                
                
%                 if low(ii-4)<=min(low(ii-10:ii)) &&high(ii)<max(high(ii-3:ii-2))&&...                               % % Orders:941; IR:0.5026; winRatio(ratioWL):69.71%(2.05);
%                         low(ii-4)<low(ii-3)&&low(ii-1)<low(ii-2)&&close(ii)>close(ii-1)*1.03 &&...               %     % % maxDraw:14.75%; profitP/profitPperDay: 2.0073%/1.7538%
%                         close(ii)>=low(ii)+(high(ii)-low(ii))*0.8 && close(ii)/close(ii-1)<1.09     
%                    listUp=[low(ii-4),open(ii-4),close(ii-4),high(ii-4),low(ii-3),open(ii-3),close(ii-3),high(ii-3)];                                 
%                    listDown=[low(ii-1),close(ii-1),open(ii-1),high(ii-1),low(ii-2),close(ii-2),open(ii-2),high(ii-2)];
%                    listCorri=[corr2(listUp(1:4),listDown(1:4)),corr2(listUp(5:8),listDown(5:8))];
%                    if listCorri(1)>0.85&&listCorri(2)>0.85
%                        RTem=close(ii+1)/close(ii)-1.003;
%                        Ri=[Ri,RTem];
%                        indTarget=[indTarget,[ii;ii+1]];
%                        Target=[Target,[close(ii);close(ii+1)]];
%                        Days=Days+1;
%                        listCorr=[listCorr;listCorri];   
%                        
%                        if close(ii+1)-open(ii+1)>=(high(ii)-low(ii))
%                            RTem=close(ii+2)/close(ii)-1.003;
%                            Ri(end)=RTem;
%                            indTarget(end)=ii+2;
%                            Target(end)=close(ii+2);
%                            Days=Days+1;
%                            Radd=[Radd,close(ii+2)/close(ii+1)-1.003];
%                            DaysAdd=DaysAdd+1;
% 
%                        end
%                        
% %                        stopP=low(ii);% stop loss
% %                        if low(ii+1)<=stopP
% %                            if open(ii+1)<stopP
% %                                stopP=open(ii+1);
% %                            end
% %                            RTem=stopP/close(ii)-1.002;
% %                            Ri(end)=RTem;
% %                            indTarget(end)=ii+1;
% %                            Target(end)=stopP;
% %                        end
%                        
%                    end
%                 end
            case 6 
                if low(ii-5)<=min(low(ii-10:ii))&&high(ii)<max(high(ii-3:ii-2))
                    Tem=[high(ii-5:ii-3),low(ii-5:ii-3)];     % % Orders:959; IR:0.4839; winRatio(ratioWL):67.05%(2.03);
                    Tem=Tem(2:end,:)-Tem(1:end-1,:);        %     % maxDraw:18.00%; profitP/profitPperDay: 2.2462%/2.0516%
                    Tem=sum(Tem>=0);                      %         %
                    highL=Tem(1);
                    lowL=Tem(2);
                    Tem=low(ii-2:ii);
                    Tem=Tem(2:end)-Tem(1:end-1);
                    Tem=sum(Tem<=0);
                    lowR=Tem;

                    if highL==2&&lowL==2&&lowR==2&&high(ii-2)>=high(ii-1)&&close(ii)>close(ii-1)*1.02&&close(ii-5)>open(ii-5)&&...                
                            close(ii)/close(ii-1)<1.09 % for current bar   %close(ii)>=low(ii)+(high(ii)-low(ii))*0.5 &&
                        listUp=[low(ii-5),open(ii-5),close(ii-5),high(ii-5),low(ii-4),open(ii-4),close(ii-4),high(ii-4),low(ii-3),open(ii-3),close(ii-3),high(ii-3)];
                        listDown=[low(ii),close(ii),open(ii),high(ii),low(ii-1),close(ii-1),open(ii-1),high(ii-1),low(ii-2),close(ii-2),open(ii-2),high(ii-2)];
                        listCorri=[corr2(listUp(1:4),listDown(1:4)),corr2(listUp(5:8),listDown(5:8)),corr2(listUp(9:12),listDown(9:12))];
                        if listCorri(3)<0.93
                            daysHold=1;
                            RTem=close(ii+daysHold)/close(ii)-1.003;
                            Ri=[Ri,RTem];
                            indTarget=[indTarget,[ii;ii+daysHold]];
                            Target=[Target,[close(ii);close(ii+daysHold)]];
                            Days=Days+daysHold;
                            listCorr=[listCorr;listCorri];
                            
                            if  close(ii+1)>=low(ii+1)+(high(ii+1)-low(ii+1))*0.9&&close(ii+1)>close(ii)*1.03
                                    RTem=close(ii+2)/close(ii)-1.003;
                                    Ri(end)=RTem;
                                    indTarget(end)=ii+2;
                                    Target(end)=close(ii+2);
                                    Days=Days+1;
                                    Radd=[Radd,close(ii+2)/close(ii+1)-1.003];
                                    DaysAdd=DaysAdd+1;
                            end    
                        end                
                    end
                end
        end
    end
    if ~isempty(Ri)
        Rall=[Rall,Ri];
        namesRall=[namesRall,stocks(i)];
    end
    
    if fig
        numberFig=size(indTarget,2);
        for i2=1:numberFig
            figure;
            ax1=subplot(3,1,1:2);
            figStart=indTarget(1,i2)-10;
            candle(high(figStart:figStart+20),low(figStart:figStart+20),close(figStart:figStart+20),open(figStart:figStart+20));
            listCorrStr=sprintf('%.3f ',listCorr(i2,:));
            title(strcat(stocks(i),';listCorr: ',listCorrStr));
            grid on;
            hold on;
            lowTem=low(figStart:figStart+20);
            indTem=[11;11+indTarget(2,i2)-indTarget(1,i2)];
            line(indTem,Target(:,i2),'color','r');
            plot(indTem(1,:),lowTem(indTem(1,:)),'r*');
            plot(indTem(2,:),lowTem(indTem(2,:)),'k*');
            try
                indAddTem=indAdd{i2}+11;
                AddTem=Add{i2};                
                line(indAddTem,AddTem,'color','b');
                plot(indAddTem(1,:),lowTem(indAddTem(1,:)),'b*');
            end
            ax2=subplot(3,1,3);
            bar(vol(figStart:figStart+20));
            grid on;
            linkaxes([ax1,ax2],'x');   
        end
    end
end
R=[Rall{:}];%planish Rall;
if ~isempty(R)
    statisticTrading(R,Days);
end
if ~isempty(Radd)
    statisticTrading(Radd,DaysAdd);
end
toc;
end

function statisticTrading(R,Days)
Lt=length(R);
IR=mean(R)/std(R);
winRatio=sum(R>0)/Lt;
ratioWL=-mean(R(R>0))/mean(R(R<0));
R=cumsum(R);
maxDraw=0;
indDraw=0;
pointDraw=0;
for i=2:Lt
    drawTem=max(R(1:i))-R(i);
    if drawTem>maxDraw
        maxDraw=drawTem;
        indDraw=i;
        pointDraw=R(i);
    end
end
figure;
plot(R);
try
    hold on;
    plot(indDraw,pointDraw,'r*')
end
strTitle=sprintf('Orders:%d; IR:%.4f; winRatio(ratioWL):%.2f%%(%.2f);\nmaxDraw:%.2f%%; profitP/profitPperDay: %.4f%%/%.4f%%'...
    ,Lt,IR,winRatio*100,ratioWL,maxDraw*100,R(end)*100/length(R),R(end)*100/Days)
title(strTitle);
grid on;
end


