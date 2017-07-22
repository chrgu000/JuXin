function op=HedgeAB %op just for python call;
%% initiate 
dateStart='2015-01-01';
dateEnd=datestr(today-1,'yyyy-mm-dd');
op=0;
sw3A='WH.CZC';
sw3B='RI.CZC';
%% real procedure
sw1=0; % get data and save it in 'D:\Trading\HedgeAB.txt'
sw2=0; % show back-test performance pictures by sort from better ones;
sw3=1; % test sw3A and sw3B to confirm back-text result;
if sw1
    delete HedgeAB.txt % reprocessing data;
%     delete HedgeAB.mat %re-load data;
    try 
        load HedgeAB;
    catch
        w=windmatlab;
        data1=w.wset('sectorconstituent','sectorid=a599010101000000');
        data2=w.wset('sectorconstituent','sectorid=a599010201000000');
        data3=w.wset('sectorconstituent','sectorid=a599010301000000');
        data4=w.wset('sectorconstituent','sectorid=a599010401000000');
        futureTem=data1(:,2);
        for i=1:length(futureTem)
            futureTem{i}(end-7:end-4)='';
        end
        futuresF=unique(futureTem);
        futureTem=[data2(:,2);data3(:,2)];
        for i=1:length(futureTem)
            futureTem{i}(end-7:end-4)='';
        end
        futuresC=futureTem;
        futureTem=data4(:,2);
        for i=1:length(futureTem)
            futureTem{i}(end-6:end-4)='';
        end
        futuresC=unique([futuresC;futureTem]);
        [dataF,~,~,Dates]=w.wsd(futuresF,'close',dateStart,today-1);
        ratioF=dataF(2:end,:)./dataF(1:end-1,:)-1;
        Dates=Dates(2:end);
        Lc=length(futuresC);
        Lf=length(futuresF);
        ratios=ones(size(ratioF,1),Lc+Lf)*nan;
        for i=1:Lc
            fprintf([futuresC{i},': %.1f%%\n'],100*i/Lc);
%             display([futuresC{i},':',num2str(roundn(100*i/Lc,-1))]);
            while 1
                dataTem=w.wsi(futuresC(i),'close',[dateStart,' 09:00:00'],[dateEnd,' 15:01:00'],...
                    'BarSize=5;periodstart=09:00:00;periodend=15:01:00;Fill=Previous');
                if length(dataTem)>1
                    break;
                end
            end
            j=0; % for count;
            for ii=length(dataTem):-46:47
                ratios(end-j,i)=dataTem(ii)/dataTem(ii-45)-1;
                j=j+1;
            end    
        end
        ratios(:,Lc+1:end)=ratioF;
        futures=[futuresC;futuresF];    
        save HedgeAB ratios futures Dates;
    end
    L=length(futures);
    inds=nchoosek(1:L,2);
    for loop=1:size(inds,1)
        Aname=futures{inds(loop,1)};
        Bname=futures{inds(loop,2)};
        A=ratios(:,inds(loop,1));
        B=ratios(:,inds(loop,2));
        indAB=(~isnan(A)) & (~isnan(B));
        A=A(indAB);
        B=B(indAB);
        dateAB=Dates(indAB);
        Lloop=length(A);
        results1=[];
        results2=[];
        results3=[];
        results4=[];
        results5=[];
        for i=1:Lloop
            wd=weekday(dateAB(i))-1;
            switch wd
                case 1
                    results1=[results1,A(i)-B(i)];
                case 2
                    results2=[results2,A(i)-B(i)];
                case 3
                    results3=[results3,A(i)-B(i)];
                case 4
                    results4=[results4,A(i)-B(i)];
                case 5
                    results5=[results5,A(i)-B(i)];
            end       
        end    
        for i=1:5
            results=eval(['results',num2str(i)]);
            sharpe=mean(results)/std(results);
            winratio=sum(results>0)/length(results);
            if length(results)>28 
                if  winratio>0.49 && sharpe>0.15
                    y=cumsum(results);
                    Re=y(end);
                    ABname=[Aname,',',Bname];
                elseif winratio<0.51 && -sharpe>0.15
                    results=-results;
                    sharpe=mean(results)/std(results);
                    winratio=sum(results>0)/length(results);
                    y=cumsum(results);
                    Re=y(end);
                    ABname=[Bname,',',Aname];
                else
                    continue;
                end
                maxDown=0;
                for ii=2:length(y)
                    maxTem=max(y(1:ii))-y(ii);
                    if maxTem>maxDown
                        maxDown=maxTem;
                        maxInd=ii;
                    end
                end
                try
                    fprintf(fid,[ABname,',weekday:%d,winRatio:%.2f%%,return:%.1f%%,sharpe:%.3f,maxDown:%.1f%%,maxInd:%d\n'],...
                        i,winratio*100,Re*100,sharpe,maxDown*100,maxInd);
                    fprintf(fid,'%g ',y); %fprintf(fid,'%g\r\n ',y);
                    fprintf(fid,'\n');
                catch
                    fid=fopen('D:\Trading\HedgeAB.txt','at');
                    fprintf(fid,[ABname,',weekday:%d,winRatio:%.2f%%,return:%.1f%%,sharpe:%.3f,maxDown:%.1f%%,maxInd:%d\n'],...
                        i,winratio*100,Re*100,sharpe,maxDown*100,maxInd);
                    fprintf(fid,'%g ',y); %fprintf(fid,'%g\r\n ',y);
                    fprintf(fid,'\n');
                end 
            end
        end
        try
            fclose(fid);
        end       
    end
