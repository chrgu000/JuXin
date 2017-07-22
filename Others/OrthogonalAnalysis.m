function OrthogonalAnalysis % cname is the names of all factors which should be input one by one.
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
[filename,pathname]=uigetfile('*.xls','Select the excel file!');
if filename==0
    warndlg('No file was selected!');
    return;
end
f=fullfile(pathname,filename);
[data,str]=xlsread(f);
cname=str(1,2:end);
[r,c]=size(data);
datas=sum(data);
datas(datas~=datas(1))=1;
datas(datas==datas(1))=0;
n=sum(datas); % the number of values' columns
level=r/(c-n-1); % the level of factors;
if mod(level,1)~=0
    level=r/(c-n);
end
rowdest=data(:,1:end-n);

rowvals=data(:,end-n+1:end);
T=sum(sum(rowvals));
if n==1
    Rowvals=rowvals;
else
    Rowvals=sum(rowvals')';
end
coldest=repmat(1:size(rowdest,2),size(rowdest,1),1);
Tn=accumarray([rowdest(:) coldest(:)], repmat(Rowvals, size(rowdest, 2), 1)); % save the sum of values of each factor's level;
C=T^2/(r*n);
SST=sum(sum(rowvals.^2))-C;
SSn=sum(Tn.^2)/(level*n)-C;
fT=r*n-1;
fn=repmat(level-1,1,c-n);
if n==1   
    SSe=SST-sum(SSn);
    fe=fT-sum(fn);
    if fe~=0
        MS=[SSn SSe]./[fn fe];
        F=MS(1:end-1)/MS(end);
        Fx=[finv(0.95,level-1,fe) finv(0.99,level-1,fe) finv(0.995,level-1,fe)];
    else
        MS=SSn./fn;
        F=MS/min(MS);
        Fx=[finv(0.95,level-1,level-1) finv(0.99,level-1,level-1) finv(0.995,level-1,level-1)];
    end
    if c<5
        data=[data,zeros(r,5-c)];
    end
    data=[data;zeros(c-n+3,size(data,2))]; % 3 means: table name, error, total variation.
    data(r+2:end,1)=[SSn';SSe;SST];
    data(r+2:end,2)=[fn';fe;fT];
    data(r+2:r+1+size(MS,2),3)=MS';
    data(r+2:r+1+size(F,2),4)=F';
    data(r+2:r+4,5)=Fx';
    
else   
    SSr=sum(sum(rowvals).^2)/r-C; 
    SSt=sum(sum(rowvals').^2)/n-C;
    SSe1=SSt-sum(SSn);
    SSe2=SST-SSr-SSt;
    fr=n-1;
    ft=r-1;
    fe1=ft-sum(fn);
    fe2=fT-fr-ft;
    
    MS=[SSn SSr SSe1 SSe2]./[fn fr fe1 fe2];
    F=MS(1:end-1)./MS(end);
    F95=[finv(0.95,level-1,fe2) finv(0.95,fr,fe2)];
    F99=[finv(0.99,level-1,fe2) finv(0.99,fr,fe2)];
    if F(end)<F95(1)
        SSe=SSe1+SSe2;
        fe=fe1+fe2;
        F=MS(1:end-2)./(SSe/fe);
    end
    if c<6
        data=[data,zeros(r,6-c)];
    end
    data=[data;zeros(c-n+5,size(data,2))]; % 3 means: table name, error, total variation.
    data(r+2:end,1)=[SSn';SSr;SSe1;SSe2;SST];
    data(r+2:end,2)=[fn';fr;fe1;fe2;fT];
    data(r+2:end-1,3)=MS';
    data(r+2:r+1+size(F,2),4)=F';
    data(r+2,5)=F95(1);data(r+2+c-n,5)=F95(2);
    data(r+2,6)=F99(1);data(r+2+c-n,6)=F99(2);
    
end
Cdata=num2cell(data); % cell format of data;
map=str(r+2:end,2:c-n+1);
Cdata(1:r,1:c-n)=map(bsxfun(@plus,data(1:r,1:c-n),0:size(map,1):numel(map)-1));
[R,C]=size(Cdata);
if n==1
    Cdata(r+1,1:5)={'SS' 'f' 'MS' 'F' 'F95/9/95'};
    rname={str{2:r+1,1},'Va_Source',cname{1:c-n},'Error','To_Variation'};  
else
    Cdata(r+1,1:6)={'SS' 'f' 'MS' 'F' 'F95','F99'};
    rname={str{2:r+1,1},'Va_Source',cname{1:c-n},'Group','Error1','Error2','To_Variation'};
end

showData = Cdata;
colorgen0 = @(text) cellstr(['<html><table border=0 width=1000 >',text,'</table></html>']);
colorgen = @(color,text) cellstr(['<html><table border=0 width=1000 bgcolor=',color,'>',text,'</table></html>']);
% showData(r+1,:) = cellfun(@(x) sprintf('<HTML><TABLE><TD color="blue" >%s</TD></TABLE>', x), showData(r+1,:), 'Uniform', 0);
showData(r+1,:) = cellfun(@(x) sprintf('<HTML><TABLE><TD><font size="4" color="red" >%s</font></TD></TABLE>', x), showData(r+1,:), 'Uniform', 0);
% showData(r+1,:) = cellfun(@(x) sprintf('<HTML><TABLE><div class="text" style="text-align:center;">%s</div></TABLE>', x), showData(r+1,:), 'Uniform', 0);


% set 0 to a space
% convert all cells into strings, otherwise we can't construct HTML code
for i = 1:R
	for j = 1:C
		if showData{i,j} == 0
			showData(i,j) = cellstr('&nbsp;');
		end
		if ~ischar(showData{i,j})
			showData(i,j) = cellstr(num2str(showData{i,j}));
		end
	end
end
% color raw data rows to yellow
for i = 1:r
	for j = 1:C
		showData(i,j) = colorgen0(showData{i,j});
	end
end
% color rows 6:9 to red
for i = r+1:R
	for j = 1:C
		showData(i,j) = colorgen('#FFFF00', showData{i,j});
	end
end
    
f=figure('Position',[0 60 130+C*80,30+R*20]);
t=uitable(f,'Data',showData,...
            'ColumnName',cname,...
            'RowName',rname);
t.Position(3)=t.Extent(3);
t.Position(4)=t.Extent(4);
% t.ForegroundColor=[0 0 1];
srsz=get(0,'ScreenSize');
figure('Position',[mod(130+C*80,srsz(3)),60,500,330]);
dot=1:level;
plot(dot,Tn);
legend(cname(1:c-n));

end


% Cdata={'30 min' '1.5 g' '45?' 53.11 0;'30 min' '2.0 g' '55?' 59.09 0;'60 min' '1.5 g' '55?' 71.31 0;'60 min' '2.0 g' '45?' 70.24 0;...
% 'SS' 'f' 'MS' 'F' 'Fx' ;215.3556 1 215.3556 35.7317 161.4476;... 
% 12.4256 1 12.4256 2.0617 1.6211e+03;0 0 0 0 0 ;233.8083 3 0 0 0;}
% 
% 
% f=figure;
% t=uitable(f,'data',Cdata);
% t.Position(3)=t.Extent(3);
% t.Position(4)=t.Extent(4);
% 
% new_Cdata = Cdata;
% row1_4 = cellfun(@(x) sprintf('<HTML><TABLE><TD color="red" bgcolor="yellow">%.4g</TD></TABLE>', x), Cdata(1:4,:), 'Uniform', 0);
% row5 = cellfun(@(S) sprintf('<HTML><TABLE><TD color="blue" bgcolor="red"><FONT size="+1">%s</FONT></TD></TABLE>', S), Cdata(5,:), 'Uniform', 0);
% row6plus = cellfun(@(x) sprintf('<HTML><TABLE><TD color="yellow" bgcolor="red">%.4g</TD></TABLE>', x), Cdata(6:end,:), 'Uniform', 0);
% new_Cdata(1:4,:) = row1_4;
% new_Cdata(5,:) = row5;
% new_Cdata(6:end,:) = row6plus;
% set(t, 'Data', new_Cdata);

