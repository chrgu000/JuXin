function pltyy
% x1=[6:2:18];
% y1=[0.55,0.67,0.68,0.72,0.72,0.71,0.77];
% x2=[2:2:24];
% y2=[0.08,0.12,0.12,0.2,0.21,0.23,0.19,0.2,0.21,0.23,0.23,0.24];
% x3=[2:2:14];
% y3=[0,0,0.04,0.04,0.05,0.05,0.05];
% figure;
% H1=axes;
% L(1)=plot(H1,x1,y1,'r','linewidth',2);
% hold on
% grid on
% set(H1,'xlim',[0,25],'xtick',[0:2:24,25]);
% set(H1,'ylim',[0,0.8]);%set(gca,'ylim',[0,0.8])
% xlabel('Time /h','fontweight','bold','fontsize',12);
% ylabel('1st/2nd--CS Ratio of Dry (%)','fontweight','bold','fontsize',12);
% title('CS Out Ratio according to Time');
% L(2)=plot(H1,x2,y2,'g','linewidth',2);
% plot(H1,x1,y1,'k*');
% plot(H1,x2,y2,'k*');
% H2=axes;
% hold on;
% L(3)=plot(H2,x3,y3,'b','linewidth',2);
% plot(H2,x3,y3,'k*')
% set(H2,'color','none'); %axes(H1) can switch to axes H1;
% set(H2,'xlim',[0,25],'xtick',[])
% set(H2,'ylim',[-0.045,0.115],'ytick',-0.045:0.02:0.115);
% set(H2,'yaxislocation','right');
% ylabel('3rd--CS Ratio of Dry (%)','fontweight','bold','fontsize',12)
% legend(L,{'1st','2nd','3rd'})
figure;
x1=[2:2:8,24];
x2=2:2:22;
y1=[0.09,0.11,0.11;0.12,0.13,0.12;0.13,0.14,0.17;0.14,0.15,0.18;0.18,0.18,0.21];
y2=[0.11,0.13,0.16,0.17,0.18,0.21,0.22,0.24,0.24,0.24,0.23];
L(1:3)=plot(x1',y1,'r','linewidth',2);
hold on;
grid on;
plot(x1',y1,'k*');
set(gca,'xlim',[0,25],'xtick',[0:2:24,25],'ylim',[0.08,0.25]);
L(4)=plot(x2,y2,'g','linewidth',2);
plot(x2,y2,'k*');
legend(L([1,4]),{'xx','xx2'});
























