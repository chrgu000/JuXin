function ArbitrageOF50ETF(option1,option2) % ih1705.cfe 新湖期货：16808015 期货市场监控中心账号020916808015 初始密码8990DUUm；咨询电话4008888398
%% code for trading for days; 10000829.sh 10000830.sh ih1706.cfe
% tic;
% w=windmatlab;
% optionInf=w.wss(option1,'exe_mode,exe_price,startdate,lasttradingdate');
% optionChe=w.wss(option2,'exe_mode,exe_price,startdate,lasttradingdate');
% if isequal(optionInf{2},optionChe{2}) &&... %isequal(abs(optionInf{1}),[35748,36141])
%         strcmp(optionInf{3},optionChe{3}) && strcmp(optionInf{4},optionChe{4})
%     if strcmp(optionInf(1),'认购') && strcmp(optionChe(1),'认沽')
%     elseif strcmp(optionInf(1),'认沽') && strcmp(optionChe(1),'认购')
%         tem=option1;
%         option1=option2;
%         option2=tem;
%     end
% else
%     display([option1,' and ',option2,' do not fit each other for this arbitrage portfolio']);
%     return;
% end
% 
% price=optionInf{2};
% future=['IH',datestr(optionInf(4),'yymm'),'.cfe'];
% startT=datestr(optionInf(3),'yyyy-mm-dd');
% endT=datestr(optionInf(4),'yyyy-mm-dd');
% [OP1,~,~,Time1]=w.wsi(option1,'open,close',startT,endT,'periodstart=09:30:00;periodend=15:00:00');%;PriceAdj=F
% [OP2,~,~,Time2]=w.wsi(option2,'open,close',startT,endT,'periodstart=09:30:00;periodend=15:00:00');
% [IH,~,~,Time3]=w.wsi(future,'open,close',startT,endT,'periodstart=09:30:00;periodend=15:00:00');
% [etf50,~,~,Time4]=w.wsi('510050.sh','open,close',startT,endT,'periodstart=09:30:00;periodend=15:00:00');
% [index50,~,~,Time5]=w.wsi('000016.sh','open,close',startT,endT,'periodstart=09:30:00;periodend=15:00:00');
% indTem=~isnan(OP1(:,1));
% OP1=OP1(indTem,:);
% Time1=Time1(indTem);
% indTem=~isnan(OP2(:,1));
% OP2=OP2(indTem,:);
% Time2=Time2(indTem);
% indTem=~isnan(IH(:,1));
% IH=IH(indTem,:);
% Time3=Time3(indTem);
% % indNan=isnan(OP1(:,1));
% % TimeTem=Time1(indNan);
% % for i=length(TimeTem):-1:1
% %     indTem=find(Time1==TimeTem(i));
% %     indAdd=find(floor(Time1(indTem+1:end))==floor(TimeTem(i)),1);
% %     OP1(indTem,:)=OP1(indTem+indAdd,:);
% % end
% % indNan=isnan(OP2(:,1));
% % TimeTem=Time2(indNan);
% % for i=length(TimeTem):-1:1
% %     indTem=find(Time2==TimeTem(i));
% %     indAdd=find(floor(Time2(indTem+1:end))==floor(TimeTem(i)),1);
% %     OP2(indTem,:)=OP2(indTem+indAdd,:);
% % end
% 
% % for i=1:length(OP1(:,1))
% %     if isnan(OP1(i))
% %         followP=OP1(i:end,1);
% %         realP=followP(~isnan(followP));
% %         OP1(i,1)=realP(1);
% %         followP=OP1(i:end,2);
% %         realP=followP(~isnan(followP));
% %         OP1(i,2)=realP(1);
% %     end
% % end
% % for i=1:length(OP2(:,1))
% %     if isnan(OP2(i))
% %         followP=OP2(i:end,1);
% %         realP=followP(~isnan(followP));
% %         OP2(i,1)=realP(1);
% %         followP=OP2(i:end,2);
% %         realP=followP(~isnan(followP));
% %         OP2(i,2)=realP(1);
% %     end
% % end
% [Time12,~,~]=intersect(Time1,Time2);
% [Time,~,ind3]=intersect(Time12,Time3);
% IH=IH(ind3,:);
% [~,~,ind1]=intersect(Time,Time1);
% OP1=OP1(ind1,:);
% [~,~,ind2]=intersect(Time,Time2);
% OP2=OP2(ind2,:);
% [~,~,ind4]=intersect(Time,Time4);
% etf50=etf50(ind4,:);
% [~,~,ind5]=intersect(Time,Time5);
% index50=index50(ind5,:);
% Time=floor(Time);
% 
% IH=IH*300;
% OP=(price+OP1-OP2-(etf50-index50/1000))*300000;
% diffOpen=OP(:,1)-IH(:,1);
% diffClose=OP(:,2)-IH(:,2);  
% 
% High=[];
% Low=[];
% Close=[];
% Open=[];
% Days=unique(Time);
% L=length(Days);
% for i=1:L
%     indTem=Time==Days(i);    
%     DOTem=diffOpen(indTem);
%     DCTem=diffClose(indTem);    
%     Open=[Open;DOTem(1)];
%     Close=[Close;DCTem(end)];
%     Low=[Low;min([DOTem;DCTem])];
%     High=[High;max([DOTem;DCTem])];
% end
% 
% figure;
% candle(High,Low,Close,Open);
% step=max(floor(L/12),1);
% set(gca,'xtick',1:step:L);
% set(gca,'xticklabel',cellstr(datestr(Days,'yyyy-mm-dd')));
% title(['期货-期权套利',' (',future(1:6),' - ',num2str(price),')'],'FontSize',16,'FontWeight','bold','Color','r');
% xlabel('时间','FontSize',12,'FontWeight','bold','Color','r');
% ylabel('套利空间（元）','FontSize',12,'FontWeight','bold','Color','r');
% grid on;
% toc;

