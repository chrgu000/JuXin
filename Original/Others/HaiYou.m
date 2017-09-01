function HaiYou(varargin)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
if mod(nargin,2)==0 && nargin~=0
    figure;
    hold on;
    for i=1:2:nargin
        [f,p]=fit(varargin{i},varargin{i+1},fittype('poly1'));
        plot(f,varargin{i},varargin{i+1},'*');
        a1=num2str((i+1)/2);
        a2=num2str(p.rsquare);
        disp(strcat(a1,'R^2 is:',a2));
    end
    hold off;
else
    disp('Input aguments are wrong,the number of aguments must be 2 or times  of 2;');
    disp('Please put in them again!');
end
end

