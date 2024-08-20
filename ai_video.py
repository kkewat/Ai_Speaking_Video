import streamlit as st
import requests
import time

def animate_video(transcript):
    url = "https://api.synclabs.so/animate"

    payload = {
        "videoUrl": "https://synchlabs-public.s3.us-west-2.amazonaws.com/david_demo_shortvid-03a10044-7741-4cfc-816a-5bccd392d1ee.mp4",
        "transcript": transcript,
        "voiceId": "5f42be17-326d-42b5-81dd-b2baffe60a1c",  # Replace with your desired voice ID
        "model": "wav2lip++",
        # Add other optional parameters as needed
    }

    headers = {
        "x-api-key": "2942acfd-2eb6-4bfb-9d89-213ae1328cc0",  # Replace with your Synclabs API key
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()

def check_video_status(job_id):
    url = f"https://api.synclabs.so/animate/{job_id}"
    headers = {"x-api-key": "2942acfd-2eb6-4bfb-9d89-213ae1328cc0"}
    
    while True:
        response = requests.request("GET", url, headers=headers)
        data = response.json()

        if data["status"] == "COMPLETED":
            return data
        else:
            time.sleep(10)  # Adjust polling interval as needed
            st.info("Video creation is in progress...")

def main():
    st.title("Ai Speaking Video Animation")

    transcript = st.text_area("Transcript")

    if st.button("Animate"):
        response = animate_video(transcript)
        job_id = response["id"]

        video_data = check_video_status(job_id)

        st.success("Video creation is complete!")
        st.write("Video URL:", video_data["videoUrl"])

        # Display video using streamlit.video (if supported)
        st.video(video_data["videoUrl"])

if __name__ == "__main__":
    main()
