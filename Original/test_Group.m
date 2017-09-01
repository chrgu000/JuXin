function test_Group(fun)

f=@(x) fun(x);
load IDNames;
stocksind=randi(2781,1,600);
[data,stock]=arrayfun(f,IDNames,'UniformOutput',false);
% [data,stock]=arrayfun(f,IDNames(unique(stocksind)),'UniformOutput',false); %
Data=vertcat(data{:});

ind=Data(:,1)>-1 & Data(:,1)<1; % delete nonsense stocks;
Data=Data(ind,:); 
stock=stock(ind);

[Data,ind]=sortrows(Data);
DataStock=flipud([num2cell(Data),stock(ind)]);
profitP=Data(:,1);
winorders=sum(profitP>0  & profitP<1);
lossorders=sum(profitP<0 & profitP>-1);
ratio=winorders/(lossorders+winorders);

f=figure;
t1=uitable(f,'position',[1 1 300 350],'Data',DataStock,'ColumnName',{'profitP','capi','orders','win','drawB','stocks'});
t1.Position(3)=t1.Extent(3);
t2=uitable(f,'position',[1 360 200 50],'Data',[winorders lossorders ratio],'ColumnName',{'winstocks','lossstocks','ratio'});
t2.Position(3)=t2.Extent(3);
t2.Position(4)=t2.Extent(4);

end



