function getIFIHIC % get data of IF/IH/IC from wind and save thme onto 'e:' disk.
w=windmatlab;
[IF00,~,~,IFtimes]=w.wsi('IF00.CFE','volume,open,high,low,close',...
    '2012-01-01 09:00:00',today);
[IH00,~,~,IHtimes]=w.wsi('IH00.CFE','volume,open,high,low,close',...
    '2015-01-01 09:00:00',today);
[IC00,~,~,ICtimes]=w.wsi('IC00.CFE','volume,open,high,low,close',...
    '2015-01-01 09:00:00',today);
save('E:\IFIHIC','IF00','IFtimes','IH00','IHtimes','IC00','ICtimes')
end