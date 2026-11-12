
const micBtn = document.getElementById("micBtn");
const statusText = document.getElementById("status");
const result = document.getElementById("result");
const timerText = document.getElementById("timer");

let mediaRecorder;
let audioChunks = [];
let recordingStream;
let countdownInterval;
let recordingTimeout;

const RECORDING_TIME = 10;

micBtn.addEventListener("click", startRecording);


// 1. START RECORDING

async function startRecording() {
    try {
        recordingStream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        audioChunks = [];

        let mimeType = "";

        if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
            mimeType = "audio/webm;codecs=opus";
        } else if (MediaRecorder.isTypeSupported("audio/webm")) {
            mimeType = "audio/webm";
        }

        mediaRecorder = mimeType
            ? new MediaRecorder(recordingStream, { mimeType })
            : new MediaRecorder(recordingStream);

        mediaRecorder.ondataavailable = function(event) {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = processRecording;

        mediaRecorder.start();

        micBtn.classList.add("recording");
        micBtn.disabled = true;

        statusText.innerText = "Listening... Speak now!";
        result.innerText = "";

        let remaining = RECORDING_TIME;

        timerText.innerText =
            `Recording: ${remaining} seconds remaining`;

        countdownInterval = setInterval(() => {
            remaining--;

            timerText.innerText =
                `Recording: ${remaining} seconds remaining`;

            if (remaining <= 0) {
                clearInterval(countdownInterval);
            }
        }, 1000);

        recordingTimeout = setTimeout(() => {
            if (mediaRecorder && mediaRecorder.state === "recording") {
                mediaRecorder.stop();
            }
        }, RECORDING_TIME * 1000);

    } catch (error) {
        statusText.innerText = "Microphone access failed.";
        result.innerText = error.message;

        releaseMicrophone();
        micBtn.disabled = false;
    }
}


// 2. SEND AUDIO TO FLASK

