
import threading
from time import sleep
from random import randint

balance = 0


class Bank:
    lock = threading.Lock()

    def deposit(self):
        global balance
        trans = 0
        for i in range(100):
            trans += 1
            num = randint(50, 500)
            balance = balance + num
            print(f'Пополнение: {num}. Баланс: {balance}.')
            if balance >= 500:
                if self.lock.locked() is True:
                    self.lock.release()
                sleep(0.001)
        return balance

    def take(self):
        global balance
        trans = 0
        for i in range(100):
            trans -= 1
            num = randint(50, 500)
            print(f'Запрос на {num}.')
            if num <= balance:
                balance = balance - num
                print(f'Снятие: {num}. Баланс: {balance}.')
            elif num > balance:
                print(f'Запрос отклонен, недостаточно средств.')
                self.lock.acquire()
        return balance


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {balance}')
