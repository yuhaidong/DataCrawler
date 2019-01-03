import requests                 #导入requests模块
from bs4 import BeautifulSoup   #导入BeautifulSoup模块
import os                       #导入os模块，os模块提供了非常丰富的方法用来处理文件和目录
import time						#导入time模块

class BeautifulPicture():

	# 类的初始化操作，设置3个变量：浏览器类型、url地址、存储路径
	def __init__(self):
		# 给请求指定一个请求头来模拟chrome浏览器
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
		# 要访问的网页地址，unsplash.com网站很好的一点是，网站上保存有每张图片的不同像素版本，可以根据需要抓取
		self.web_url = 'https://unsplash.com'
		# 设置图片要存放的文件目录
		self.folder_path = '/Users/yuhaidong/studying/python/pycharm/test/folder'

	# 返回requests网页的response
	def request(self, url):
		# 向目标url地址发送get请求，返回一个response对象
		r = requests.get(url)
		return r

	# 创建文件夹
	def mkdir(self, path):
		# strip函数去除首尾空格
		path = path.strip()
		isExists = os.path.exists(path)
        
		if not isExists:
			print('创建名字叫做', path, '的文件夹')
            
            # 创建文件夹
			os.makedirs(path)
            
			print('创建成功！')
		else:
			print(path, '文件夹已经存在了，不再创建')

	# 保存图片
	def save_img(self, url, name):
		print('开始保存图片...')

		# 请求访问
		img = self.request(url)
		# 让线程休眠一段时间
		time.sleep(0.5)
		# 文件名称，这里是图片名称
		file_name = name + '.jpg'

		print('开始保存文件')

		# 文件打开模式为“ab”，表示以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。
		# 也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
		f = open(file_name, 'ab')
		# 写入文件
		f.write(img.content)

		print(file_name, '文件保存成功！')


		# 关闭文件
		f.close()

	# 页面抓取的逻辑
	def get_pic(self):
		print('开始网页get请求')
        

        # 请求访问页面
		request_page = self.request(self.web_url)
        
		print('开始获取所有a标签')

        # 使用BeautifulSoup作文档解析，request_page.text是所获得的请求页面。
        # 定义一个BeautifulSoup变量并调用其find_all()方法。
        # 获取网页中的class为“_2zEKz”的所有"img"标签。
        # 这里文档解析器使用的是Python的内置标准库html.parser。
		all_a = BeautifulSoup(request_page.text, 'html.parser').find_all('img', class_='_2zEKz')
        
		print('开始创建文件夹')

        # 创建文件夹
		self.mkdir(self.folder_path)
        
		print('开始切换文件夹')

        # 切换路径至上面创建的文件夹
		os.chdir(self.folder_path)

        # 爬取的每张图片的像素大小，默认设为900w
        # https://unsplash.com/这个网站里每张图片都提供了很多种像素版本，这里是在设置一个要获取的像素版本
		pixel = '900w'

		# 后面用来给图片命名
		i = 1

		# 将爬虫的循环操作放入到try...except中，捕获异常
		try:
			for a in all_a:
				# img标签中完整的srcset字符串
				img_str_all = a['srcset']
				# 显示完整的url
				print('a标签的style内容是：', img_str_all)

				# 截取拿到pixel变量对应像素的url
				img_str = img_str_all[0:img_str_all.find(pixel)]
				# strip()函数去除首尾空格
				img_str = img_str.strip()
				# 显示截取后的url路径
				print('截取后的图片的url是：', img_str)

				# 保存图片，str()函数返回一个对象的string格式
				self.save_img(img_str, str(i))

				i += 1
		except KeyboardInterrupt:
			print('爬虫执行中断，执行过程使用ctrl+C中断！')		
		except Exception as e:
			print('爬虫执行中断，执行过程出现异常！')
		else:
			print('爬虫执行成功！整个过程未出现异常！全部图片共%d张全部保存成功！'%(i-1))
		finally:
			print('----------爬虫执行完成！----------')

#创建类的实例
beauty = BeautifulPicture()
#执行类中的方法
beauty.get_pic()
