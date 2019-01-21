from flask import render_template, jsonify

from Src.utils import log as logger
from Src.utils.decorator import write_operate_log
from Src.utils.init_app import create_app

app = create_app()

logger.init("log")


@app.route(r"/v1/bms/index.html")
def index():
    return render_template("nia_web/index.html")


@app.route(r"/test/")
@write_operate_log(action_cn="测试", action_en="test")
def test():
    return {"code": 200, "msg": "aaa"}


if __name__ == '__main__':
    logger.info("启动并初始化成功")
    app.run(port=5001)
