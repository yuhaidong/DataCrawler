
from selenium import webdriver  #导入Selenium
import requests                 #导入requests模块
from bs4 import BeautifulSoup   #导入BeautifulSoup模块
import os                       #导入os模块，os模块提供了非常丰富的方法用来处理文件和目录
import time						#导入time模块

class BeautifulPicture():

	# 初始化函数
	def __init__(self):
		# 给请求指定一个请求头来模拟chrome浏览器
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
		# 要访问的网页地址，unsplash.com网站很好的一点是，网站上保存有每张图片的不同像素版本，可以根据需要抓取
		self.web_url = 'https://unsplash.com'
		# 设置图片要存放的文件目录
		self.folder_path = '/Users/yuhaidong/studying/temp/folder' 

	# 创建文件夹函数
	def mkdir(self, path):
		# strip函数去除首尾空格
		path = path.strip()
		isExists = os.path.exists(path)

		if not isExists:
			print('创建名字叫做', path, '的文件夹')
			os.makedirs(path)
			print('创建成功！')
			return True
		else:
			print(path, '文件夹已经存在了，不再创建')
			return False

	# 返回requests网页的response
	def request(self, url):
		# 向目标url地址发送get请求，返回一个response对象
		r = requests.get(url)
		return r

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

	# 下拉操作函数
	def scroll_down(self, driver, times):
		print("----------------开始执行下拉操作！----------------")

		for i in range(times):
			print("---------开始执行第", str(i + 1),"次下拉操作---------")
			
			#执行JavaScript实现网页下拉倒底部
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 500);")
			
			print("第", str(i + 1), "次下拉操作执行完毕！开始等待页面加载...")
			
			# 等待20秒（时间可以根据自己的网速而定），页面加载出来再执行下拉操作
			time.sleep(10)

	# 业务抓取的逻辑
	def get_pic(self):
		print('开始网页get请求')
		
		# 注意！！Selenium不再支持PhantomJS了，改用Chrome
		#driver = webdriver.PhantomJS()
		# 使用selenium通过Chrome来进行网络请求。
		driver = webdriver.Chrome(executable_path='/Users/yuhaidong/studying/selenium/chromedriver')

		# 请求抓取地址
		driver.get(self.web_url)
		#执行网页下拉到底部操作，执行3次
		self.scroll_down(driver=driver, times=2)
		
		print('开始获取所有a标签')

		# 使用BeautifulSoup作文档解析，driver.page_source是所获得的请求页面。
		all_a = BeautifulSoup(driver.page_source, 'html.parser').find_all('img', class_='_2zEKz')
		
		print('开始创建文件夹')

		#创建文件夹
		self.mkdir(self.folder_path)

		print('开始切换文件夹')

		#切换路径至上面创建的文件夹
		os.chdir(self.folder_path)

		# 这里添加一个查询图片标签的数量，来检查我们下拉操作是否有误
		print("a标签的数量是：", len(all_a))

		pixel = '900w'

		# 后面用来给图片命名
		i = 1

		# 将爬虫的循环操作放入到try...except中，捕获异常
		try:
			# 循环每个标签，获取标签中图片的url并且进行网络请求，最后保存图片
			for a in all_a:
				# a标签中完整的style字符串
				img_str_all = a['srcset']

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
			print('爬虫执行中断，执行过程出现异常！Exception是：', e)
		else:
			print('爬虫执行成功！整个过程未出现异常！全部图片共%d张全部保存成功！'%(i-1))
		finally:
			print('----------爬虫执行完成！----------')

		print("a标签的数量是：", len(all_a))

#创建类的实例
beauty = BeautifulPicture()
#执行类中的方法
beauty.get_pic()
