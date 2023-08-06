import pika
import json
MQ_USER='micro'
MQ_PASSWORD='micro'
MQ_VHOST='micro'
MQ_HOST='127.0.0.1'
MQ_PORT=5672
def send_demo():
    credentials = pika.PlainCredentials(MQ_USER, MQ_PASSWORD)  # mq用户名和密码
    # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, virtual_host=MQ_VHOST, credentials=credentials))
    channel = connection.channel()
    # 声明消息队列，消息将在这个队列传递，如不存在，则创建
    result = channel.queue_declare(queue='python-test')

    for i in range(40):
        message = json.dumps({'OrderId': "1000%s" % i})
        # 向队列插入数值 routing_key是队列名
        channel.basic_publish(exchange='', routing_key='python-test', body=message)
        print(message)
    connection.close()

if __name__ == '__main__':
    send_demo()