import os
import random
import time
from bs4 import BeautifulSoup
import requests


def get_name_link():
    url = "http://www.resgain.net/xmdq.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    name_links = []
    for s in soup.find_all(attrs={'class': 'btn btn2'}):
        name_links.append("https://www.resgain.net/" + s.get('href'))
    return name_links


def get_name_list():
    url = "http://www.resgain.net/xmdq.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    name_list = []
    for s in soup.find_all(attrs={'class': 'btn btn2'}):
        name_list.append(s.text.split("姓")[0])
    return name_list


def get_data(url, gender: int):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    rec_file_name = "name_" + ("male" if (gender == 1) else "female") + ".txt"

    with open(rec_file_name, "a", encoding='utf-8') as nf:
        for s in soup.select(".cname"):
            # print("Get cname as", str(s.contents[0])[1:])
            nf.write(str(s.contents[0])[1:] + '\n')


def main():
    del_old = input("Input [Y] to delete old .txt file:")
    if (del_old == 'Y'):
        os.remove("name_male.txt")
        os.remove("name_female.txt")

    name_link_list = get_name_link()
    first_name_list = get_name_list()
    print("Get Name Links done.")

    current_count = 0
    total_count = len(name_link_list)
    for name_link in name_link_list:
        url_male = name_link + "&gender=1&wx1=&wx2="
        url_female = name_link + "&gender=0&wx1=&wx2="
        # print("Use name link {} as:\nMale: {}\nFemale: {}"
        #       .format(name_link, url_male, url_female))
        # input("Let's GO?")
        print("Progress: {} of {}: {}"
              .format(current_count + 1, total_count, first_name_list[current_count]))
        get_data(url_male, 1)
        t = random.randint(1, 3)
        time.sleep(t)
        get_data(url_female, 0)
        t = random.randint(1, 3)
        time.sleep(t)
        current_count += 1
        if (current_count % 10 == 0):
            time.sleep(15)


if __name__ == "__main__":
    main()
