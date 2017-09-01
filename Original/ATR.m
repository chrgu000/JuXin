function re=ATR(varargin) % varargin(1) means 
global high low close;
I=varargin{1};
re(I)=0;
for i=2:I
    HL=high(i)-low(i);
    HC=abs(high(i)-close(i-1));
    LC=abs(low(i)-close(i-1));
    re(i)=max([HL HC LC]);
end
if nargin==2
    ma=varargin{2};
    Re(I,1)=0;
    for i=ma+1:I
        Re(i)=mean(re(i-ma+1:i));
    end
    re=Re;
end

end