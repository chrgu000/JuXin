function MACD(varargin)
narginchk(1,4)
if nargin==1
    short=12;
    long=26;
    mlen=9;
elseif nargin==2
    short=varargin{2};
    long=26;
    mlen=9;
elseif nargin==3
    short=varargin{2};
    long=varargin{3};
    mlen=9;
else
    short=varargin{2};
    long=varargin{3};
    mlen=varargin{4};
end
DIFF=EMA(varargin{1},short)-EMA(varargin{1},long);
DEA=EMA(DIFF,mlen);
MACDbar=2*(DIFF-DEA);
pind=find(MACDbar>=0);
nind=find(MACDbar<0);
hold on;
grid on;
plot(DIFF,'k');
plot(DEA,'b');
bar(pind,MACDbar(pind),'r','EdgeColor','r','LineWidth',0.1);
bar(nind,MACDbar(nind),'g','EdgeColor','g','LineWidth',0.1);
hold off;
end

function EMAValue=EMA(Price,Length)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
EMAValue=zeros(length(Price),1);
K=2/(Length+1);
for i=1:length(Price)
    if i==1
        EMAValue(i)=Price(i);
    else 
        EMAValue(i)=Price(i)*K+EMAValue(i-1)*(1-K);
    end
end
end
