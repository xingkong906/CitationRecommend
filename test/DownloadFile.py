from util.downloader import Downloader
file_name = "../data_set/data.html"
url = 'http://aan.how/browse/paper/30000'
with open(file_name, 'w',encoding='utf-8') as file:
    file.write(Downloader(url)())
print("写入完成")