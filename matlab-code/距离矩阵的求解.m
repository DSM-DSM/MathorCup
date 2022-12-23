[i,j]=size(aunt);
[m,n]=size(order);
aunt = table2array(aunt);
oorder = table2array(order);

dist = zeros(m,i);
for p=1:m
    for q=1:i
        delta_x = aunt(q,1)-order(p,1);
        delta_y = aunt(q,2)-order(p,2);
        dist(p,q) = sqrt(delta_x^2/1000+delta_y^2/1000);
    end
end
xlswrite('dist.xlsx',dist)
