 function op=ArbitrageOF50ETFAll(varargin) % ih1705.cfe 新湖期货：16808015 code:280018期货市场监控中心账号020916808015 初始密码8990DUUm；咨询电话4008888398
tic;
sw0=1;% show two trading targets' difference for history price;50etf-50index
sw1=0;% show all options-future K lines which are trading in the "date";
sw2=0;% get all options-future data in history; 
sw3=1;% show Pictures;
sw4=0;%code for draw principle figures;
test=0;% test odd portfolio;
%% show two trading targets' difference for history price;50etf-50index
if sw0
    w=windmatlab;
    target1='510050.SH'; %50etf
    target2='000016.SH'; %50index
    startT='2016-1-1';
    endT='2017-1-1';
    [etf50,~,~,Date]=w.wsd(target1,'close',startT,endT);
    index50=w.wsd(target2,'close',startT,endT);
    Diff=(etf50*1000-index50)*300;
    L=length(Date);
    
    dateTest=datestr(floor(mean(datenum({startT,endT}))),'yyyy-mm-dd');
    yearNow=str2num(datestr(dateTest,'yyyy'));
    LgetValue=sum(Date<=datenum([num2str(yearNow),'0501'],'yyyymmdd'));% get mean value from LgetValue dates;  
    
    dataTem=w.wset('indexconstituent',['date=',dateTest,';windcode=000016.SH']);
    stocks=dataTem(:,2);
    names=dataTem(:,3);
    weights=cell2mat(dataTem(:,4));
    dataTem=w.wss(stocks,'div_cashandstock,div_exdate',['rptDate=',num2str(yearNow-1),'1231']);
    cashEx=cell2mat(dataTem(:,1));
    DateEx=dataTem(:,2);
    indTem=~strcmp(DateEx,'0:00:00');
    stocks=stocks(indTem);
    names=names(indTem);
    weights=weights(indTem);
    DateEx=DateEx(indTem);
    cashEx=cashEx(indTem);
    exDates=datenum(DateEx,'yyyy/mm/dd');
    diffEx=zeros(L,1);
    LgetValue=sum(Date<=datenum([num2str(yearNow),'0501'],'yyyymmdd'));% get mean value from LgetValue dates;
    for i=LgetValue+1:L
        indTem=exDates==Date(i);
        stocksTem=stocks(indTem);
        weightsTem=weights(indTem);
        cashExTem=cashEx(indTem);
        exDatesTem=exDates(indTem);
        diffi=0;
        for ii=1:sum(indTem)
            sT=stocksTem{ii};
            eT=datestr(exDatesTem(ii),'yyyymmdd');
            wT=weightsTem(ii);
            cT=cashExTem(ii);
            dataTem=w.wss([sT,',',target2],'close',['tradeDate=',eT],'priceAdj=U','cycle=D');
            stockP=dataTem(1);
            indexP=dataTem(2);
            diffTem=indexP*cT/stockP*wT*3;
            if ~isnan(diffTem)
                diffi=diffi+diffTem;
            end         
        end
        diffEx(i)=diffi;        
    end           
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     Datestr=cellstr(datestr(Date,'yyyy-mm-dd'));
%     diffEx=zeros(L,1);
%     for i=LgetValue:L
%         display(i);
%         dateTest=Datestr{i};
%         dataTem=w.wset('indexconstituent',['date=',dateTest,';windcode=000016.SH']);
%         stocks=dataTem(:,2);
%         names=dataTem(:,3);
%         weights=cell2mat(dataTem(:,4));
%         yearNow=str2num(datestr(dateTest,'yyyy'));
%         dataTem=w.wss(stocks,'div_cashandstock,div_exdate',['rptDate=',num2str(yearNow-1),'1231']);
%         cashEx=cell2mat(dataTem(:,1));
%         DateEx=dataTem(:,2);
%         indTem=~strcmp(DateEx,'0:00:00');
%         stocks=stocks(indTem);
%         names=names(indTem);
%         weights=weights(indTem);
%         DateEx=DateEx(indTem);
%         cashEx=cashEx(indTem);
%         exDates=datenum(DateEx,'yyyy/mm/dd');
%         indTem=exDates>datenum([num2str(yearNow),'0501'],'yyyymmdd') & exDates<=datenum(dateTest,'yyyy-mm-dd');
%         stocks=stocks(indTem);
%         weights=weights(indTem);
%         DateEx=cellstr(datestr(exDates(indTem)-1,'yyyymmdd'));
%         cashEx=cashEx(indTem);
%         diff=0;
%         for i=1:length(stocks)
%             stock=stocks{i};
%             DateTem=DateEx{i};
%             weight=weights(i);
%             dataTem=w.wss([stock,',',target2],'close',['tradeDate=',DateTem],'priceAdj=U','cycle=D');
%             stockP=dataTem(1);
%             indexP=dataTem(2);
%             diffTem=indexP*cashEx(i)/stockP*weight*3;
%             if ~isnan(diffTem)
%                 diff=diff+diffTem;
%             end
%         end    
%         diffEx(i)=diff;
%     end

    diffEx(1)=mean(Diff(1:LgetValue));
    diffEx=cumsum(diffEx); 
    
    figure;
    set(gcf,'position',[100,100,1500,900])
    deltaDiff=diffEx-Diff;
    Ltem=sum(deltaDiff<7000);
