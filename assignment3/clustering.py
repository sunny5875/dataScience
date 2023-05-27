import sys
from math import sqrt
import matplotlib.pyplot as plt #표로 보기 위해 사용

class Point:
    def __init__(self, id, x: float, y: float):
        self.id = int(id)
        self.x = x
        self.y = y
        self.label = None # undefined는 None, noise는 0


class DBSCAN:
    def __init__(self, data_sets: list, eps: float, min_pts: int):
        self.data_sets = data_sets
        self.eps = eps
        self.min_pts = min_pts

    # L2 distance
    @staticmethod
    def distance(point1: Point, point2: Point) -> float:
        return sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    # point의 neighbhor를 찾음
    def range_query(self, point: Point) -> list:
        neighbor = [p for p in self.data_sets if self.distance(point, p) <= self.eps]
        neighbor.remove(point) # 자기자신은 삭제
        return neighbor

    def run(self):
        cluster_count = 0
        clusters = []
        for pt in self.data_sets:
            if pt.label is not None:  
                continue

            neighbor = self.range_query(pt)

            if len(neighbor) < self.min_pts:
                pt.label = 0  # Noise로 설정
                continue

            cluster_count += 1  # 새로운 클러스터 생성
            clusters.append([])

            pt.label = cluster_count
            clusters[-1].append(pt)

            seed_set = set(neighbor)

            while seed_set:
                q = seed_set.pop()
                if q.label == 0:  # Noise
                    q.label = cluster_count
                if q.label is not None:
                    continue

                q.label = cluster_count
                clusters[-1].append(q)
                neighbor = self.range_query(q)

                if len(neighbor) >= self.min_pts:
                    seed_set.update(neighbor)

            print('%dth cluster\'s count: %d' % (cluster_count, len(clusters[-1])))

        return clusters


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("argv is not correct! please check argv one more time")
        quit()

    input_file_name = sys.argv[1]
    n = int(sys.argv[2])
    eps = float(sys.argv[3])
    min_pts = int(sys.argv[4])

    # input file 읽기
    data = []
    for d in open(input_file_name, 'r').readlines():
        data.append(Point(*map(float, d.strip().split())))

    # DBSCAN 실행
    dbscan = DBSCAN(data, eps, min_pts)
    print('start clustering')
    clusters = dbscan.run()
    clusters.sort(key=len) 
    if len(clusters) > n:
        print('result: %d clusters, discard %d clusters' % (len(clusters), len(clusters) - n))
        clusters = clusters[len(clusters) - n:]

    count = 0
    for c in clusters:
        c.sort(key=lambda p: p.id)
        f = open('input%d_cluster_%d.txt' % (int(input_file_name[-5]), count), 'w')
        for p in c:
            f.write(str(p.id) + '\n')
            plt.scatter(p.x, p.y, s=1.5, c='C' + str(p.label))
        count += 1
        f.close()
    plt.show()