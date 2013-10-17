import math

def polarToCartesian(angle, length):
    return math.cos(math.radians(angle))*length, math.sin(math.radians(angle))*length

def cartesianToPolar(x, y):
    return math.degrees(math.atan(y/x)), math.sqrt((x*x)+(y*y))

def normalizeAngle(angle):
    return 360-angle

def getAngleOfReflection(angle, surfaceAngle):
    return (2*surfaceAngle-angle)%360

def getReducedSpeedByPercent(percent, speed):
    percent, speed = float(percent), float(speed)
    if (100.0-percent)/100.0*speed <= 0.05:
        return 0
    else:
        return (100.0-percent)/100.0*speed
    
def getLength(cartesian):
    return math.sqrt((cartesian[0]*cartesian[0])+(cartesian[1]*cartesian[1]))

def getAngleFromCartesian(cartesian):
    x = cartesian[0]
    y = cartesian[1]
    try:
        print "Try"
        return math.degrees(math.atan(y/x))%360
    except Exception, e:
        print "Exception: "+str(e)
        if x==0:
            if y > 0:
                return 270
            elif y < 0:
                return 90
            else:
                return 0
        elif y==0:
            if x > 0:
                return 0
            elif x < 0:
                return 180
            else:
                return 0
            
def get1DCollisionMomentum(m1, v1, m2, v2):
    m1=float(m1);v1=float(v1);m2=float(m2);v2=float(v2)
    dif = m1-m2
    sum_ = m1+m2
    return (dif*v1+2*m2*v2)/sum_, (2*m1*v1-dif*v2)/sum_
    
def get2DCollisionVector(m1, v1x, v1y, m2, v2x, v2y):
    m1vxf, m2vxf = get1DCollisionMomentum(m1, v1x, m2, v2x)
    m1vyf, m2vyf = get1DCollisionMomentum(m1, v1y, m2, v2y)
    return ((m1vxf, m1vyf), (m2vxf, m2vyf))



def getFinalCollisionPolarVector(m1, v1x, v1y, m2, v2x, v2y):
    value = get2DCollisionVector(m1, v1x, v1y, m2, v2x, v2y)
    polarVector1 = (getAngleFromCartesian((value[0][0], value[0][1])), 
                    math.sqrt((value[0][0]*value[0][0])+(value[0][1]*value[0][1])))

    polarVector2 = (getAngleFromCartesian((value[1][0], value[1][1])), 
                    math.sqrt((value[1][0]*value[1][0])+(value[1][1]*value[1][1])))
    return polarVector1, polarVector2

def getFinalCollisionPolarVectorFromPolarVector(m1, a1, l1, m2, a2, l2):
    vec1 = polarToCartesian(a1, l1)
    vec2 = polarToCartesian(a2, l2)
    value = get2DCollisionVector(m1, vec1[0], vec1[1], m2, vec2[0], vec2[1])
    polarVector1 = (getAngleFromCartesian((value[0][0], value[0][1])), 
                    math.sqrt((value[0][0]*value[0][0])+(value[0][1]*value[0][1])))

    polarVector2 = (getAngleFromCartesian((value[1][0], value[1][1])), 
                    math.sqrt((value[1][0]*value[1][0])+(value[1][1]*value[1][1])))
    return polarVector1, polarVector2


def getFinalPolarVectorFromVector(m1, v1, m2, v2):
    v1x, v1y = v1[0], v1[1]
    v2x, v2y = v2[0], v2[1]
    vec = get2DCollisionVector(m1, v1x, v1y, m2, v2x, v2y)
    result1 = 0
    result2 = 0
    if vec[0][0] >= 0:
        result1 = math.degrees(math.atan(vec[0][1]/vec[0][0]))%360, math.sqrt((vec[0][0]*vec[0][0])+(vec[0][1]*vec[0][1]))
    else:
        result1 = 180+math.degrees(math.atan(vec[0][1]/vec[0][0])), math.sqrt((vec[0][0]*vec[0][0])+(vec[0][1]*vec[0][1]))
        
    if vec[1][0] >= 0:
        result2 = math.degrees(math.atan(vec[1][1]/vec[1][0]))%360, math.sqrt((vec[1][0]*vec[1][0])+(vec[1][1]*vec[1][1]))
    else:
        result2 = 180+math.degrees(math.atan(vec[1][1]/vec[1][0])), math.sqrt((vec[1][0]*vec[1][0])+(vec[1][1]*vec[1][1]))
    return result1, result2

