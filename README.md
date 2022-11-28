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

## 分别构建

python >= 3.8

1. 在tree_hust/settings.py中修改数据库配置 DATABASE = ...
   - NAME: 数据库名称，需要提前在mysql中创建一个新的database
   - PASSWORD: mysql数据库的密码
2. 命令行中运行下列命令构建后端 (如果是linux系统, 可能是python3)
   1. `cd backend`
   2. `python -m pip install --upgrade pip`
   3. `python -m pip install -r requirements.txt`
   4. `python manage.py migrate User`
   5. `python manage.py migrate Post`
   6. `python manage.py migrate`
   7. `python manage.py runserver`
3. 命令行中运行下列命令构建前端 (如果是linux系统, 可能是python3)
   1. `cd ../website`
   2. `npm install`
   3. `npm run build` 生成build\文件夹, 放到项目的主目录下
   4. `npm start`
4. 将.nginx.conf和build加到nginx配置中

## docker构建

```shell
# 更新apt-get
sudo apt-get remove docker \
               docker-engine \
               docker.io

sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo apt-get update

# 安装docker
sudo apt-get install docker-ce docker-ce-cli containerd.io

# 启动docker
sudo systemctl enable docker
sudo systemctl start docker

# 建立docker用户组
sudo groupadd docker
sudo usermod -aG docker $USER
# 推出终端并重新登录

docker-compose up
```

---

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
