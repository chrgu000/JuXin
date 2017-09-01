function [cost,margin]=ArbitrageCostMargin(option1,option2)%option1为认购，option2为认沽;
w=windmatlab;
Tem=w.wss(option1,'lasttradingdate,exe_price');
future=['IH',datestr(Tem(1),'yymm'),'.cfe'];
data=w.wsq([option1,',',option2,',',future],'rt_latest');
arbitrageP=(Tem{2}+data(1)-data(2))*300000-data(3)*300;
cost1=-abs(arbitrageP)+876+data(3)*151.8/10000;
cost2=-abs(arbitrageP)+876+data(3)*6072/10000;
cost=[cost1,cost2];
display('套利组合价格转换为建仓时为负值，则盈利计算公式为：平仓时套利组合价格-建仓时套利组合价格；');
display(['若非当日平仓，则套利组合成本价格：',num2str(cost1),';','否则，成本价格：',num2str(cost2)]);
if arbitrageP >0
    margin=data(3)*300*0.21+w.wss(option1,'maint_margin')*30; 
else
    margin=data(3)*300*0.21+w.wss(option2,'maint_margin')*30;
end
display(['所需基本保证金为：',num2str(margin)]);
end