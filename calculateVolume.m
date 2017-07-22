% 该指标需要用到三个标的，分别是期货future,期权optionBuy和optionSell;这三个标的可变；最后做出一个bar图；matlab代码如下：
w=windmatlab; 
future='IH1706.CFE';
optionBuy='10000821.sh';
optionSell='10000822.sh';
vol=w.wsi([future,',',optionBuy,',',optionSell],'volume','2017-05-18 09:30:00','2017-05-18 15:01:00','periodstart=09:30:00;periodend=15:01:00');
oneV=size(vol,1)/3;
vol=cell2mat(vol(:,3));
F=vol(1:oneV);
O1=vol(oneV+1:oneV*2)*30;
O2=vol(oneV*2+1:end)*30;
totalV=F+O1+O2;
bar(totalV);
