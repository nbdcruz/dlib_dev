import streamlit as st

from streamlit_webrtc import ClientSettings, VideoTransformerBase, VideoProcessorBase, RTCConfiguration, WebRtcMode, webrtc_streamer


import av
import cv2

from imutils import face_utils
import dlib

st.title("Streamlit WebRTC using DLIB")
st.write("This is a sample to integrate DLIB :D ")


x = 'shape_predictor_68_face_landmarks.dat'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(x)

class VideoProcessor:
    
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)
        
        for (i, rect) in enumerate(rects):
        	s = predictor(gray, rect)
        	s = face_utils.shape_to_np(s)

        	for(i, y) in s:
        		cv2.circle(img, (i,y), 2, (0, 255, 0), -1)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


    
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)
        
webrtc_ctx = webrtc_streamer(key="dlib", 
                              mode=WebRtcMode.SENDRECV,
                              rtc_configuration=RTC_CONFIGURATION,
                              video_processor_factory=VideoProcessor,
                              media_stream_constraints={"video": True, "audio": False},
                              async_processing=True)


while True:
    if webrtc_ctx.video_transformer:
        result = webrtc_ctx.video_transformer.result_queue.get(timeout=1.0)
        labels_placeholder.table(result)
    else:
        break