from services.email import service

if __name__ == '__main__':
    service = service.Service()
    service.run()