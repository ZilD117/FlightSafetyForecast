import math
import random
import time
class algopack:

    '''

    init: size_1: list [x,y] turbulance map scale
          size_2: list [x,y] flight path map scale
    '''

    def __init__(self, size_1=None):
        self.X = 360
        self.Y = 180

        self.x_amplify = size_1[1]/self.X #float
        self.y_amplify = size_1[0]/self.Y #float
        #rint(self.y_amplify, self.x_amplify)
        #self.ratio_area = self.x_amplify * self.y_amplify

    '''
    input param: turbo_array :2-d array, turbo_array[i][j] = turbulance at specific point
                 flight_path : 1-d array, flight_path[i] = (x,y)
    output type: int
    '''

    # complexity optimization: prefix sum
    def prefixsum(self, turbo_array):
        dp = []
        for i in range(len(turbo_array)):
            dp.append([0]*len(turbo_array[0]))
        dp[0][0] = turbo_array[0][0]
        for row in range(len(dp)):
            for col in range(len(dp[0])):
                if row == 0 and col == 0:
                    continue
                if row == 0 or col == 0:
                    if row == 0:
                        dp[row][col] = dp[row][col-1]+turbo_array[row][col]
                    if col == 0:
                        dp[row][col] = dp[row-1][col]+turbo_array[row][col]
                else:
                    dp[row][col] = dp[row-1][col] + dp[row][col-1] - dp[row-1][col-1] + turbo_array[row][col]
        return dp

    def data_modify(self, turbo_array):
        #time1 = time.time()
        pf_array = self.prefixsum(turbo_array)

        modified_map = []
        for i in range(self.Y):
            modified_map.append([0]*self.X)
        for row in range(len(modified_map)):

            for col in range(len(modified_map[0])):
                #print(row, col)
                real_y = (row + 1) * self.y_amplify
                real_x = (col + 1) * self.x_amplify
                #print(real_x,real_y)
                used_y = math.floor(real_y)
                used_x = math.floor(real_x)
                real_y_1 = row * self.y_amplify
                real_x_1 = col * self.x_amplify
                used_y_1 = math.floor(real_y_1)
                used_x_1 = math.floor(real_x_1)
                area = (used_y-used_y_1)*(used_x-used_x_1)
                if row == 0 and col == 0:
                    temp = pf_array[used_y-1][used_x-1]
                    modified_map[row][col] = temp/area
                    continue
                if row == 0 or col == 0:
                    if row == 0:

                        modified_map[row][col] = (pf_array[used_y-1][used_x-1] -
                                                 pf_array[used_y-1][used_x_1-1])/area
                    if col == 0:
                        modified_map[row][col] = (pf_array[used_y - 1][
                                                     used_x- 1] -
                                                 pf_array[used_y_1 - 1][used_x - 1])/area

                else:
                    modified_map[row][col] = (pf_array[used_y-1][used_x-1] -
                                             pf_array[used_y_1-1][used_x-1]-
                                             pf_array[used_y-1][used_x_1-1]+
                                             pf_array[used_y_1-1][used_x_1-1])/area
        #time2 = time.time()
        return modified_map

    '''
    flight_path: 2-d array form [(x,y)]
    '''
    def turboCalc(self, flight_path,turbo_array):
        #time1 = time.time()
        #print(time1)
        modified_map = self.data_modify(turbo_array)
        turboScore = 0
        totol_length = 0
        for index in range(len(flight_path)-1):
            if flight_path[index][0]>flight_path[index+1][0]:
                start = flight_path[index+1]
                end = flight_path[index]
            else:
                end = flight_path[index+1]
                start = flight_path[index]
            start_x, start_y = start[0]+180, start[1]+90
            end_x, end_y = end[0]+180, end[1]+90
            inclination = (end_y-start_y)/(end_x-start_x)
            begin_y = start_y+inclination*(math.ceil(start_x)-start_x)
            turboScore += math.sqrt((begin_y-start_y)**2+(math.ceil(start_x)-start_x)**2)*modified_map[math.floor(start_y)][math.floor(start_x)]
            totol_length += math.sqrt((begin_y-start_y)**2+(math.ceil(start_x)-start_x)**2)
            for partition in range(math.ceil(start_x),math.floor(end_x)):
                begin_y += inclination
                turboScore += math.sqrt(inclination**2+1)*modified_map[math.ceil(begin_y)][partition]
            turboScore+=math.sqrt(((end_x-math.floor(end_x))**2+(end_y-begin_y)**2))*modified_map[math.floor(end_y)][math.floor(end_x)]
            totol_length += math.sqrt((begin_y-start_y)**2+(math.ceil(start_x)-start_x)**2)
        #time2 = time.time()
        #print(time2)
        return (turboScore/totol_length)*100

    '''
    return a string telling you the severeness of this flight
    param: flight_path, turbo_array, plane_weight(in lbs)
    '''
    def turboRate(self, flight_path, turbo_array, plane_weight):
        turboScore = self.turboCalc(flight_path, turbo_array)

        if plane_weight <= 15500:
            if turboScore <= 16:
                return "Light"
            if 16 < turboScore <= 36:
                return "Moderate"
            if 36 < turboScore <= 64:
                return "Severe"
            if turboScore > 64:
                return "Extreme"
        elif 15500 < plane_weight <= 300000:
            if turboScore <= 20:
                return "Light"
            if 20 < turboScore <= 44:
                return "Moderate"
            if 44 < turboScore <= 79:
                return "Severe"
            if turboScore > 79:
                return "Extreme"
        elif plane_weight > 300000:
            if turboScore <= 24:
                return "Light"
            if 24 < turboScore <= 54:
                return "Moderate"
            if 54 < turboScore <= 96:
                return "Severe"
            if turboScore > 96:
                return "Extreme"


# test_data
if __name__ == "__main__":
    calc = algopack([1400,700])
    lst = []
    for i in range(1400):
        l = []
        for j in range(700):
            l.append(random.random())
        lst.append(l)
    flight_path = [(36.1245, -86.6782), (35.9977, -85.0491), (35.9048, -83.8947), (35.1847, -79.9919),
                   (37.5335, -75.8581), (38.6486, -75.0885), (39.0955, -74.8003), (40.6401, -73.7765)]
    print(calc.turboCalc(flight_path, lst))









