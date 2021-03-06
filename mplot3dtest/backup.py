import pandas as pd
import math
import matplotlib.pyplot as plt


def display_graph(index):
    x = [math.cos(yawList[index]) * math.cos(pitchList[index]),
         math.sin(yawList[index]) * math.cos(pitchList[index]),
         -1 * math.sin(pitchList[index])]

    y = [math.cos(yawList[index]) * math.sin(pitchList[index]) * math.sin(rollList[index]) - math.sin(yawList[index]) * math.cos(rollList[index]),
         math.sin(yawList[index]) * math.sin(pitchList[index]) * math.sin(rollList[index]) + math.cos(yawList[index]) * math.cos(rollList[index]),
         math.cos(pitchList[index]) * math.sin(rollList[index])]

    z = [math.cos(yawList[index]) * math.sin(pitchList[index]) * math.cos(rollList[index]) + math.sin(yawList[index]) * math.sin(rollList[index]),
         math.sin(yawList[index]) * math.sin(pitchList[index]) * math.cos(rollList[index]) - math.cos(yawList[index]) * math.sin(rollList[index]),
         math.cos(pitchList[index]) * math.cos(rollList[index])]

    #print('Time: {} seconds\nX axis: {}\nY axis: {}\nZ axis: {}'.format(sum(time[0:index]), x, y, z))

    ax.plot([0, x[0]], [0, x[1]], [0, x[2]], color='r', label='X axis')
    ax.plot([0, y[0]], [0, y[1]], [0, y[2]], color='g', label='Y axis')
    ax.plot([0, z[0]], [0, z[1]], [0, z[2]], color='b', label='Z axis')
    ax.legend()
    plt.show()