%     plotyy(1:L,[Diff,diffEx],1:Ltem,deltaDiff(1:Ltem));
%     legend('50etf-50index','分红除权计算的Diff','DeltaDiff','location','northwest');
    [AX,h1,h2]=plotyy(1:L,[Diff,diffEx],1:L,zeros(1,L));
    set(h1,'linewidth',2);
    set(h2,'color','b');
    set(AX(1),'ylim',[min(Diff)*1.1,max(diffEx)*1.1]);
    set(AX(2),'ycolor','b');
%     axis(AX(2),[1,L,12000,40000]);    
%     set(AX(2),'ytick',12000:1000:40000)
    hT=legend('50etf-50index','分红除权计算的Diff','location','northoutside','orientation','horizontal');%
    set(hT,'fontsize',12);
    
    hold on;
    line([1,L],[0,0],'color','k');
    text(L+1,0,'y1-O线');
    step=ceil(L/30);
    indTem=1:step:L;
    if indTem(end)~=L
        indTem(end)=L;
    end
    set(gca,'xtick',indTem);
    set(gca,'xticklabel',cellstr(datestr(Date(indTem),'yyyy-mm-dd')),'xticklabelrotation',60);
    yMax=max([Diff;diffEx]);
    yMin=min([Diff;diffEx]);
    step=floor((yMax-yMin)/20);
    set(gca,'ytick',yMin:step:yMax);
    grid on;
    axes(AX(2));
    hold on;
    text(L+1,0,'y2-O线');
    
    files=dir('D:\Trading\OptionFuture\*.mat');
    files={files.name};
    L=length(files);
    monthSw0=[dateTest(3:4),'00'];
    indy2={};
    y2={};
    legends={};
    for i=1:L
        load(['D:\Trading\OptionFuture\',files{i}]);    
        if size(IH,1)<30
            continue;
        end
        if ~strcmp(monthSw0,titleName(3:6))
            monthSw0=titleName(3:6);
            IH=IH(:,1:2)*300;
            OP=(price+OP1(:,1:2)-OP2(:,1:2))*300000;
            diffClose=OP(:,2)-IH(:,2);  
            Close=[];
            Days=unique(Time);
            Ldays=length(Days);
            for ii=1:Ldays
                indTem=Time==Days(ii);    
                DCTem=diffClose(indTem);    
                Close=[Close;DCTem(end)];
            end  
            [~,indDay,indTem]=intersect(Days,Date);
            if length(indDay)>1
                indy2=[indy2,indTem];      
                y2=[y2,Close(indDay)];
                legends=[legends,titleName];
            end
        end  
    end 
    Lt=length(y2);
    aboveTem=0;
    belowTem=0;
    for i=1:Lt
        Tem=y2{i};
        if aboveTem<max(Tem)
            aboveTem=max(Tem);
        end
        if belowTem>min(Tem)
            belowTem=min(Tem);
        end
    end    
    aboveTem=aboveTem+abs(aboveTem/10);
    belowTem=belowTem-abs(belowTem/10);
    step=floor((aboveTem-belowTem)/12);
    set(AX(2),'ylim',[belowTem,aboveTem]);   
    set(AX(2),'ytick',belowTem:step:aboveTem);
    for i=1:Lt
        indTem=indy2{i};
        yTem=y2{i};
        plot(indTem,yTem,'-.');
    end
    legend(legends,'location','northwestoutside');
end
%% show all options-future K lines which are trading in the "date";
if sw1
    if nargin==0
        Date=datestr(today,'yyyy-mm-dd');
    elseif nargin==1
        Date=varargin{1};
    else
        display('Too many pararmeters!');
    end
    w=windmatlab;
    parameters=['date=',Date,';','us_code=510050.SH;option_var=全部;call_put=全部;field=option_code,strike_price,month,call_put,first_tradedate,last_tradedate,option_name'];
    data=w.wset('optionchain',parameters);
    options=data(:,1);
    prices=cell2mat(data(:,2));
    months=cell2mat(data(:,3));
    calls=data(:,4);
    starts=data(:,5);
    ends=data(:,6);
    names=data(:,7);
    Lopt=length(options);
    for i=1:Lopt
        names{i}=names{i}(end-4:end);
    end       
    LoptStr=num2str(Lopt-1);
    fi=1;
    for i=1:Lopt-1
        display(['i=',num2str(i),'/',LoptStr,'; ','Time: ',num2str(toc)]);
        price=prices(i);
        month=months(i);
        name=names(i);
        indTem=find((strcmp(names(i+1:end),name) & months(i+1:end)==month)==1,1)+i;
        if isempty(indTem)
            continue;
        else
            if strcmp(calls{i},'认购')
                option1=options(i);
                option2=options(indTem);
            else
                option1=options(indTem);
                option2=options(i);
            end
        end
        future=['IH',num2str(mod(month,10000)),'.cfe'];
        while 1
            [OP1,~,~,Time1]=w.wsi(option1,'open,close',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00');
            if size(OP1,1)>1 
                break;
            end
        end
        while 1
            [OP2,~,~,Time2]=w.wsi(option2,'open,close',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00');
            if size(OP2,1)>1 
                break;
            end
        end
        while 1
            [IH,~,~,Time3]=w.wsi(future,'open,close',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00');
            if size(IH,1)>1 
                break;
            end
        end
        while 1
            if datenum(ends(i),'yyyy/mm/dd') >datenum('20161130','yyyymmdd')
                [etf50,~,~,Time4]=w.wsi('510050.sh','open,close',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00;PriceAdj=F;Fill=Previous');
            else
                [etf50,~,~,Time4]=w.wsi('510050.sh','open,close',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00;Fill=Previous');
            end
            if size(etf50,1)>1 
                break;
            end
        end
        while 1
            [index50,~,~,Time5]=w.wsi('000016.sh','open,close',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00;Fill=Previous');
            if size(index50,1)>1 
                break;
            end
        end
        indTem=~isnan(OP1(:,1));
        OP1=OP1(indTem,:);
        Time1=Time1(indTem);
        indTem=~isnan(OP2(:,1));
        OP2=OP2(indTem,:);
        Time2=Time2(indTem);
        indTem=~isnan(IH(:,1));
        IH=IH(indTem,:);
        Time3=Time3(indTem);   
        [Time12,~,~]=intersect(Time1,Time2);
        [Time,~,ind3]=intersect(Time12,Time3);
        IH=IH(ind3,:);
        [~,~,ind1]=intersect(Time,Time1);
        OP1=OP1(ind1,:);
        [~,~,ind2]=intersect(Time,Time2);         
        OP2=OP2(ind2,:);
        [~,~,ind4]=intersect(Time,Time4);         
        etf50=etf50(ind4,:);
        [~,~,ind5]=intersect(Time,Time5);         
        index50=index50(ind5,:); 
        Time=floor(Time); 

        IH=IH*300;
%         OP=(price+OP1-OP2-(etf50-index50/1000))*300000;
        OP=(price+OP1-OP2)*300000;
        diffOpen=OP(:,1)-IH(:,1);
        diffClose=OP(:,2)-IH(:,2);  
        High=[];
        Low=[];
        Close=[];
        Open=[];
        Days=unique(Time);
        Ldays=length(Days);
        for ii=1:Ldays
            indTem=Time==Days(ii);    
            DOTem=diffOpen(indTem);
            DCTem=diffClose(indTem);    
            Open=[Open;DOTem(1)];
            Close=[Close;DCTem(end)];
            Low=[Low;min([DOTem;DCTem])];
            High=[High;max([DOTem;DCTem])];
        end
        fTem=mod(fi,6);
        if fTem==1
            figure;
            set(gcf,'position',[100,100,1800,900]);
        elseif fTem==0
            fTem=6;
        end
        subplot(2,3,fTem);
        candle(High,Low,Close,Open);
        step=max(floor(Ldays/4),1);
        set(gca,'xtick',1:step:Ldays);
        set(gca,'xticklabel',cellstr(datestr(Days(1:step:Ldays),'yyyy-mm-dd')));
        title(['期货-期权套利',' (',future(1:6),' - ',num2str(price),')'],'FontSize',16,'FontWeight','bold','Color','r');
        xlabel('时间','FontSize',12,'FontWeight','bold','Color','r');
        ylabel('套利空间（元）','FontSize',12,'FontWeight','bold','Color','r');
        text(Ldays,min(Low),option1);
        text(Ldays,max(High),option2);
        grid on;
        fi=fi+1;
    end
end
%% get all options-future data in history; 
if sw2
    w=windmatlab;
    loops=ceil((today-datenum(2015,2,9))/29);
    year=2015;
    month=1;
    monthTem=1;
    day=28;
    Data=[];% store data for all options;
    for j=1:loops
        if monthTem==12
            year=year+1;
        end
        month=month+1;
        monthTem=mod(month,12);
        if monthTem==0
            monthTem=12;
        end
        Date=datenum(year,monthTem,day);
        if Date >today
            Date=today;
        end    
        parameters=['date=',datestr(Date,'yyyy-mm-dd'),';','us_code=510050.SH;option_var=全部;',...
            'call_put=全部;field=option_code,strike_price,month,call_put,first_tradedate,last_tradedate,option_name'];
        data=w.wset('optionchain',parameters);
        Data=[Data;data];
        if Date==today
            break;
        end       
    end
    options=Data(:,1);
    [options,indTem]=unique(options);
    Data=Data(indTem,:);
    prices=cell2mat(Data(:,2));
    months=cell2mat(Data(:,3));
    calls=Data(:,4);
    starts=Data(:,5);
    ends=Data(:,6);
    names=Data(:,7);
    Lopt=length(options);
    for i=1:Lopt
        names{i}=names{i}(end-4:end);
    end  
    LoptStr=num2str(Lopt-1);
    for i=1:Lopt-1
        price=prices(i);
        month=months(i);
        name=names(i);
        indTem=find((strcmp(names(i+1:end),name) & months(i+1:end)==month)==1,1)+i;
        if isempty(indTem)
            continue;
        else
            if strcmp(calls{i},'认购')
                option1=options(i);
                option2=options(indTem);
            else
                option1=options(indTem);
                option2=options(i);
            end
        end
        future=['IH',num2str(mod(month,10000)),'.cfe'];
        [OP1,~,~,Time1]=w.wsi(option1,'open,close,volume',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00');%;
        [OP2,~,~,Time2]=w.wsi(option2,'open,close,volume',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00');
        [IH,~,~,Time3]=w.wsi(future,'open,close,volume',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00');
        if datenum(ends(i))>datenum('2016-11-29') %50etf期权除权日
            [etf50,~,~,Time4]=w.wsi('510050.sh','open,close',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00;PriceAdj=F;Fill=Previous');
        else
            [etf50,~,~,Time4]=w.wsi('510050.sh','open,close',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00;Fill=Previous');
        end        
        [index50,~,~,Time5]=w.wsi('000016.sh','open,close',starts(i),ends(i),'periodstart=09:30:00;periodend=15:00:00;Fill=Previous');
        indTem=~isnan(OP1(:,1));
        OP1=OP1(indTem,:);
        Time1=Time1(indTem);
        indTem=~isnan(OP2(:,1));
        OP2=OP2(indTem,:);
        Time2=Time2(indTem);
        indTem=~isnan(IH(:,1));
        IH=IH(indTem,:);
        Time3=Time3(indTem);   
        [Time12,~,~]=intersect(Time1,Time2);
        [Time,~,ind3]=intersect(Time12,Time3);
        IH=IH(ind3,:);
        [~,~,ind1]=intersect(Time,Time1);
        OP1=OP1(ind1,:);
        [~,~,ind2]=intersect(Time,Time2);         
        OP2=OP2(ind2,:);
        [~,~,ind4]=intersect(Time,Time4);         
        etf50=etf50(ind4,:);
        [~,~,ind5]=intersect(Time,Time5);         
        index50=index50(ind5,:); 
        Time=floor(Time); 
        titleName=[future(1:6),'-',num2str(price)];    
        tem=['D:\Trading\OptionFuture\',titleName,'.mat'];
        save(tem,'price','OP1','OP2','IH','etf50','index50','Time','titleName','option1','option2');
        display(['i=',num2str(i),'/',LoptStr,' --',titleName,': ',num2str(toc),' seconds.']);
    end
end
%% show Pictures;
if sw3
    files=dir('D:\Trading\OptionFuture\*.mat');
    files={files.name};
    L=length(files);
    fi=1;
    for i=1:L
        load(['D:\Trading\OptionFuture\',files{i}]);    
        IH=IH(:,1:2)*300;
%         OP=(price+OP1(:,1:2)-OP2(:,1:2)-(etf50-index50/1000))*300000;
        OP=(price+OP1(:,1:2)-OP2(:,1:2))*300000;
        diffOpen=OP(:,1)-IH(:,1);
        diffClose=OP(:,2)-IH(:,2);  
        High=[];
        Low=[];
        Close=[];
        Open=[];
        Days=unique(Time);
        Ldays=length(Days);
        if Ldays>50 || Ldays<10
            continue;
        end
        for ii=1:Ldays
            indTem=Time==Days(ii);    
            DOTem=diffOpen(indTem);
            DCTem=diffClose(indTem);    
            Open=[Open;DOTem(1)];
            Close=[Close;DCTem(end)];
            Low=[Low;min([DOTem;DCTem])];
            High=[High;max([DOTem;DCTem])];
        end
        fTem=mod(fi,6);
        if fTem==1
            figure;
            set(gcf,'position',[100,100,1800,900]);
        elseif fTem==0
            fTem=6;
        end
        average=[];
        for ii=10:Ldays
            average=[average;mean(Close(ii-9:ii))];
        end
        try
            subplot(2,3,fTem);
            plot(10:Ldays,average);
            hold on;
            candle(High,Low,Close,Open);
            step=max(ceil(Ldays/12),1);
            set(gca,'xtick',1:step:Ldays);
            set(gca,'xticklabel',cellstr(datestr(Days(1:step:Ldays),'yyyy-mm-dd')),'XTickLabelRotation',60);
            title(['期货-期权套利',' (',titleName,')'],'FontSize',16,'FontWeight','bold','Color','r');
            xlabel('时间','FontSize',12,'FontWeight','bold','Color','r');
            ylabel('套利空间（元）','FontSize',12,'FontWeight','bold','Color','r');
            text(Ldays+1,min(Low),option1);
            text(Ldays+1,max(High),option2);
%             text(1,Low(1),num2str(Open(1)));
%             text(1,High(1),num2str(Close(Ldays)))
%             text(1,max(High),num2str(fi));
            grid on;
            fi=fi+1;
        end
    end
end
%% code for draw principle figures;
if sw4
    figure;
    point1=2.1;
    point2=2.35;
    point3=2.6;
    pointsX=[point1,point2,point3];
    B1=-0.014;
    B2=B1;
    B3=B1+(point3-point2)*0.2;
    IH=2.3766;

    subplot(122);
    S3=0.0104;
    S2=S3;
    S1=S3-(point2-point1)*0.2;
    plot(pointsX,[B1,B2,B3],'b--');
    hold on;
    plot(pointsX,[S1,S2,S3],'b--');
    plot(pointsX,[B1+S1,B2+S2,B3+S3],'b');
    IH1=(IH-point1)*0.2;
    IH2=0;
    IH3=(IH-point3)*0.2;
    plot([point1,point3],[IH1,IH3],'r');
    plot([point1,point3],[IH1+B1+S1,IH3+B3+S3],'k');
    set(gca,'Ytick',0);
    set(gca,'Xtick',pointsX);
    title('B:两张期权合约对冲一张期货合约');
    grid on;

    subplot(121);
    plot(pointsX,[B1,B2,B3],'b');
    hold on;
    IH1=(IH-point1)*0.2;
    IH2=0;
    IH3=(IH-point3)*0.2;
    plot([point1,point3],[IH1,IH3],'r');
    plot(pointsX,[IH1+B1,(IH-point2)*0.2+B2,IH3+B3],'k');
    set(gca,'Ytick',0);
    set(gca,'Xtick',pointsX);
    title('A:一张期权合约对冲一张期货合约');
    xlabel('到期日价格');
    ylabel('到期日收益');
    grid on;

    figure;
    subplot(121);
    plot(pointsX,[B1,B2,B3],'Color',[0.7,0.7,0.7]);
    hold on;
    plot([point1,point3],[IH1,IH3],'Color',[0.7,0.7,0.7]);
    plot(pointsX,[IH1+B1,(IH-point2)*0.2+B2,IH3+B3],'k');
    pointx=point2+(IH3+B3)/0.2;
    fill([point1,pointx,point1],[IH1+B1,0,0],'r','facealpha',0.5);
    fill([pointx,point3,point3,point2,pointx],[0,0,IH3+B3,IH3+B3,0],'g','facealpha',0.5);
    set(gca,'Ytick',0);
    set(gca,'Xtick',pointsX);
    title('A:一张期权合约对冲一张期货合约');
    xlabel('到期日价格');
    ylabel('到期日收益');
    grid on;
    subplot(122);
    plot(pointsX,[B1,B2,B3],'--','Color',[0.7,0.7,0.7]);
    hold on;
    plot(pointsX,[S1,S2,S3],'--','Color',[0.7,0.7,0.7]);
    plot(pointsX,[B1+S1,B2+S2,B3+S3],'Color',[0.7,0.7,0.7]);
    plot([point1,point3],[IH1,IH3],'Color',[0.7,0.7,0.7]);
    plot([point1,point3],[IH1+B1+S1,IH3+B3+S3],'k');
    fill([point1,point3,point3,point1],[IH1+B1+S1,IH1+B1+S1,0,0],'r','facealpha',0.5);
    set(gca,'Ytick',0);
    set(gca,'Xtick',pointsX);
    title('B:两张期权合约对冲一张期货合约');
    grid on;
end
%% test some odd arbitrage portfolio;
if test
    option1='10000646.sh';
    option2='10000651.sh';
    future='IH1608.cfe';
    portfolio='IH1608-2.05.mat';
    w=windmatlab;
    Date=w.wss(option1,'startdate,lasttradingdate');
    startT=Date(1);
    endT=Date(2);
    [Data1,~,~,Date1]=w.wsd(option1,'high,low,close,open',startT,endT);
    Data2=w.wsd(option2,'high,low,close,open',startT,endT);
    [Data3,~,~,Date3]=w.wsd(future,'high,low,close,open',startT,endT);
    indTem=~isnan(Data3(:,1));
    Data3=Data3(indTem,:);
    Date3=Date3(indTem);
    figure;
    set(gcf,'position',[100,100,1800,900]);
    subplot(2,2,1);
    candle(Data1(:,1),Data1(:,2),Data1(:,3),Data1(:,4));
    text(length(Data1(:,1))+3,min(Data1(:,2)),datestr(Date1(end),'yyyy-mm-dd'));
    grid on;
    subplot(2,2,2);
    candle(Data2(:,1),Data2(:,2),Data2(:,3),Data2(:,4));
    text(length(Data2(:,1))+3,min(Data2(:,2)),datestr(Date1(end),'yyyy-mm-dd'));
    grid on;
    subplot(2,2,3);
    candle(Data3(:,1),Data3(:,2),Data3(:,3),Data3(:,4));
    text(length(Data3(:,1))+3,min(Data3(:,2)),datestr(Date3(end),'yyyy-mm-dd'));
    grid on;
    subplot(2,2,4);
    load(['D:\Trading\OptionFuture\',portfolio]);    
    IH=IH*300;
    OP=(price+OP1-OP2)*300000;
    diffOpen=OP(:,1)-IH(:,1);
    diffClose=OP(:,2)-IH(:,2);  
    High=[];
    Low=[];
    Close=[];
    Open=[];
    Days=unique(Time);
    Ldays=length(Days);
    for ii=1:Ldays
        indTem=Time==Days(ii);    
        DOTem=diffOpen(indTem);
        DCTem=diffClose(indTem);    
        Open=[Open;DOTem(1)];
        Close=[Close;DCTem(end)];
        Low=[Low;min([DOTem;DCTem])];
        High=[High;max([DOTem;DCTem])];
    end
    candle(High,Low,Close,Open);
    step=max(ceil(Ldays/4),1);
    set(gca,'xtick',1:step:Ldays);
    set(gca,'xticklabel',cellstr(datestr(Days(1:step:Ldays),'yyyy-mm-dd')));
    title(['期货-期权套利',' (',titleName,')'],'FontSize',16,'FontWeight','bold','Color','r');
    xlabel('时间','FontSize',12,'FontWeight','bold','Color','r');
    ylabel('套利空间（元）','FontSize',12,'FontWeight','bold','Color','r');
    text(Ldays+1,min(Low),option1);
    text(Ldays+1,max(High),option2);
    grid on;
end

op=toc;
end
