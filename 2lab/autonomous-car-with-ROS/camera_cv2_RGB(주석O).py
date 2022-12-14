import cv2 
import time
import numpy as np





def main():
    camera=cv2.VideoCapture(0)
    camera.set(4,1024)
    camera.set(3,768)

    while (camera.isOpened()):
        ret,frame=camera.read() #read는 무조건 2개의 값을 반환한다, ret은 reterval의 약자로 값을 입력받아 True,False로 반환한다. frame은 읽어온 카메라 영상을 담는 변수로 선언
        frame = cv2.flip(frame,1)
        cv2.imshow('frame',frame)
        
        
        #기존 코드
        #slicing=frame[200:768, 0:1024] 
        #cv2.imshow('frames',slicing)
        #문자열 슬라이싱과 같이 frame을 픽셀 단위로 자를 수 있다/
        #세로 데이터를 220~520까지 데이터를 쓰고  가로 데이터는 0~360까지 데이터를 씀(다 쓴단 의미져) 
                
        #수정 코드
        height , _, _=frame.shape
        save_image = frame[int(height/2):,:,:]  #가로로 반을 잘라내는 코드, 기존 코드에서처럼 값을 수시로 변경할 필요성이 없어진다
        save_image = cv2.cvtColor(save_image, cv2.COLOR_BGR2YUV)  #RGB영상을 YUV로 변경
        cv2.imshow('save',save_image)

      
     
        gray=cv2.cvtColor(save_image,cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh=cv2.threshold(blur,130,255,cv2.THRESH_BINARY_INV) #threshold:이미지 BGR에 이진화 처리를해 흑 백을 바꾼다. 영상or이미지,임계점,최대점,cv2.THRESH_BINARY_INV
        #1=white(),0=black
        
        #노이즈 제거 모폴리지기법q
        mask=cv2.erode(thresh,None,iterations=2)
        #erode(이미지변수,필터가 적용되어 저장될 이미지 변수, 반복할 횟수,)
        # object의 영역을 침식시켜 줄여버림(압축) 
        # 원리는 필터를 적용하려는 중심 픽셀에 커널을 가중하여 가장 작은 값을 찾고 그 중 가장 작은 값을
        # 필터의 중심 픽셀에 적용, 이진화되어서 픽셀엔 0,255밖에 없으니 0주위의 값은 커널 크기만큼 0으로 바뀌어 output됨


        #팽창연산
        mask=cv2.dilate(mask,None,iterations=2)

        cv2.imshow('mask',mask)
        #eride와 정반대로 255주위 픽셀을 가중치된 커널의 크기만큼 255로 바꾸어 팽창연산해버림
        
        #윤곽선 검출,contour(등고선)을 출력,contour:동일한 픽셀값을 가지는 영역의 경계선 정보
        contours,_=cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)
        #findContours(입력영상변수.non-zero픽셀을 객체로 간주(white만 객체로 간주) 
        #             (1: 외곽선 개수, CHAIN_APPROX_NONE:모든 컨투어 포인트를 반환)   


        if len(contours)>0:
            c=max(contours,key=cv2.contourArea)
         #countourArea=contours로 둘러쌓인 면적
            #countour들 중 가장 큰 값을 반환
            
            M=cv2.moments(c)
            #moment함수:무게중심, 객체의 면적등과 같은 특성을 계산
            #countours들 에서 moment계산            
            
            # 무게 중심점을 구하는 공식 
            cx= int(M[ 'm10']/M['m00'])
            cy= int(M['m01']/M['m00'])

           # print(cx)
        
            if cx >= 247 and cx <=395:
                print('turn left')
                time.sleep(0)
            elif cx >=483 and cx <=585:
                print("turn right")
                time.sleep(0)
            else:
                print('go')
                time.sleep(0)#

            
            #cv2.line(이미지 변수, 시작점 좌표, 종료점 좌표,색상,선두께)
            #cv2.line은 두좌표를 있는 선을 긋는다.








        if cv2.waitKey(1) ==ord('q'):
            break


    cv2.destroyAllWindows()
 
        


if __name__ =='__main__':
    main()
        