def graph_coordinates():
    initialVelocity = [0, 0, 0]
    coords = [(0, 0, 0)]
    #initialDistance = [0, 0, 0]
    initXdir, initYdir, initZdir = [0, 0, 0], [0, 0, 0], [0, 0, 0]
    for i in range(len(time)):
        averageVelocity = [((accX[i] - firstAcc[0]) * time[i] + 2 * initialVelocity[0])/2, ((accY[i] - firstAcc[1]) * time[i] + 2 * initialVelocity[1])/2, ((accZ[i] - firstAcc[2]) * time[i] + 2 * initialVelocity[2])/2]
        initialVelocity = [(accX[i] - firstAcc[0]) * time[i] + initialVelocity[0], (accY[i] - firstAcc[1]) * time[i] + initialVelocity[1], (accZ[i] - firstAcc[0]) * time[i] + initialVelocity[2]]
        distanceMoved = [averageVelocity[0] * time[i], averageVelocity[1] * time[i], averageVelocity[2] * time[i]]

        xDirection = [math.cos(yawList[i]) * math.cos(pitchList[i]) * distanceMoved[0] - initXdir[0] * distanceMoved[0],
                      math.sin(yawList[i]) * math.cos(pitchList[i]) * distanceMoved[0] - initXdir[1] * distanceMoved[0],
                      math.sin(pitchList[i]) * distanceMoved[0] - initXdir[2] * distanceMoved[0]]
        yDirection = [(-1 * math.cos(yawList[i]) * math.sin(pitchList[i]) * math.sin(rollList[i]) - math.sin(yawList[i]) * math.cos(rollList[i])) * distanceMoved[1] - initYdir[0] * distanceMoved[1],
                      (-1 * math.sin(yawList[i]) * math.sin(pitchList[i]) * math.sin(rollList[i]) + math.cos(yawList[i]) * math.cos(rollList[i])) * distanceMoved[1] - initYdir[1] * distanceMoved[1],
                      math.cos(pitchList[i]) * math.sin(rollList[i]) * distanceMoved[1] - initYdir[2] * distanceMoved[1]]
        zDirection = [(-1 * math.cos(yawList[i]) * math.sin(pitchList[i]) * math.cos(rollList[i]) + math.sin(yawList[i]) * math.sin(rollList[i])) * distanceMoved[2] - initZdir[0] * distanceMoved[2],
                      (math.sin(yawList[i]) * math.sin(pitchList[i]) * math.cos(rollList[i]) - math.cos(yawList[i]) * math.sin(rollList[i])) * distanceMoved[2] - initZdir[1] * distanceMoved[2],
                      math.cos(pitchList[i]) * math.sin(rollList[i]) * distanceMoved[2] - initZdir[2] * distanceMoved[2]]

        coords.append((coords[i][0] + xDirection[0] + yDirection[0] + zDirection[0], coords[i][1] + xDirection[1] + yDirection[1] + zDirection[1], coords[i][2] + xDirection[2] + yDirection[2] + zDirection[2]))
        if i == 1:
            initXdir = [xDirection[0]/distanceMoved[0], xDirection[1]/distanceMoved[0], xDirection[2]/distanceMoved[0]]
            initYdir = [yDirection[0]/distanceMoved[1], yDirection[1]/distanceMoved[1], yDirection[2]/distanceMoved[1]]
            initZdir = [zDirection[0]/distanceMoved[2], zDirection[1]/distanceMoved[2], zDirection[2]/distanceMoved[2]]
            #initialDistance = [coords[i][0] + xDirection[0] + yDirection[0] + zDirection[0], coords[i][1] + xDirection[1] + yDirection[1] + zDirection[1], coords[i][2] + xDirection[2] + yDirection[2] + zDirection[2]]
        #coords.append((coords[i][0] + xDirection[0] + yDirection[0] + zDirection[0], coords[i][1] + xDirection[1] + yDirection[1] + zDirection[1], coords[i][2] + xDirection[2] + yDirection[2] + zDirection[2]))
    print(coords)
    ax.plot([x[0] for x in coords], [x[1] for x in coords], [x[2] for x in coords])
    ax.legend()
    plt.show()


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    dimension = 0.25
    ax.set_xlim(-1 * dimension, dimension)
    ax.set_ylim(-1 * dimension, dimension)
    ax.set_zlim(-1 * dimension, dimension)
    pitchList = []
    rollList = []
    yawList = []
    data = pd.read_excel('TestData.xlsx').values
    time = [x[0] for x in data]
    accX = [x[1]/9.8 for x in data]
    accY = [x[2]/9.8 for x in data]
    accZ = [x[3]/9.8 for x in data]
    gyroX = [x[4] for x in data]
    gyroY = [x[5] for x in data]
    gyroZ = [x[6] for x in data]
    firstAcc = [accX[0], accY[0], accZ[0]]
    totalTime = 0
    firstPitch = 180 * math.atan(accX[0] / math.pow(accY[0] * accY[0] + accZ[0] * accZ[0], 0.5)) / math.pi
    firstRoll = 180 * math.atan(accY[0] / math.pow(accX[0] * accX[0] + accZ[0] * accZ[0], 0.5)) / math.pi
    firstYaw = 180 * math.atan(accZ[0] / math.pow(accX[0] * accX[0] + accZ[0] * accZ[0], 0.5)) / math.pi
    #pitch, roll, yaw = 0, 0, 0
    for i in range(len(time)):
        totalTime += time[i]
        pitch = (180 * math.atan(accX[i] / math.pow(accY[i] * accY[i] + accZ[i] * accZ[i], 0.5)) / math.pi) - firstPitch
        roll = (180 * math.atan(accY[i] / math.pow(accX[i] * accX[i] + accZ[i] * accZ[i], 0.5)) / math.pi) - firstRoll
        yaw = (180 * math.atan(accZ[i] / math.pow(accX[i] * accX[i] + accZ[i] * accZ[i], 0.5)) / math.pi) - firstYaw
        #roll += (gyroX[i] - gyroX[0]) * time[i]
        #yaw += (gyroY[i] - gyroY[0]) * time[i]
        #pitch += (gyroZ[i] - gyroZ[0]) * time[i]
        pitchList.append(pitch * 2 * math.pi / 360)
        rollList.append(roll * 2 * math.pi / 360)
        yawList.append(yaw * 2 * math.pi / 360)
        #print(f'{totalTime}, {pitch}, {roll}, {yaw}')
        print(f'{totalTime}, {accX[i]}, {accY[i]}, {accZ[i]}')
    #print(accX)
    #print(accY)
    #print(accZ)
    #myIndex = int(input(f"Enter array index from range 0 to {len(time)}: "))
    #display_graph(myIndex)
    graph_coordinates()