def isLookingAt(p, angle, rect):
    try:
        A = rect[0], rect[1]
        dA = A[0]-p[0], A[1]-p[1]
        PhiA = math.degrees(math.atan(dA[1]/dA[0]))
        if dA[0] < 0:
            PhiA = 180+PhiA
        B = rect[0], rect[1]+rect[3]
        dB = B[0]-p[0], B[1]-p[1]
        PhiB = math.degrees(math.atan(dB[1]/dB[0]))
        if dB[0] < 0:
            PhiB = 180+PhiB
        C = rect[0]+rect[2], rect[1]
        dC = C[0]-p[0], C[1]-p[1]
        PhiC = math.degrees(math.atan(dC[1]/dC[0]))
        if dC[0] < 0:
            PhiC = 180+PhiC
        D = rect[0]+rect[2], rect[1]+rect[3]
        dD = D[0]-p[0], D[1]-p[1]
        PhiD = math.degrees(math.atan(dD[1]/dD[0]))
        if dD[0] < 0:
            PhiD = 180+PhiD
        angles = [PhiA, PhiB, PhiC, PhiD]
        minAngle = min(angles)
        maxAngle = max(angles)
        minAngle1 = minAngle%360
        if abs(minAngle-maxAngle)>180:
            if angle > maxAngle and angle <= minAngle1:
                return True, (minAngle, maxAngle, angle), angles.index(minAngle), angles.index(maxAngle)
            else:
                return False, (minAngle, maxAngle, angle), angles.index(minAngle), angles.index(maxAngle)
        elif minAngle < 0:
            if angle > minAngle and angle < maxAngle:
                return True, (minAngle, maxAngle, angle), angles.index(minAngle), angles.index(maxAngle)
            else:
                return False, (minAngle, maxAngle, angle), angles.index(minAngle), angles.index(maxAngle)
        elif angle > minAngle and angle < maxAngle:
            return True, (minAngle, maxAngle, angle), angles.index(minAngle), angles.index(maxAngle)
        else:
            return False, (minAngle, maxAngle, angle), angles.index(minAngle), angles.index(maxAngle)
    except:
        return False, (0,0), 0, 0
    
def indexToCoordinate(rect, index):
    if index==0:
        return rect.topleft
    elif index==1:
        return rect.bottomleft
    elif index==2:
        return rect.topright
    elif index==3:
        return rect.bottomright
    
    
def getPointOfIntersection(A, B, C, D):
    x1,y1 = A
    x2,y2 = B
    x3,y3 = C
    x4,y4 = D
    d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4);
    if d==0:
        return None
    xi = ((x3-x4)*(x1*y2-y1*x2)-(x1-x2)*(x3*y4-y3*x4))/d
    yi = ((y3-y4)*(x1*y2-y1*x2)-(y1-y2)*(x3*y4-y3*x4))/d
    return xi, yi
    
def intersectionPointDepreciated(A, B, C, D):
    "Be sure to enter floats!"
    x = 0
    m1 = (B[1]-A[1])/(B[0]-A[0])
    try:
        m2 = (D[1]-C[1])/(D[0]-C[0])
    except:
        x = C[0]
        m2 = x
    b1 = A[1]-m1*A[0]
    b2 = C[1]-m2*C[0]
    if x==0:
        x = (b1+b2)/(m1-m2)
    y = (m1*x)-3
    return x, y