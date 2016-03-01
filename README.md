# 介绍            
参见: [图书馆图书状态监控服务](http://www.studyandshare.info/monitor_book_service.html)               
             
# 原理说明            
通过 [这个网页](http://www.studyandshare.info/mon_Lib_bok_collect_info.html) 收集用户提交的 `URL`,`书名`,`邮箱` 信息，并将这些信息保存到文件 `urls.txt` 中 ,而 `LibraryScaner.py` 通过 `urls.txt` 来获取要监控的URL，从而进一步获取相应的URL网页，通过分析网页中的关键字，来判断所要监控的图书的书刊状态。如果所要监控的图书变为 **可借** 状态，则通过调用shell脚本 `SendMail.sh` 向用户指定的邮箱发送Email来通知用户。                
                     
利用 Unix/Linux 系统中的 `Cron` 服务，来使 `LibraryScaner.py` 每隔一定时间（比如20分钟）就运行一次，即文件 `urls.txt` 文件中的URL每隔一定时间（比如20分钟）就被扫描一遍，从而实现了对图书馆书刊状态的全天候监控。                   


