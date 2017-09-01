function AvsBGroup(varargin)
% when the last parameter is 1, draw curves of A and B; or don't draw
% curves;
% when only one parameter or two parameters(one is stock A's number, the other
% is 1), then only calculate the correlations of A and selected dir's
% stocks;
% varargin{end}=='c' means test stock data saved in "
% E:\360Synchronization\360Synchronization\MatLab\DataFromZX\BackTest"
spec=0;
if nargin==0 
    path=uigetdir;
    name_f=dir(strcat(path,'\*.txt'));
    name={name_f.name};
    pict=0;
elseif nargin==1 && isnumeric(varargin{1})
    path=uigetdir;
    name_f=dir(strcat(path,'\*.txt'));
    name={name_f.name};
    pict=1;
elseif (nargin==1 & length(varargin{1})==8) | (nargin==2 & varargin{2}==1)
    spec=1;
    path=uigetdir;
    name_f=dir(strcat(path,'\*.txt'));
    name={name_f.name};
    if nargin==1
        pict=0;
    else
        pict=1;
    end
else
    if varargin{end}==1 | varargin{end}=='c'
        pict=varargin{end};
        name=varargin(1:end-1);
    elseif varargin{end}==0
        pict=0;
        name=varargin(1:end-1);
    else
        pict=0;
        name=varargin(1:end);        
    end    
end

if spec==0
    el=1:numel(name);
    ind=nchoosek(el,2);
    A=name(ind(:,1))';
    B=name(ind(:,2))';
    N=repmat(pict,length(A),1);
else
    A=repmat(varargin(1),length(name),1);
    B=name';
    N=repmat(pict,length(A),1);
end
ratio=arrayfun(@(x,y,z) AvsB(x,y,z),A,B,N);

[ratio,ind]=sort(ratio);
A=A(ind);
B=B(ind);
ratio=num2cell(ratio);
TableData=[A,B,ratio];
cname={'A','B','Correlation'};
f=figure;
uitable(f,'Data',TableData,'ColumnName',cname);
% t.Position(3)=f.Extent(3);
% t.Position(4)=t.Extent(4);
end