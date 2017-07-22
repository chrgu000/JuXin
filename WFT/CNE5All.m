function [stocks_weights,weights,stdDev]=CNE5All
tic;
h=waitbar(0,'Read in data for running......');
w=windmatlab;
dataTem=w.wset('IndexConstituent','date=20170308;windcode=000300.SH');
stocks=dataTem(:,2);
weights=cell2mat(dataTem(:,4));
test=w.wsd(stocks,'close','ED-60TD',today-370*3,'Fill=Previous','PriceAdj=F');
ind=sum(isnan(test))<1;
stocks=stocks(ind); % delete stocks whose trading time is less than 3 years;
weights=weights(ind);
% stocks=stocks(1:200);
numStocks=length(stocks);
%% Get indicators: 1--Beta,2--Momentum,3--Size,4--ResidualVolatility,5--Booktoprice,6--Liquidity;
Shares=w.wss(stocks,'float_a_shares');
Price=zeros(821,numStocks);
Volume=zeros(820,numStocks);
Equity=zeros(820,numStocks);
for i=1:1500:numStocks
    if i+1500<numStocks
        Price(:,i:i+1500)=w.wsd(stocks(i:i+1500),'close','ED-820TD',today-1,'Fill=Previous','PriceAdj=F');
        Volume(:,i:i+1500)=w.wsd(stocks(i:i+1500),'volume','ED-819TD',today-1,'Fill=Previous','PriceAdj=F');
        Equity(:,i:i+1500)=w.wsd(stocks(i:i+1500),'bps','ED-819TD',today-1,'Fill=Previous','PriceAdj=F');
    else
        Price(:,i:end)=w.wsd(stocks(i:end),'close','ED-820TD',today-1,'Fill=Previous','PriceAdj=F');
        Volume(:,i:end)=w.wsd(stocks(i:end),'volume','ED-819TD',today-1,'Fill=Previous','PriceAdj=F');
        Equity(:,i:end)=w.wsd(stocks(i:end),'bps','ED-819TD',today-1,'Fill=Previous','PriceAdj=F');
    end
end
for i=1:numStocks % replace 0 in matrix by mean of non-elements in column;
    tem=Volume(:,i);
    ind=tem==0;
    tem(ind)=mean(tem(~ind));
    Volume(:,i)=tem;
end
% rt=Price(2:end,:)./repmat(Price(1,:),size(Price,1)-1,1)-1;
% rft=1.00013652*ones(size(rt));
% rft=cumprod(rft)-1;
rt=Price(2:end,:)./Price(1:end-1,:)-1;
rft=0.00001386*ones(size(rt));