elseif sw2
    data=importdata('HedgeAB.txt');
    L=length(data);
    dataTem=regexp(data(1:2:L),',','split');
    wk1=[];
    wk2=[];
    wk3=[];
    wk4=[];
    wk5=[];
    shar1=[];
    shar2=[];
    shar3=[];
    shar4=[];
    shar5=[];
    for i=1:length(dataTem)
        wd=str2num(dataTem{i}{3}(end));
        shar=str2double(dataTem{i}{6}(8:end));
        switch wd
            case 1
                wk1=[wk1,(i-1)*2+1];
                shar1=[shar1,shar];
            case 2
                wk2=[wk2,(i-1)*2+1];
                shar2=[shar2,shar];
            case 3
                wk3=[wk3,(i-1)*2+1];
                shar3=[shar3,shar];
            case 4
                wk4=[wk4,(i-1)*2+1];
                shar4=[shar4,shar];
            case 5
                wk5=[wk5,(i-1)*2+1];
                shar5=[shar5,shar];
        end
    end
    for i=1:5
        indData=eval(['wk',num2str(i)]);
        shar=eval(['shar',num2str(i)]);
        [~,indTem]=sort(shar,'descend');
        indData=indData(indTem);
        dataTxt=data(indData);
        datay=data(indData+1);
        fi=1;
        for ii=1:length(dataTxt)/10
            txt=regexp(dataTxt(ii),',','split');
            y=regexp(datay(ii),' ','split');
            txt=txt{1};
            y=str2double(y{1});
            fim=mod(fi,6);
            if fim==0;
                fim=6;
            elseif fim==1
                figure;
                set(gcf,'position',[100,100,1800,900]);
            end
            subplot(2,3,fim);
            plot(y);
            hold on;
            title(strcat(txt(1),'-',txt(2),':',txt(3)));
            xlabel(strcat(txt{4:7}));
            maxInd=str2num(txt{end}(8:end));
            plot(maxInd,y(maxInd),'r*');
            grid on;  
            fi=fi+1;
        end       
    end
    op=fi-1;
elseif sw3
    w=windmatlab;
    Dates=w.tdays(dateStart,dateEnd);
    Dates=Dates(2:end);
    for i=1:2
        if i==1
            future=sw3A;
        else
            future=sw3B;
        end
        if strcmpi(future(end-2:end),'CFE')
            dataTem=w.wsd(future,'close',dateStart,today-1);
            ratioTem=dataTem(2:end)./dataTem(1:end-1)-1;
        else
            while 1
                dataTem=w.wsi(future,'close',[dateStart,' 09:00:00'],[dateEnd,' 15:01:00'],...
                    'BarSize=5;periodstart=09:00:00;periodend=15:01:00;Fill=Previous');
                if length(dataTem)>1
                    break;
                end
            end
            Lt=length(dataTem);
            ratioTem=[];
            for ii=47:46:Lt
                ratioTem=[ratioTem;dataTem(ii+45)/dataTem(ii)-1];
            end          
        end
        if i==1
            upRatioA=ratioTem;
        else
            upRatioB=ratioTem;
        end   
    end
    indTem=(~isnan(upRatioA))&(~isnan(upRatioB));
    upRatioA=upRatioA(indTem);
    upRatioB=upRatioB(indTem);
    Dates=Dates(indTem);
    results1=[];
    results2=[];
    results3=[];
    results4=[];
    results5=[];
    for i=1:length(Dates)
        wd=weekday(Dates(i))-1;
        switch wd
            case 1
                results1=[results1,upRatioA(i)-upRatioB(i)];
            case 2
                results2=[results2,upRatioA(i)-upRatioB(i)];
            case 3
                results3=[results3,upRatioA(i)-upRatioB(i)];
            case 4
                results4=[results4,upRatioA(i)-upRatioB(i)];
            case 5
                results5=[results5,upRatioA(i)-upRatioB(i)];
        end    
    end
    figure;
    set(gcf,'position',[100,100,1800,900]);
    for i=1:5
        subplot(2,3,i);
        results=eval(['results',num2str(i)]);
        sharpe=mean(results)/std(results);
        ABname=[sw3A,'-',sw3B,': '];
        winRatio=sum(results>0)/length(results);
        if sharpe<0
            sharpe=-sharpe;
            results=-results;
            ABname=[sw3B,'-',sw3A,': '];
            winRatio=sum(results>0)/length(results);
        end
        y=cumsum(results);
        plot(y);
        maxDown=0;
        for ii=2:length(y)
            maxTem=max(y(1:ii))-y(ii);
            if maxTem>maxDown
                maxDown=maxTem;
                maxInd=ii;
            end
        end
        hold on;
        plot(maxInd,y(maxInd),'r*');            
        title([ABname,'weekday',num2str(i)]);
        xlabel(['winRatio:',num2str(roundn(winRatio*100,-1)),'%',' sharpe:',num2str(roundn(sharpe,-4)),' maxDown:',num2str(roundn(maxDown*100,-2)),'%']);            
        grid on;
    end            
