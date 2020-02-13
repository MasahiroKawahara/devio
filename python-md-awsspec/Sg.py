#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ライブラリ インポート
import boto3
import pandas as pd


# In[ ]:


# boto3 client
client = boto3.client('ec2')


# In[ ]:


# 名前タグ取得用関数
def get_name_from_tags(tags):
    tags_filter = [t['Value'] for t in tags if t['Key'] == "Name"]
    if tags_filter:
        return tags_filter[0]
    else:
        return ""


# In[ ]:


# VPC　ID <--> VPC Name 対応関係の情報取得
vpcs = client.describe_vpcs()['Vpcs']


# In[ ]:


df_vpcs = pd.DataFrame(
    [
        [vpc['VpcId'], get_name_from_tags(vpc['Tags'])]
        for vpc in vpcs
    ],
    columns=['VpcId', 'Name']
)


# In[ ]:


# VPC Name 取得用関数
def get_vpc_name(vpcid):
    df_filter = df_vpcs[df_vpcs['VpcId'] == vpcid]
    if df_filter.empty:
        return ''
    else:
        return df_filter.iloc[0]['Name']


# In[ ]:


# Security Groups 情報取得
sgs = client.describe_security_groups()['SecurityGroups']


# ## Security Groups 一覧

# In[ ]:


sgs.sort(key=lambda sg:sg['VpcId'])
df_sgs = pd.DataFrame(
    [
        [
            sg['GroupName'],
            sg['GroupId'],
            "{} ({})".format(sg['VpcId'], get_vpc_name(sg['VpcId'])),
            sg['Description']
        ]
        for sg in sgs
    ],
    columns=['GroupName', 'GroupId', "VPC", "Description"]
)
df_sgs.index = df_sgs.index + 1


# In[ ]:


# display
print('## SecurityGroups 一覧')
print(df_sgs.to_markdown())


# ## 各 Security Group Rules

# In[ ]:


# Security Group の名前取得用
def get_sg_name(sgid):
    df_filter = df_sgs[df_sgs['GroupId'] == sgid]
    if df_filter.empty:
        return ''
    else:
        return df_filter.iloc[0]['GroupName']


# In[ ]:


# Ip Protocol 表示用
def parse_ip_protocol(ip_protocol):
    if ip_protocol == '-1':
        return 'ALL'
    else:
        return ip_protocol


# In[ ]:


# Port Range 表示用
def parse_port_range(ip_protocol, from_port, to_port):
    if ip_protocol == '-1':
        return 'ALL'
    elif ip_protocol == 'tcp' or ip_protocol == 'udp':
        # TCP, UDP
        if from_port == to_port:
            return "{}".format(from_port)
        else:
            return "{} - {}".format(from_port, to_port)
    else:
        # ICMP, ICMPv6
        icmp_type = 'ALL' if from_port == -1 else from_port
        icmp_code = 'ALL' if to_port == -1 else to_port
        return "Type:{} Code:{}".format(icmp_type, icmp_code)


# In[ ]:


print('## 各 SecurityGroup ルール')
for sg in sgs:
    # get rules
    buffer = []
    for perms in sg['IpPermissions']:
        # ip protocol, port range
        ip_protocol = parse_ip_protocol(perms.get('IpProtocol'))
        port_range = parse_port_range(
            perms.get('IpProtocol'),
            perms.get('FromPort'),
            perms.get('ToPort')
        )
        for ip_range in perms['IpRanges']:
            buffer.append([
                ip_protocol,
                port_range,
                ip_range.get('CidrIp'),
                ip_range.get('Description')
            ])
        for ip_range in perms['Ipv6Ranges']:
            buffer.append([
                ip_protocol,
                port_range,
                ip_range.get('CidrIpv6'),
                ip_range.get('Description')
            ])
        for group in perms['UserIdGroupPairs']:
            group_id = group['GroupId']
            buffer.append([
                ip_protocol,
                port_range,
                "{} ({})".format(group_id, get_sg_name(group_id)),
                group.get('Description')
            ])
    df_rules = pd.DataFrame(
        buffer,
        columns=['IpProtocol', 'PortRange', 'Source', 'Description']
    ).sort_values(by=['IpProtocol', 'PortRange', 'Source']).reset_index(drop=True)
    df_rules.index = df_rules.index + 1
    # display
    print("### {} (vpc:{})".format(sg['GroupName'], get_vpc_name(sg['VpcId'])))    
    if df_rules.empty:
        print('- no rules')
    else:
        print(df_rules.to_markdown())
    print('')

