library(readxl)
library(mvnTest)
aunt <- read_excel(
  'D:/QQ下载文件/MathorCup大数据竞赛资料/代码/data/aunt.xlsx')
order <- read_excel(
  'D:/QQ下载文件/MathorCup大数据竞赛资料/代码/data/order.xlsx')

mshapiro.test(t(aunt[,3:4]))
mshapiro.test(t(order[,6:7]))