end
end



% function HedgeAB
% Aobj='ZN.SHF';
% Bobj='PB.SHF';
% try
%     load xy;
% catch
%     w=windmatlab;
%     [A,~,~,Date]=w.wsd(Aobj,'open,close','20140929',today-1);
%     B=w.wsd(Bobj,'open,close','20140929',today-1);
%     AOpen=A(:,1);
%     AClose=A(:,2);
%     BOpen=B(:,1);
%     BClose=B(:,2);
% end
% L=length(AOpen);
% results=zeros(1,L);
% plus=0;
% minus=0;
% for j=1:5
%     switch j
%         case 1
%             wk1=1;
%             wk2=0;
%             wk3=0;
%             wk4=0;
%             wk5=0;
%         case 2
%             wk1=0;
%             wk2=2;
%             wk3=0;
%             wk4=0;
%             wk5=0;
%         case 3
%             wk1=0;
%             wk2=0;
%             wk3=3;
%             wk4=0;
%             wk5=0;
%         case 4
%             wk1=0;
%             wk2=0;
%             wk3=0;
%             wk4=4;
%             wk5=0;
%         case 5
%             wk1=0;
%             wk2=0;
%             wk3=0;
%             wk4=0;
%             wk5=5;
%     end
%     for i=3:L  
%         temLast=BClose(i-1)/BClose(i-2)-AClose(i-1)/AClose(i-2);
%         tem=BClose(i)/BClose(i-1)-AClose(i)/AClose(i-1);
%         wd=weekday(Date(i))-1;
%         switch wd
%             case wk1  % hold status on monday;
%                 results(i)=tem;
%             case wk2
%                 results(i)=tem;
%             case wk3
%                 results(i)=-tem;
%             case wk4 
%                 results(i)=-tem;
%             case wk5
%                 results(i)=-tem;
%         end
%         if results(i)>0
%             plus=plus+1;
%         elseif results(i)<0
%             minus=minus+1;
%         end
%     end
% 
%     resultsCopy=results(results~=0);
%     y=cumsum(results);
%     maxDown=0;
%     for i=2:length(y)
%         maxTem=max(y(1:i))-y(i);
%         if maxTem>maxDown
%             maxDown=maxTem;
%             maxInd=i;
%         end
%     end
%     fprintf('winRatio: %.2f%%;return:%.3f;sharpe: %.3f; maxDown:%.1f%%\n',...
%         plus/(plus+minus)*100,y(end),mean(resultsCopy)/std(resultsCopy),maxDown*100);
%     figure;
%     [AX,H1,H2]=plotyy(1:L,[AClose,BClose*(max(AClose)/max(BClose))],1:L,y*100);%AX stand by two figures; H1 and H2 stand by two lines;
%     title('A和B多空完全对冲','fontsize',16);
%     xlabel('时间','fontsize',12);
%     set(AX(1),'xTick',1:20:L);
%     DateStr=datestr(Date,'yyyy-mm-dd');
%     dateTarget=mat2cell(DateStr,ones(size(DateStr,1),1),size(DateStr,2));
%     set(AX(1),'xTicklabel',dateTarget(1:20:L),'XTickLabelRotation',60);
%     set(get(AX(1),'ylabel'),'string','股指期货指数','fontsize',12);
%     set(get(AX(2),'ylabel'),'string','策略涨跌指数（%）','fontsize',12);
%     set(AX(2), 'YColor', 'r')
%     set(H2,'color','k');
%     legend('A连续','B连续','策略曲线','location','NorthOutside','Orientation','horizontal');
%     grid on;
%     axes(AX(2));
%     hold on;
%     plot(maxInd,y(maxInd)*100,'r*');
%     hold off;
% end
% end