%% code for trading for minutes;
% w=windmatlab;
% startT=[datestr(today-15,'yyyy-mm-dd'),' 09:00:00'];
% endT=[datestr(today-1,'yyyy-mm-dd'),' 15:01:00'];
% IH=w.wsi(future,'close',startT,endT,'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
% [QQdata,~,~,Time]=w.wsi(option,'close',startT,endT,'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
% L=length(Time);
% IH=IH(end-L+1:end)*300;
% if bos>0
%     QQ=(price+QQdata)*300000;
%     diff=IH-QQ;
% else
%     QQ=(price-QQdata)*300000;
%     diff=QQ-IH;
% end
% 
% % subplot(211);
% plot(diff);
% set(gca,'xtick',1:241:L);
% Date=cellstr(datestr(Time,'yyyy-mm-dd'));
% set(gca,'xticklabel',Date(1:241:L));
% title(['期货-期权 数据波动情况',' (',future,' - ',option,')'],'FontSize',16,'FontWeight','bold','Color','r');
% xlabel('时间','FontSize',12,'FontWeight','bold','Color','r');
% ylabel('套利空间（元）','FontSize',12,'FontWeight','bold','Color','r');
% grid on;
% % subplot(212);
% % diffS=abs(diff)-4090;
% % plot(diffS);
% % set(gca,'xtick',1:241:L);
% % set(gca,'xticklabel',Date(1:241:L));
% % title('套利盈亏情况');
% % grid on;
%% code for draw principle figures;
% figure;
% point1=2.1;
% point2=2.35;
% point3=2.6;
% pointsX=[point1,point2,point3];
% B1=-0.014;
% B2=B1;
% B3=B1+(point3-point2)*0.2;
% IH=2.3766;
% 
% subplot(122);
% S3=0.0104;
% S2=S3;
% S1=S3-(point2-point1)*0.2;
% plot(pointsX,[B1,B2,B3],'b--');
% hold on;
% plot(pointsX,[S1,S2,S3],'b--');
% plot(pointsX,[B1+S1,B2+S2,B3+S3],'b');
% IH1=(IH-point1)*0.2;
% IH2=0;
% IH3=(IH-point3)*0.2;
% plot([point1,point3],[IH1,IH3],'r');
% plot([point1,point3],[IH1+B1+S1,IH3+B3+S3],'k');
% set(gca,'Ytick',0);
% set(gca,'Xtick',pointsX);
% title('B:两张期权合约对冲一张期货合约');
% grid on;
% 
% subplot(121);
% plot(pointsX,[B1,B2,B3],'b');
% hold on;
% IH1=(IH-point1)*0.2;
% IH2=0;
% IH3=(IH-point3)*0.2;
% plot([point1,point3],[IH1,IH3],'r');
% plot(pointsX,[IH1+B1,(IH-point2)*0.2+B2,IH3+B3],'k');
% set(gca,'Ytick',0);
% set(gca,'Xtick',pointsX);
% title('A:一张期权合约对冲一张期货合约');
% xlabel('到期日价格');
% ylabel('到期日收益');
% grid on;
% 
% figure;
% subplot(121);
% plot(pointsX,[B1,B2,B3],'Color',[0.7,0.7,0.7]);
% hold on;
% plot([point1,point3],[IH1,IH3],'Color',[0.7,0.7,0.7]);
% plot(pointsX,[IH1+B1,(IH-point2)*0.2+B2,IH3+B3],'k');
% pointx=point2+(IH3+B3)/0.2;
% fill([point1,pointx,point1],[IH1+B1,0,0],'r','facealpha',0.5);
% fill([pointx,point3,point3,point2,pointx],[0,0,IH3+B3,IH3+B3,0],'g','facealpha',0.5);
% set(gca,'Ytick',0);
% set(gca,'Xtick',pointsX);
% title('A:一张期权合约对冲一张期货合约');
% xlabel('到期日价格');
% ylabel('到期日收益');
% grid on;
% subplot(122);
% plot(pointsX,[B1,B2,B3],'--','Color',[0.7,0.7,0.7]);
% hold on;
% plot(pointsX,[S1,S2,S3],'--','Color',[0.7,0.7,0.7]);
% plot(pointsX,[B1+S1,B2+S2,B3+S3],'Color',[0.7,0.7,0.7]);
% plot([point1,point3],[IH1,IH3],'Color',[0.7,0.7,0.7]);
% plot([point1,point3],[IH1+B1+S1,IH3+B3+S3],'k');
% fill([point1,point3,point3,point1],[IH1+B1+S1,IH1+B1+S1,0,0],'r','facealpha',0.5);
% set(gca,'Ytick',0);
% set(gca,'Xtick',pointsX);
% title('B:两张期权合约对冲一张期货合约');
% grid on;
end




