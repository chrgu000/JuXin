function prepareCNE5Value=PrepareCNE5
replyTem=input('update data or not? y/n [n]:','s');
if ~isempty(replyTem)&&(replyTem=='y'||strcmp(replyTem,'yes'))
    h=waitbar(0,'开始计算PrepareCNE5...');
    BetaX;
    waitbar(0.1233,h,'PrepareCNE5已完成...12.33%');
    MomentumX;
    waitbar(0.4623,h,'PrepareCNE5已完成...46.23%');
    SizeX;
    waitbar(0.4762,h,'PrepareCNE5已完成...47.62%');
    ResidualVolatilityX;
    waitbar(0.5970,h,'PrepareCNE5已完成...59.70%');
    BooktopriceX;
    waitbar(0.6045,h,'PrepareCNE5已完成...60.45%');
    LiquidityX;
    waitbar(1,h,'PrepareCNE5已完成...100%');
    pause(1);
    delete(h);
end
load Beta 
load Momentum 
load Size 
load ResidualVolatility 
load Booktoprice 
load Liquidity
stocksValue={betaValue{1},momentumValue{1},sizeValue{1},residualVolatilityValue{1},...
    booktopriceValue{1},liquidityValue{1}};
sameStocks=stocksValue{1};
indicatorsValue={betaValue{2}(:,1),momentumValue{2},sizeValue{2},residualVolatilityValue{2},...
    booktopriceValue{2},liquidityValue{2}}; % 此处momentumValue 和residualVolatilityValue是复数，需要确认修改；
for i=2:6
    sameStocks=intersect(sameStocks,stocksValue{i});
end
indicators=zeros(length(sameStocks),6);
for i=1:6
    [~,~,ind]=intersect(sameStocks,stocksValue{i});
    indicators(:,i)=indicatorsValue{i}(ind);
end

prepareCNE5Value={sameStocks,indicators};
save PrepareCNE5 prepareCNE5Value;
end

