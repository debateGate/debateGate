from app.main import main
if __name__ == '__main__':
    if main.config["DEBUG"] == True:
        main.run(host="localhost", ssl_context=('./ssl.crt', './ssl.key'))
    else:
        main.run()
