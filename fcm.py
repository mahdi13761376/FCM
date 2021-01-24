from random import random
import math
import matplotlib.pyplot as plt


def read_data(data):
    out = []
    for point in data.read().split():
        out.append(point.split(','))
    return out


number_of_clusters = 2
m = 2
file_name = 'sample5.csv'
data = open('datasets/' + file_name)
data_input = read_data(data)
size_of_point = len(data_input[0])
clustering_outputs = {}
center = {}
max_clusters = 10


def is_end(center, new_center, size_of_point):
    res = 0
    threshold = 0.001
    center_size = len(center)
    for i in range(center_size):
        res1 = 0
        for j in range(size_of_point):
            res1 += pow(center[i][j] - new_center[i][j], 2)
        res += pow(res1, 0.5)
    if res < threshold:
        return True
    return False


while True:
    if len(center) == 0:
        for j in range(number_of_clusters):
            for i in range(size_of_point):
                if j not in center.keys():
                    center[j] = []
                center[j].append(random())
    if number_of_clusters not in clustering_outputs:
        clustering_outputs[number_of_clusters] = {}
    datas = []
    for i in range(len(data_input)):
        data = []
        for j in range(number_of_clusters):
            res = 0
            for k in range(number_of_clusters):
                u = 0
                uu = 0
                for l in range(size_of_point):
                    u += pow(center[k][l] - float(data_input[i][l]), 2)
                    uu += pow(center[j][l] - float(data_input[i][l]), 2)
                res += (pow(pow(uu, 0.5) / pow(u, 0.5), 2 / (m - 1)))
            data.append(1 / res)
        datas.append(data)
    new_center = {}
    for i in range(number_of_clusters):
        for j in range(size_of_point):
            u = 0
            uu = 0
            for k in range(len(data_input)):
                u += pow(datas[k][i], m) * float(data_input[k][j])
                uu += pow(datas[k][i], m)
            if i not in new_center.keys():
                new_center[i] = []
            new_center[i].append(u / uu)
    if is_end(center, new_center, size_of_point):
        entropy = 0.0
        for i in range(len(data_input)):
            for j in range(number_of_clusters):
                if datas[i][j] != 0:
                    entropy += (datas[i][j] * math.log(datas[i][j]))
        clustering_outputs[number_of_clusters] = {
            'data': datas,
            'entropy': -entropy / math.log(number_of_clusters),
            'centers': new_center
        }
        datas = []
        center = {}
        if number_of_clusters > max_clusters:
            break
        number_of_clusters += 1
    else:
        center = new_center
best_cluster = 2

for i in clustering_outputs.keys():
    if clustering_outputs[best_cluster]['entropy'] > clustering_outputs[i]['entropy']:
        best_cluster = i
data = clustering_outputs[best_cluster]['data']
centers = list(clustering_outputs[best_cluster]['centers'].values())
print(centers)
clustered = []
for da in data:
    best = 0
    for i in range(len(da)):
        if da[best] < da[i]:
            best = i
    clustered.append(best)
if size_of_point == 2:
    x = [float(x1[0]) for x1 in data_input]
    y = [float(x1[1]) for x1 in data_input]
    xc = [x1[0] for x1 in centers]
    yc = [x1[1] for x1 in centers]
    plt.scatter(x, y, c=clustered)
    plt.scatter(xc, yc, c='blue', s=100)
    plt.show()
print(data)
print(best_cluster)
print(clustering_outputs[best_cluster]['centers'])
cost = 0.0
print(centers[0])
for i in range(len(data_input)):
    c = centers[clustered[i]]
    cost += pow(pow(float(data_input[i][0]) - c[0], 2) + pow(float(data_input[i][1]) - c[1], 2), 0.5)
print(cost)
