import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

VELOCITY = 2

dataFileName = "data/" + str(VELOCITY) + "FPSPulltest.csv"
df = pd.read_csv(dataFileName)

def printDistanceTraveled( ):
    global VELOCITY
    global df
    WHEEL_CIRCUMFERENCE = 9.425

    expectedDistanceTraveled = 103.875
    actualDistanceTraveled = df["DIST_HIGH_RES"].iloc[-1]
    errorRate = "{:.2f}".format(abs((expectedDistanceTraveled / actualDistanceTraveled) - 1))

    if VELOCITY == 2:
        startLocation = [60,577,525]
        endLocation = [119,646,607]
        numberOfRollovers = [10,10,10]
        calculatedDistanceTraveled = [0,0,0]

    odoMin = [min(df['WHEEL_A'].to_numpy()), min(df['WHEEL_B'].to_numpy()), min(df['WHEEL_C'].to_numpy())]
    odoMax = [max(df['WHEEL_A'].to_numpy()), max(df['WHEEL_B'].to_numpy()), max(df['WHEEL_C'].to_numpy())]
    for odo in range(3):
        calculatedDistanceTraveled[odo] = numberOfRollovers[odo]*WHEEL_CIRCUMFERENCE
        calculatedDistanceTraveled[odo] += ((odoMax[odo] - startLocation[odo]) + (endLocation[odo] - odoMin[odo])) * (WHEEL_CIRCUMFERENCE / (odoMax[odo] - odoMin[odo]))

    print('Odo start locations: ' + str(startLocation[0]) + ' ' + str(startLocation[1]) + ' ' + str(startLocation[2]))
    print('Odo end locations: ' + str(endLocation[0]) + ' ' + str(endLocation[1]) + ' ' + str(endLocation[2]))
    print('Number of Rollovers: ' + str(numberOfRollovers[0]) + ' ' + str(numberOfRollovers[1]) + ' ' + str(numberOfRollovers[2]))
    print('Tool traveled ' + str(expectedDistanceTraveled) + '" and reported ' + str(actualDistanceTraveled/100) + '". Manual calculation from rollover: ' +
            str(calculatedDistanceTraveled[0]) + '" ODOA | ' + str(calculatedDistanceTraveled[1]) + '" ODOB | ' + str(calculatedDistanceTraveled[2]) + '" ODOC')
    print('Error rate of ' + errorRate + '%')

def graphRawOdoValues( displayRollovers ):
    global df
    global VELOCITY

    lineColor = ['r', 'g', 'b']
    x1 = df['TICKS'].to_numpy()
    y1 = df['WHEEL_A'].to_numpy()
    y2 = df['WHEEL_B'].to_numpy()
    y3 = df['WHEEL_C'].to_numpy()

    if displayRollovers:
        yMin = min(np.concatenate((y1,y2,y3), axis=None))
        yMax = max(np.concatenate((y1,y2,y3), axis=None))
        rolloverLocations = [0, 0, 0]

        if VELOCITY == 2:
            rolloverLocations[0] = [1500, 1000]
            rolloverLocations[1] = [250, 1750]
            rolloverLocations[2] = [500]

        for odo in range(3):
            for i in range(len(rolloverLocations[odo])):
                plt.axvline(x=rolloverLocations[odo][i], c=lineColor[odo])

    plt.scatter(x1, y1, label = "Odo A", c=lineColor[0], s=1)
    plt.scatter(x1, y2, label = "Odo B", c=lineColor[1], s=1)
    plt.scatter(x1, y3, label = "Odo C", c=lineColor[2], s=1)
    plt.xlabel('Tick #')
    plt.ylabel('10-bit Odo Wheel Value')
    plt.legend()
    plt.show()

printDistanceTraveled( )
graphRawOdoValues( False )
