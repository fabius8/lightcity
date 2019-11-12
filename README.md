# convert2gpx
高德指定城市转换经纬度

需要配合xcode虚拟定位，可对城市漫游，快速实现高德点亮城市。

# 使用方法
1. 修改city.json，添加城市
2. ./convert2gpx city.json 生成 city.gpx
3. 将gpx文件添加到xcode工程，虚拟定位选择该文件即可
