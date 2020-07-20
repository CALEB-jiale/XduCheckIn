from flask import Flask, escape, request
import file_util

app = Flask("XDU Check In")

dir_data = 'data'


def init():
    file_util.create_dir_if_not_exist(dir_data)


if __name__ == "__main__":
    init()

    app.run(host='0.0.0.0', port='8080')
