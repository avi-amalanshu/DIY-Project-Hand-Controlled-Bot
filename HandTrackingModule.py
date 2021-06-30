import cv2 as cv2
import mediapipe as mp
import time


class handDetector():
	def __init__(self, mode = False, maxhands = 2, detectconf = 0.5, trackconf = 0.5):
		self.mphands = mp.solutions.hands
		self.hands = self.mphands.Hands(mode, maxhands, detectconf, trackconf)
		self.mpdraw = mp.solutions.drawing_utils

	def findHands(self, frame, draw = True):
		framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(framergb)
		if self.results.multi_hand_landmarks:
			for handlms in self.results.multi_hand_landmarks:
				if draw:
					self.mpdraw.draw_landmarks(frame, handlms, self.mphands.HAND_CONNECTIONS)

	def findPosition(self, frame, handNo=0):
		lmlist = []
		if self.results.multi_hand_landmarks:
			myHand = self.results.multi_hand_landmarks[handNo]
			for id, lm in enumerate(myHand.landmark):
				h,w,c = frame.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				lmlist.append([id, cx, cy])
		return lmlist


def main():
	cap = cv2.VideoCapture(0)
	detector = handDetector()
	current_time = 0
	previous_time = 0
	while True:
		retval, frame = cap.read()
		frame = detector.findHands(frame)
		lmlist= detector.findPosition(frame)
		if len(lmlist) != 0:
			print(lmlist)
		current_time = time.time()
		fps = 1 / (current_time - previous_time)
		previous_time = current_time
		cv2.putText(frame, str(int(fps)), (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
					fontScale=1, color=(255, 0, 255), thickness=3)
		cv2.imshow('win1', frame)
		if cv2.waitKey(1) & 0xFF == 27:
			break
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()