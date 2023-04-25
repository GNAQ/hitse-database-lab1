import os
import sys
import random

CLASS_BEGIN = [0, 1, 121, 241, 361]
CLASS_END = [0, 120, 240, 360, 480]
CLASS_CNT = {i: 0 for i in range(1, 481)}


def proc_male(id_bgn, id_end):
    name_list = []
    with open("./main/data/name_male.txt", encoding="utf-8") as f:
        for line in f:
            name_list.append(line.rstrip())
    random.shuffle(name_list)

    result_list = []
    for i in range(id_bgn, id_end):
        syear = random.randint(1, 4)
        age = random.randint(15, 35)
        clas = random.randint(CLASS_BEGIN[syear], CLASS_END[syear])
        while CLASS_CNT[clas] == 30:
            clas = random.randint(CLASS_BEGIN[syear], CLASS_END[syear])
        CLASS_CNT[clas] += 1
        strclass = f'{syear}N{clas:03d}'
        strid = f'10{syear}{i+1:05d}'

        rstr = strid + ',' + name_list[i] + ',' + \
            '男' + ',' + str(age) + ',' + strclass
        result_list.append(rstr + '\n')

    with open("./main/output/male.csv", "w", encoding="utf-8") as result_file:
        for rstr in result_list:
            result_file.write(rstr)


def proc_female(id_bgn, id_end):
    name_list = []
    with open("./main/data/name_female.txt", encoding="utf-8") as f:
        for line in f:
            name_list.append(line.rstrip())
    random.shuffle(name_list)

    result_list = []
    for i in range(id_bgn, id_end):
        syear = random.randint(1, 4)
        age = random.randint(15, 35)
        clas = random.randint(CLASS_BEGIN[syear], CLASS_END[syear])
        while CLASS_CNT[clas] == 30:
            clas = random.randint(CLASS_BEGIN[syear], CLASS_END[syear])
        CLASS_CNT[clas] += 1
        strclass = f'{syear}N{clas:03d}'
        strid = f'10{syear}{i+1:05d}'

        rstr = strid + ',' + name_list[i] + ',' + \
            '女' + ',' + str(age) + ',' + strclass
        result_list.append(rstr + '\n')

    with open("./main/output/female.csv", "w", encoding="utf-8") as result_file:
        for rstr in result_list:
            result_file.write(rstr)


def proc_course():
    course_list = []
    with open("./main/data/course.txt", encoding="utf-8") as f:
        for line in f:
            course_list.append(line.rstrip())
    random.shuffle(course_list)

    result_list = []
    for i, cname in enumerate(course_list):
        cid = f'C{i+1:03d}'
        chours = random.randint(1, 12) * 8
        credit = chours / 16
        tid = f'T{random.randint(1, 99):02d}'
        rstr = cid + ',' + cname + ',' + \
            f'{credit:.1f}' + ',' + str(chours) + ',' + tid
        result_list.append(rstr + '\n')

    with open("./main/output/course.csv", "w", encoding="utf-8") as c_f:
        for rstr in result_list:
            c_f.write(rstr)


def gen_score():
    selnum = [0, 16, 32, 48, 64]
    stu = []
    sid = []
    tid = [f'C{i+1:03d}' for i in range(0, 999)]
    results = []
    with open("./main/output/male.csv", encoding="utf-8") as f:
        for line in f:
            stu.append(line.rstrip())
    with open("./main/output/female.csv", encoding="utf-8") as f:
        for line in f:
            stu.append(line.rstrip())
    for s in stu:
        sid.append(s[0:8])
    
    for i in sid:
        yr = (int(i) // 100000) % 10
        random.shuffle(tid)
        for j, t in enumerate(tid):
            if j == selnum[yr]:
                break
            sco = random.uniform(0, 100)
            results.append(i + ',' + t + ',' + f'{sco:.2f}' + '\n')
    
    # print(results)
    
    with open("./main/output/score.csv", "w", encoding="utf-8") as f:
        for rstr in results:
            f.write(rstr)

def main():
    # proc_male(0, 5000)
    # proc_female(5000, 10000)

    # proc_course()
    # gen_score()
    pass


if __name__ == "__main__":
    main()
