# hust_tree_hollow

快速原型系统：https://modao.cc/app/YBB8vnYLrir35n8H838nVr

以下为主要界面：

### 主界面
![](./icon/main.png)

### 帖子
![](./icon/post.png)

### 设置
![](./icon/settings.png)

# 使用手册

python 版本最好3.8以上

1. 在tree_hust/settings.py中修改数据库配置 DATABASE = ...
   - NAME: 数据库名称，需要提前在mysql中创建一个新的database
   - PASSWORD: mysql数据库的密码
   - 别的应该不需要变
2. 命令行中运行下列命令 (如果是linux系统, 可能是python3)
   1. `python -m pip install --upgrade pip`
   2. `python -m pip install -r requirements.txt`
   3. `python manage.py migrate`
   4. `python manage.py runserver`
3. 在 `http://localhost:8000/`处打开