<img width="1331" alt="image" src="https://user-images.githubusercontent.com/637919/182259936-3e35f931-de8b-4182-9098-64aed5e48a9d.png">
<img width="1375" alt="image" src="https://user-images.githubusercontent.com/637919/182259956-8e202e3b-158c-47a1-91b2-311c3ff6cef9.png">

### 启动一个环境

mkdir ~/.venvs
mkdir ~/.venvs/docker_dns_reg

python3 -m venv ~/.venvs/docker_dns_reg
source ~/.venvs/docker_dns_reg/bin/activate


### 安装依赖

pip install docker
pip install CloudFlare
pip install streamlit

### 开始撸

记得用
streamlit run main.py
来启动

稍后估计得做生产化

<img width="1008" alt="image" src="https://user-images.githubusercontent.com/637919/182260069-660495b7-a27b-49d7-aa15-1d7396906b4e.png">

主逻辑其实就只有这么一点点

有技巧的其实就是那个streamlit的foreach循环渲染，可以方便的手动决定哪些容器注册到dns去，当然，取名字记得别重复
