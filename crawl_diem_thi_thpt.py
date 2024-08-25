import requests
import pandas as pd
import numpy as np
import aiohttp
import asyncio
import nest_asyncio
import time
from bs4 import BeautifulSoup

url = 'https://api-university-2022.beecost.vn/university/lookup_examiner?id='
cum_thi = []
 for i in range(1000001, 70000001, 1000000):
     response = requests.get(url+str(i))
     if response.status_code == 200:
         cum_thi.append({
         'ma_cum': int(i/1000000),
         'cum': response.json().get('data', {}).get('test_location')
         })
 cum_thi = pd.DataFrame(cum_thi)

cum_thi = pd.read_csv('D:/Downloads/diem_thi_2024/cum_thi.csv')
# # Áp dụng nest_asyncio để có thể chạy vòng lặp sự kiện bên trong một vòng lặp đã tồn tại
nest_asyncio.apply()

sem = asyncio.Semaphore(10000)  # Giới hạn số lượng yêu cầu đồng thời

async def fetch(session, id):
    url = f'https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/2023/{id}.html'
    try:
        async with sem:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    record = soup.select_one('.resultSearch__right > table > tbody')
                    if record != None:
                        rows = record.find_all('tr')
                        scores = {}
                        scores['id'] = id
                        for row in rows:
                            columns = row.find_all('td')
                            if len(columns) == 2:
                                key = columns[0].get_text(strip=True)
                                value = columns[1].get_text(strip=True)
                                scores[key] = value
                        
                        data.append(scores)
                        print(f'id: {id}')
                        duration = time.perf_counter() - start
                        print(f"Total time: {duration} s")
                        return True
                    else:
                        return False
                    record = None
                else:
                    print(f'Error: {response.status} for id: {id}')
                    duration = time.perf_counter() - start
                    print(f"Total time: {duration} s")
                    return False

    except Exception as e:
        print(f'Exception occurred: {e} for id: {id}')
        return False

async def main():
    data = []
    max_errors = 400
    error_count = 0

    async with aiohttp.ClientSession() as session:
        for i in cum_thi['ma_cum']:
            id = i*1000000 +1
            ids = []
            while True:
                if i < 10:
                    id_str = '0' + str(id)
                else:
                    id_str = str(id)

                ids.append(id_str)
                id += 1

                if len(ids) >= 1000:
                    # Chia thành các nhóm yêu cầu
                    tasks = [fetch(session, id_str) for id_str in ids]
                    results = await asyncio.gather(*tasks)
                    
                    # Kiểm tra số lượng lỗi liên tục
                    error_count = results.count(False)
                    if error_count > max_errors:
                        print('Too many errors, moving to next index')
                        break

                    ids = []  # Xóa danh sách IDs sau khi hoàn thành nhóm

            # Đảm bảo tất cả các tác vụ đã được hoàn thành
            if ids:
                tasks = [fetch(session, id_str) for id_str in ids]
                results = await asyncio.gather(*tasks)

                # Kiểm tra số lượng lỗi liên tục
                error_count = results.count(False)
                if error_count > max_errors:
                    print('Too many errors, moving to next index')


start = time.perf_counter()
data = []
asyncio.run(main())
#await main()   #Chạy bằng Spyder hoặc jupyter
data = pd.DataFrame(data)
data.to_csv("data.csv", index = False)
