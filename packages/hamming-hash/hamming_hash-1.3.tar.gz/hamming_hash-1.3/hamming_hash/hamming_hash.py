import hashlib
import time
import binascii
import matplotlib.pyplot as plt
class hamming_hash():
    errors = []
    index = []
    stat = []
    dist = []
    mode = ''
    
    def init(self):
        self.errors = []
        self.index = []
        self.stat = []
        self.dist = []
        mode = ''
        
    def statistika(self,count,index,errors,dist,time1,time2,graph):
        print('________________________________________________Статистика_______________________________________________')
        plt.figure(figsize=(15,10))
        plt.plot(self.index,self.errors, graph, label='% изменения')
        plt.xlabel('Индекс ошибки')
        plt.ylabel('% изменения')
        plt.legend()
        plt.show()
        print('Кол-во ошибок:{}'.format(count))
        print('Индексы ошибок в битовой последовательности:{}'.format(index))
        print('Процент изменения:{}'.format(errors))
        print('Расстояние Хэмминга:{}'.format(dist))
        print('Время хеширования изначальной последовательности:{}'.format(time1))
        print('Время хеширования измененной последовательности:{}'.format(time2))
        
    def array_statistika(self,count,index,errors,dist,time1,time2,graph):
        print('________________________________________________Статистика_______________________________________________')
        plt.figure(figsize=(15,10))
        plt.plot(self.index,self.errors, graph, label='% изменения')
        plt.xlabel('Кол-во ошибок')
        plt.ylabel('% изменения')
        plt.legend()
        plt.show()
        print('Кол-во ошибок:{}'.format(index))
        print('Процент изменения:{}'.format(errors))
        print('Расстояние Хэмминга:{}'.format(dist))
        print('Время хеширования изначальной последовательности:{}'.format(time1))
        print('Время хеширования измененной последовательности:{}'.format(time2))
        
    def dif_statistika(self,count,index,errors,dist,time1,time2,graph):
        print('________________________________________________Статистика_______________________________________________')
        plt.figure(figsize=(15,10))
        plt.plot(len(self.index),self.errors, graph, label='% изменения')
        plt.xlabel('Кол-во ошибок')
        plt.ylabel('% изменения')
        plt.legend()
        plt.show()
        print('Кол-во ошибок:{}'.format(count))
        print('Индексы ошибок в битовой последовательности:{}'.format(index))
        print('Процент изменения:{}'.format(errors))
        print('Расстояние Хэмминга:{}'.format(dist))
        print('Время хеширования изначальной последовательности:{}'.format(time1))
        print('Время хеширования измененной последовательности:{}'.format(time2))
    
    def text_to_bits(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    def text_from_bits(self, bits, encoding='utf-8', errors='ignore'):
        n = int(bits, 2)
        return self.int2bytes(n).decode(encoding, errors)

    def int2bytes(self, i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

    def change_bin(self, s,mas):
        text = ''
        for i in range(len(s)):
            if i in mas:
                if s[i] == '0':
                    text += '1'
                else:
                    text += '0'
            else:
                text += s[i]
        return text

    def hamming2(self, s1, s2):
        dist = 0
        errors = []
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                errors.append(i)
                dist += 1
        return errors, dist
    
    def statist(self, s, mode, index=1, many_index=[1,2], first_index=0, second_index=100, steps = 1, dif_index=[1,2]):
        self.init()
        self.mode = mode
        
        if mode == 'single_index_bit':
            tim = time.time()
            second = hashlib.sha256((self.text_from_bits(self.change_bin(self.text_to_bits(s),[index]))).encode('utf-8')).hexdigest().upper()
            self.stat.append(time.time()-tim)

            tim = time.time()
            first = hashlib.sha256(s.encode('utf-8')).hexdigest().upper()
            self.stat.append(time.time()-tim)

            ham = self.hamming2(self.text_to_bits(first),self.text_to_bits(second))
            self.errors.append(ham[1]/len(self.text_to_bits(second)))
            self.dist.append(ham[1])
            self.index.append(index)
            print('Вычисление для mode={} успешно выполнены.'.format(mode))
            
        elif mode == 'many_index_bit':
            for i in many_index:
                tim = time.time()
                second = hashlib.sha256((self.text_from_bits(self.change_bin(self.text_to_bits(s),[i]))).encode('utf-8')).hexdigest().upper()
                self.stat.append(time.time()-tim)

                tim = time.time()
                first = hashlib.sha256(s.encode('utf-8')).hexdigest().upper()
                self.stat.append(time.time()-tim)

                ham = self.hamming2(self.text_to_bits(first),self.text_to_bits(second))
                self.errors.append(ham[1]/len(text_to_bits(second)))
                self.dist.append(ham[1])
                self.index.append(i)
            print('Вычисление для mode={} успешно выполнены.'.format(mode))
            
        elif mode == 'array_index_bit':
            for i in range(first_index,second_index,steps):
                tim = time.time()
                second = hashlib.sha256((self.text_from_bits(self.change_bin(self.text_to_bits(s),range(i)))).encode('utf-8')).hexdigest().upper()
                self.stat.append(time.time()-tim)

                tim = time.time()
                first = hashlib.sha256(s.encode('utf-8')).hexdigest().upper()
                self.stat.append(time.time()-tim)

                ham = self.hamming2(self.text_to_bits(first),self.text_to_bits(second))
                self.errors.append(ham[1]/len(self.text_to_bits(second)))
                self.dist.append(ham[1])
                try:
                    self.index.append(range(i)[-1]+1)
                except:
                    self.index.append(0)
            print('Вычисление для mode={} успешно выполнены.'.format(mode))
            
        elif mode == 'diff_index_bit':
            tim = time.time()
            second = hashlib.sha256((self.text_from_bits(self.change_bin(self.text_to_bits(s),dif_index))).encode('utf-8')).hexdigest().upper()
            self.stat.append(time.time()-tim)

            tim = time.time()
            first = hashlib.sha256(s.encode('utf-8')).hexdigest().upper()
            self.stat.append(time.time()-tim)

            ham = hamming2(self.text_to_bits(first),self.text_to_bits(second))
            self.errors.append(ham[1]/len(self.text_to_bits(second)))
            self.dist.append(ham[1])
            self.index = dif_index
            print('Вычисление для mode={} успешно выполнены.'.format(mode))
    
    
    def show_statist(self):
        if self.mode == 'single_index_bit':
            self.statistika(count=len(self.errors),index=self.index,errors=self.errors,dist=self.dist,time1=self.stat[0],time2=self.stat[1],graph='bo')
        elif self.mode == 'many_index_bit':
            self.statistika(count=len(self.errors),index=self.index,errors=self.errors,dist=self.dist,time1=self.stat[0],time2=self.stat[1],graph='b')
        elif self.mode == 'array_index_bit':
            self.array_statistika(count=len(self.errors),index=self.index,errors=self.errors,dist=self.dist,time1=self.stat[0],time2=self.stat[1],graph='b')
        elif self.mode == 'diff_index_bit':
            self.dif_statistika(count=len(self.index),index=self.index,errors=self.errors,dist=self.dist,time1=self.stat[0],time2=self.stat[1],graph='bo')