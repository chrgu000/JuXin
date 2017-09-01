function getIDNames(IDNames)
L=length(IDNames);
for i=1:L
    if IDNames{i}(1)=='6'
        IDNames(i)=strcat('SH',IDNames(i));
    else
        IDNames(i)=strcat('SZ',IDNames(i));
    end
end
save IDNames IDNames;
end