async function processRecording() {
    clearInterval(countdownInterval);
    clearTimeout(recordingTimeout);

    micBtn.classList.remove("recording");

    statusText.innerText = "Processing your voice...";
    timerText.innerText = "Please wait";

    try {
        const audioBlob = new Blob(audioChunks, {
            type: mediaRecorder.mimeType
        });

        const formData = new FormData();

        formData.append("audio", audioBlob, "recording.webm");

        const response = await fetch("/transcribe", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        result.innerText =
            "Recognized Speech:\n" +
            (data.transcript || "No speech detected.");

        if (!response.ok || !data.success) {
            statusText.innerText = "Command could not be completed.";

            showResultPopup(
                "Command Failed",
                data.message || "Unable to complete the command.",
                null,
                false
            );

            return;
        }

        statusText.innerText = "Command processed successfully!";

        // Show the result in a popup
        showResultPopup(
            getPopupTitle(data.intent),
            data.message,
            data.data,
            true
        );

        timerText.innerText = "Ready for your next command";

    } catch (error) {
        statusText.innerText = "Something went wrong.";
        result.innerText += "\n\n" + error.message;
        timerText.innerText = "Please try again";

    } finally {
        releaseMicrophone();
        micBtn.disabled = false;
    }
}


// 3. POPUP TITLE BASED ON INTENT

function getPopupTitle(intent) {

    switch (intent) {

        case "VIEW_TIMETABLE":
            return "Timetable Details";

        case "VIEW_ATTENDANCE":
            return "Attendance Details";

        case "MARK_ATTENDANCE":
            return "Attendance Update";

        case "VIEW_ACADEMIC_CALENDAR":
            return "Academic Calendar";

        default:
            return "ERP Assistant Result";
    }
}


// 4. DISPLAY RESULT POPUP


function showResultPopup(title, message, data, success) {

    const oldPopup = document.getElementById("erpResultPopup");

    if (oldPopup) {
        oldPopup.remove();
    }

    const popup = document.createElement("div");
    popup.id = "erpResultPopup";

    popup.style.cssText = `
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.65);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        padding: 20px;
    `;

    const card = document.createElement("div");

    card.style.cssText = `
        background: white;
        color: #222;
        padding: 30px;
        border-radius: 14px;
        width: 92vw;
        max-width: 1100px;
        max-height: 90vh;
        display: flex;
        flex-direction: column;
        text-align: left;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    `;

    // Heading
    const heading = document.createElement("h2");
    heading.innerText = title;

    heading.style.cssText = `
        text-align: center;
        font-size: 26px;
        margin-bottom: 15px;
        color: #263445;
        flex-shrink: 0;
    `;

    // Result message
    const messageText = document.createElement("p");
    messageText.innerText = message || "";

    messageText.style.cssText = `
        text-align: center;
        line-height: 1.6;
        color: ${success ? "#16834a" : "#c0392b"};
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 15px;
        flex-shrink: 0;
    `;

    // Scrollable data area
    const dataContainer = document.createElement("div");

    dataContainer.style.cssText = `
        margin-top: 10px;
        flex: 1;
        min-height: 0;
        max-height: 65vh;
        overflow: auto;
        padding: 5px;
        border: 1px solid #e1e6ed;
        border-radius: 8px;
    `;

    if (data !== null && data !== undefined) {
        renderData(data, dataContainer);
    }

    // Close button
    const closeButton = document.createElement("button");
    closeButton.innerText = "Close";

    closeButton.style.cssText = `
        display: block;
        margin: 20px auto 0;
        padding: 12px 35px;
        background: #222;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 15px;
        flex-shrink: 0;
    `;

    closeButton.addEventListener("click", () => {
        popup.remove();
    });

    card.appendChild(heading);
    card.appendChild(messageText);
    card.appendChild(dataContainer);
    card.appendChild(closeButton);

    popup.appendChild(card);
    document.body.appendChild(popup);
}

// 5. DISPLAY DATABASE DATA AS READABLE TABLES

function renderData(data, container) {

    if (Array.isArray(data)) {

        if (data.length === 0) {
            const emptyText = document.createElement("p");
            emptyText.innerText = "No matching records found.";
            container.appendChild(emptyText);
            return;
        }

        if (typeof data[0] === "object" && data[0] !== null) {

            const table = document.createElement("table");

            table.style.cssText = `
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            `;

            const headers = Object.keys(data[0]);
            const headerRow = document.createElement("tr");

            headers.forEach(key => {
                const th = document.createElement("th");
                th.innerText = key.replaceAll("_", " ");
                th.style.cssText =
                    "border:1px solid #ddd;padding:9px;background:#eee;text-align:left;";
                headerRow.appendChild(th);
            });

            table.appendChild(headerRow);

            data.forEach(record => {

                const row = document.createElement("tr");

                headers.forEach(key => {
                    const td = document.createElement("td");

                    td.innerText = formatValue(record[key]);

                    td.style.cssText =
                        "border:1px solid #ddd;padding:9px;";

                    row.appendChild(td);
                });

                table.appendChild(row);
            });

            container.appendChild(table);

        } else {

            data.forEach(item => {
                const p = document.createElement("p");
                p.innerText = formatValue(item);
                container.appendChild(p);
            });
        }

    } else if (typeof data === "object") {

        Object.entries(data).forEach(([key, value]) => {

            const row = document.createElement("p");

            row.style.cssText = `
                padding: 8px;
                border-bottom: 1px solid #eee;
            `;

            const label = document.createElement("strong");
            label.innerText = key.replaceAll("_", " ") + ": ";

            row.appendChild(label);
            row.appendChild(
                document.createTextNode(formatValue(value))
            );

            container.appendChild(row);
        });

    } else {

        const p = document.createElement("p");
        p.innerText = formatValue(data);
        container.appendChild(p);
    }
}


// 6. FORMAT DATABASE VALUES

function formatValue(value) {

    if (value === null || value === undefined) {
        return "-";
    }

    if (typeof value === "object") {
        return JSON.stringify(value);
    }

    return String(value);
}


// 7. RELEASE MICROPHONE

function releaseMicrophone() {

    if (recordingStream) {
        recordingStream.getTracks().forEach(track => track.stop());
        recordingStream = null;
    }
}
