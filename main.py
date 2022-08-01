import docker
import CloudFlare
import streamlit as st
import sys

#启动方式是：
#streamlit run main.py

# Initialize Cloudflare API client
#token是你的api_key
cf = CloudFlare.CloudFlare(
    email="lemonhall2012@qq.com",
    token="xxxxxxxxxxxxxxxxxx"
)

#更新ipv6地址的函数
#hostname="docker.lemonhall.me"
#ipv6_address=""
def dns_updater(hostname,ipv6_address):
    # Get zone ID (for the domain). This is why we need the API key and the domain API token won't be sufficient
    zone = ".".join(hostname.split(".")[-2:]) # domain = test.mydomain.com => zone = mydomain.com
    zones = cf.zones.get(params={"name": zone})

    if len(zones) == 0:
        print(f"Could not find CloudFlare zone {zone}, please check domain {hostname}")
        sys.exit(2)

    zone_id = zones[0]["id"]

    # Fetch existing A record
    aaaa_records = cf.zones.dns_records.get(zone_id, params={"name": hostname, "type": "AAAA"})

    if len(aaaa_records): # Have an existing record
        print("Found existing record, updating...")
        a_record = aaaa_records[0]
        # Update record & save to cloudflare
        a_record["content"] = ipv6_address
        cf.zones.dns_records.put(zone_id, a_record["id"], data=a_record)
    else: # No existing record. Create !
        print("Record doesn't existing, creating new record...")
        a_record = {}
        a_record["type"] = "AAAA"
        a_record["name"] = hostname
        a_record["ttl"] = 60 # 1 == auto
        a_record["content"] = ipv6_address
        cf.zones.dns_records.post(zone_id, data=a_record)

#响应真实注册动作的一个代理吧，你就这样考虑
def reg_it(name,ip):
	hostname= name + ".lemonhall.me"
	dns_updater(hostname,ip)
	st.success("成功注册到 CloudFlare 主机 :  "+name+".lemonhall.me 将可用")


#拿到docker的client
client = docker.from_env()
cons = client.containers.list()

st.set_page_config(page_title="Docker dns注册管理页面", page_icon="random", layout="wide", initial_sidebar_state="auto", menu_items=None)
st.header('Docker dns 注册管理页面')
st.markdown("____")

# # Show users table 
colms = st.columns((1, 2, 2, 1))
fields = ["序号", '容器名', 'ip地址', "动作"]
for col, field_name in zip(colms, fields):
    # header
    col.write(field_name)

n=0
for c in cons:
	if(c.status=="running"):
		col1, col2, col3, col4 = st.columns((1, 2, 2, 1))
		col1.write(n)  # index
		col2.write(c.name)  # 容器名
		col3.write(c.attrs['NetworkSettings']['GlobalIPv6Address'])  # IP地址
		button_phold = col4.empty()  # create a placeholder
		do_action = button_phold.button("注册该容器", key=n,on_click=reg_it,args=(c.name,c.attrs['NetworkSettings']['GlobalIPv6Address']))
		n=n+1