y=rt-rft;%504 rows and each column stands for one stock's return;
hs300Price=w.wsd('000300.sh','close','ED-820TD',today-1,'Fill=Previous','PriceAdj=F');
Rt=hs300Price(2:end)./repmat(hs300Price(1,:),size(hs300Price,1)-1,1)-1;% returns of hu-shen_300 on the past 504 trading days; 
BetaX=zeros(252,numStocks); 
funTem=@(x)0.5.^(x/63);
wtBeta=flipud(funTem(1:252)');
myfunc=@(beta,x) beta(1)*x+beta(2);
MomentumX=zeros(252,numStocks);
funTem=@(x) 0.5.^(x/126);
wtMomentum=flipud(funTem(1:504)');
SizeX=zeros(252,numStocks);
ResidualVolatilityX=zeros(252,numStocks);
funTem=@(x)0.5.^(x/42);
wtRV=flipud(funTem(1:252)');
LiquidityX=zeros(252,numStocks);
for i=569:820 % loop for 252 trading days;
    %% Get----Beta  
    HSIGMA=zeros(1,numStocks); % prepare for 'ResidualVolatility';
    for j=1:numStocks
        [beta,r]=nlinfit(Rt(i-251:i),y(i-251:i,j),myfunc,[1,1],'Weights',wtBeta);
        BetaX(i-568,j)=beta(1);
        HSIGMA(j)=std(r);
    end
    %% Get----Momentum
    MomentumX(i-568,:)=sum(repmat(wtMomentum,1,numStocks).*log((1+rt(i-524:i-21,:))./(1+rft(i-524:i-21,:)))); 
    %% Get----Size
    SizeX(i-568,:)=log(Shares'.*Price(i,:));
    %% Get----ResidualVolatility
    DASTD=std(y(i-251:i,:),wtRV);
    ind_tem=i-252:21:i;
    rt21=rt(ind_tem,:);
    rft21=rft(ind_tem,:);
    Z=log( bsxfun(@rdivide,(1+rt21),(1+rft21)) );
    Z=cumsum(Z);
    CMRA=max(Z)-min(Z);
    ResidualVolatilityX(i-568,:)=0.74*DASTD+0.16*CMRA+0.1*HSIGMA;    
    %% Get----Liquidity
    stom=@(x) log(sum(Volume(x-20:x,:)./repmat(Shares',21,1)));
    STOM=stom(i); 
    STOQTem=zeros(size(STOM));
    STOATem=zeros(size(STOM));
    for j=0:12
        Tem=stom(i-j*21);
        if j<3
            STOQTem=STOQTem+exp(Tem);
        end
        STOATem=STOATem+exp(Tem);       
    end
    STOQ=log(STOQTem/3);
    STOA=log(STOATem/12);    
    LiquidityX(i-568,:)=0.35*STOM+0.35*STOQ+0.3*STOA;
    
    temBar=(i-569)/252;
    temBar=roundn(temBar,-4);
    tem=toc;
    temTime=roundn(tem/60,-1);  
    waitbar(temBar,h,['Completed...',num2str(100*temBar),'%; Time lapses:',num2str(temTime),' minutes.']);    
end
%% Get----Booktoprice
BooktopriceX=Equity(end-251:end,:)./Price(end-251:end,:);
%% Get--Industry
data=w.wss(stocks,'industry_gics','industryType=3');
[dataUnique,~,indexMap]=unique(data);
Ldata=length(data);
Lunique=length(dataUnique);
Indicators=zeros(Ldata,Lunique);
for i=1:Ldata
    Indicators(i,indexMap(i))=1;
end
industryInd=Indicators; %'Indicators' is an matrix: number of stocks X kinds of Industries;

%% Optimization;
Y=Price(end-251:end,:)./Price(end-252:end-1,:)-1; % each day's return for each stock; % [f,~,u]=regress(y,X);
F=zeros(numStocks,54);
U=zeros(numStocks,size(Y,1));
for i=1:numStocks
    yTem=Y(:,i);
    XTem=[BetaX(:,i),MomentumX(:,i),SizeX(:,i),ResidualVolatilityX(:,i),LiquidityX(:,i),BooktopriceX(:,i),repmat(industryInd(i,:),252,1)];
    %XTem=mapstd(XTem);
    [f,~,u]=regress(yTem,XTem);
    F(i,:)=f;
    U(i,:)=u;
end
Xmat=zeros(numStocks,54);
for i=1:numStocks
    Xmat(i,:)=[BetaX(1,i),MomentumX(1,i),SizeX(1,i),ResidualVolatilityX(1,i),LiquidityX(1,i),BooktopriceX(1,i),industryInd(i,:)];
end
Fmat=cov(F);
Deltamat=cov(U').*eye(size(U',2));

numAssets = numStocks;
expectedReturns = sum(Y)'; 
targetReturn = 10;
covMx=Xmat*Fmat*Xmat'+Deltamat;
H = 2*covMx;
f = zeros(numAssets,1); 
A = -transpose(expectedReturns);
b = -targetReturn;
% lb = -inf*ones(numAssets,1);
lb = -1*ones(numAssets,1);
ub = inf*ones(numAssets,1);
beq = [1];
Aeq = transpose(ones(numAssets,1));
[weights,variance] = quadprog(H,f,A,b,Aeq,beq,lb,ub);
stdDev = sqrt(variance);
stocks_weights=[stocks,num2cell(weights)];
delete(h)
toc;
end


% function value=CNE5All
% % [status, cmdout] = system('python xxx.py in.txt out.txt') % matlab calls
% % python function to get return value;
% % # -*- coding: utf-8 -*-
% % import sys
% % if __name__=="__main__":
% %         infile = sys.argv[1]
% %         outfile = sys.argv[2]
% %         fin = open(infile, 'r')
% %         fout = open(outfile, 'w')
% %         a = fin.readline().strip()
% %         b = fin.readline().strip()
% %         c = float(a)+float(b)
% %         fout.write('%f' % c)
% %         fout.close()
% %         fin.close()
% tic;
% updateButton=input('update or not? y/n [n]:','s');
% if ~isempty(updateButton)&&updateButton=='y'
%     pythonFile='python D:\Trading\Python\TS.py';
%     system(pythonFile);
% end
% dirFiles='E:\TuData\hs300\';
% files=dir([dirFiles,'*.xlsx']);
% numStocks=length(files);
% stocks=zeros(numStocks,1);
% Price=zeros(821,numStocks);
% Volume=zeros(820,numStocks);
% iTem=0;
% for i=1:numStocks
%     fileTem=files(i);
%     nameTem=fileTem.name(1:6);
%     dataTem=xlsread([dirFiles,nameTem]);
%     if size(dataTem,1)>820
%         stocks(i-iTem)=str2num(nameTem);
%         Price(:,i-iTem)=dataTem(end-820:end,4);
%         Volume(:,i-iTem)=dataTem(end-819:end,7);
%     else
%         iTem=iTem+1;
%     end
% end
% indTem=1:sum(stocks~=0);
% stocks=stocks(indTem);
% Price=Price(:,indTem);
% Volume=Volume(:,indTem);
% dataTem=xlsread('e:\TuData\stocksBasics.csv');% only can get current data
% allStocks=dataTem(:,1);
% Shares=dataTem(:,6);
% Equity=dataTem(:,14);
% [~,indTemA,indTemS]=intersect(allStocks,stocks);
% Shares=Shares(indTemA)*10^8;
% stocks=stocks(indTemS);
% Price=Price(:,indTemS);
% Volume=Volume(:,indTemS);
% numStocks=length(stocks);
% %% Get indicators: 1--Beta,2--Momentum,3--Size,4--ResidualVolatility,5--Booktoprice,6--Liquidity;
% rt=Price(2:end,:)./Price(1:end-1,:)-1;
% rft=0.00001386*ones(size(rt));
% y=rt-rft;%504 rows and each column stands for one stock's return;
% dataTem=xlsread('e:\TuData\hs300.xlsx');
% hs300Price=dataTem(end-820:end,4);
% Rt=hs300Price(2:end)./repmat(hs300Price(1,:),size(hs300Price,1)-1,1)-1;% returns of hu-shen_300 on the past 504 trading days; 
% BetaX=zeros(252,numStocks); 
% funTem=@(x)0.5.^(x/63);
% wtBeta=flipud(funTem(1:252)');
% myfunc=@(beta,x) beta(1)*x+beta(2);
% MomentumX=zeros(252,numStocks);
% funTem=@(x) 0.5.^(x/126);
% wtMomentum=flipud(funTem(1:504)');
% SizeX=zeros(252,numStocks);
% ResidualVolatilityX=zeros(252,numStocks);
% funTem=@(x)0.5.^(x/42);
% wtRV=flipud(funTem(1:252)');
% LiquidityX=zeros(252,numStocks);
% for i=569:820 % loop for 252 trading days; 
%     %% Get----Beta  
%     HSIGMA=zeros(1,numStocks); % prepare for 'ResidualVolatility';
%     for j=1:numStocks
%         [beta,r]=nlinfit(Rt(i-251:i),y(i-251:i,j),myfunc,[1,1],'Weights',wtBeta);
%         BetaX(i-568,j)=beta(1);
%         HSIGMA(j)=std(r);
%     end
%     %% Get----Momentum
%     MomentumX(i-568,:)=sum(repmat(wtMomentum,1,numStocks).*log((1+rt(i-524:i-21,:))./(1+rft(i-524:i-21,:)))); 
%     %% Get----Size
%     SizeX(i-568,:)=log(Shares'.*Price(i,:));
%     %% Get----ResidualVolatility
%     DASTD=std(y(i-251:i,:),wtRV);
%     ind_tem=i-252:21:i;
%     rt21=rt(ind_tem,:);
%     rft21=rft(ind_tem,:);
%     Z=log( bsxfun(@rdivide,(1+rt21),(1+rft21)) );
%     Z=cumsum(Z);
%     CMRA=max(Z)-min(Z);
%     ResidualVolatilityX(i-568,:)=0.74*DASTD+0.16*CMRA+0.1*HSIGMA;    
%     %% Get----Liquidity
%     stom=@(x) log(sum(Volume(x-20:x,:)./repmat(Shares',21,1)));
%     STOM=stom(i); 
%     STOQTem=zeros(size(STOM));
%     STOATem=zeros(size(STOM));
%     for j=0:12
%         Tem=stom(i-j*21);
%         if j<3
%             STOQTem=STOQTem+exp(Tem);
%         end
%         STOATem=STOATem+exp(Tem);       
%     end
%     STOQ=log(STOQTem/3);
%     STOA=log(STOATem/12);    
%     LiquidityX(i-568,:)=0.35*STOM+0.35*STOQ+0.3*STOA;
% 
% end
% %% Get----Booktoprice
% % BooktopriceX=Equity(end-251:end,:)./Price(end-251:end,:); % just can get
% % current value rather than all history's value;
% 
% Y=Price(end-251:end,:)./Price(end-252:end-1,:)-1; % each day's return for each stock; % [f,~,u]=regress(y,X);
% F=zeros(numStocks,5);
% U=zeros(numStocks,size(Y,1));
% for i=1:numStocks
%     yTem=Y(:,i);
%     XTem=[BetaX(:,i),MomentumX(:,i),SizeX(:,i),ResidualVolatilityX(:,i),LiquidityX(:,i)];
%     %XTem=mapstd(XTem);
%     [f,~,u]=regress(yTem,XTem);
%     F(i,:)=f;
%     U(i,:)=u;
% end
% 
% Xmat=XTem;
% Fmat=cov(F);
% Deltamat=cov(U).*eye(size(U,2));
% 
% 
% 
% toc;
% end




