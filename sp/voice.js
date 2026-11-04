
const micBtn = document.getElementById("micBtn");
const statusText = document.getElementById("status");
const result = document.getElementById("result");
const timerText = document.getElementById("timer");

let mediaRecorder;
let audioChunks = [];
let recordingStream;
let countdownInterval;

const RECORDING_TIME = 10;


// Start recording when microphone is clicked

micBtn.addEventListener("click", startRecording);


async function startRecording() {

    try {

        // Request microphone permission

        recordingStream =
            await navigator.mediaDevices.getUserMedia({
                audio: true
            });

        audioChunks = [];

        // Check supported audio format

        let mimeType = "";

        if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
            mimeType = "audio/webm;codecs=opus";
        } else if (MediaRecorder.isTypeSupported("audio/webm")) {
            mimeType = "audio/webm";
        }

        // Create MediaRecorder

        mediaRecorder = mimeType
            ? new MediaRecorder(recordingStream, { mimeType })
            : new MediaRecorder(recordingStream);

        // Collect audio data

        mediaRecorder.ondataavailable = function(event) {

            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }

        };


        // When recording stops

        mediaRecorder.onstop = async function() {

            clearInterval(countdownInterval);

            micBtn.classList.remove("recording");

            statusText.innerText = "Processing your voice...";
            timerText.innerText = "Please wait";

            const audioBlob = new Blob(audioChunks, {
                type: mediaRecorder.mimeType
            });

            const formData = new FormData();

            formData.append(
                "audio",
                audioBlob,
                "recording.webm"
            );

            try {

                // Send audio to Flask

                const response = await fetch("/transcribe", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || "Transcription failed");
                }

                // Display recognized text

                result.innerText =
                    data.text || "No speech detected.";

                statusText.innerText = "Transcription completed!";
                timerText.innerText = "Ready for your next command";

            } catch (error) {

                statusText.innerText = "Something went wrong.";

                result.innerText = error.message;

                timerText.innerText = "Please try again";

            } finally {

                // Release microphone

                recordingStream.getTracks().forEach(track => {
                    track.stop();
                });

                recordingStream = null;

                micBtn.disabled = false;

            }

        };


        // Start recording

        mediaRecorder.start();

        micBtn.classList.add("recording");
        micBtn.disabled = true;

        statusText.innerText = "Listening... Speak now!";
        result.innerText = "";

        // Countdown display

        let remaining = RECORDING_TIME;

        timerText.innerText =
            "Recording: " + remaining + " seconds remaining";

        countdownInterval = setInterval(() => {

            remaining--;

            timerText.innerText =
                "Recording: " + remaining + " seconds remaining";

            if (remaining <= 0) {
                clearInterval(countdownInterval);
            }

        }, 1000);


        // Automatically stop after 10 seconds

        setTimeout(() => {

            if (mediaRecorder &&
                mediaRecorder.state === "recording") {

                mediaRecorder.stop();

            }

        }, RECORDING_TIME * 1000);


    } catch (error) {

        statusText.innerText =
            "Microphone access failed.";

        result.innerText = error.message;

        if (recordingStream) {

            recordingStream.getTracks().forEach(track => {
                track.stop();
            });

            recordingStream = null;
        }

        micBtn.disabled = false;

    }

}
