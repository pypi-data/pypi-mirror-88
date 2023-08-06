from sanic import Sanic
from sanic.response import json
from wk.extra.linux import get_local_ip

print(get_local_ip())
app = Sanic()

@app.route('/')
async def demo(request):
    msg = {'message': 'Welcom to 猿人学Python'}
    return json(msg, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)