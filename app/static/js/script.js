document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Function to convert ChatGPT response to speech
    async function convertChatGPTResponseToSpeech(text) {
        if (!text) {
            console.error('No ChatGPT response to convert to speech.');
            return;
        }

        // Show loading, hide other sections
        chatGPTTTSLoadingDiv.classList.remove('hidden');
        chatGPTTTSResultDiv.classList.add('hidden');
        chatGPTTTSErrorDiv.classList.add('hidden');

        try {
            // Send the request to the TTS API
            const response = await fetch('/text-to-speech/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({text: text}),
            });

            if (!response.ok) {
                throw new Error('Failed to convert text to speech');
            }

            // Get the audio blob
            const audioBlob = await response.blob();

            // Create a URL for the audio blob
            const audioUrl = URL.createObjectURL(audioBlob);

            // Set the audio source and show the player
            chatGPTAudioPlayer.src = audioUrl;
            chatGPTTTSResultDiv.classList.remove('hidden');

            // Enable download button
            chatGPTDownloadBtn.classList.remove('hidden');

            // Remove any existing event listeners by cloning and replacing the button
            const newChatGPTDownloadBtn = chatGPTDownloadBtn.cloneNode(true);
            chatGPTDownloadBtn.parentNode.replaceChild(newChatGPTDownloadBtn, chatGPTDownloadBtn);
            // Update the reference to the new button
            const chatGPTDownloadBtnRef = document.getElementById('chatgpt-download-btn');

            chatGPTDownloadBtnRef.addEventListener('click', function () {
                const a = document.createElement('a');
                a.href = audioUrl;
                a.download = 'chatgpt-response.mp3';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });

        } catch (error) {
            console.error('Error:', error);
            chatGPTTTSErrorDiv.classList.remove('hidden');
        } finally {
            // Hide loading
            chatGPTTTSLoadingDiv.classList.add('hidden');
        }
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });

    // STT option switching functionality for both STT tabs
    const optionBtns = document.querySelectorAll('.option-btn');
    const sttOptions = document.querySelectorAll('.stt-option');

    optionBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            // Get the parent tab to only affect options within the same tab
            const parentTab = this.closest('.tab-content');

            // Remove active class from buttons and options within this tab
            parentTab.querySelectorAll('.option-btn').forEach(b => b.classList.remove('active'));
            parentTab.querySelectorAll('.stt-option').forEach(o => o.classList.remove('active'));

            // Add active class to clicked button and corresponding option
            this.classList.add('active');
            const optionId = this.getAttribute('data-option');
            document.getElementById(`${optionId}-option`).classList.add('active');
        });
    });

    // Text-to-Speech functionality
    const ttsForm = document.getElementById('tts-form');
    const textInput = document.getElementById('text-input');
    const convertBtn = document.getElementById('convert-btn');
    const ttsResultDiv = document.getElementById('tts-result');
    const audioPlayer = document.getElementById('audio-player');
    const downloadBtn = document.getElementById('download-btn');
    const ttsLoadingDiv = document.getElementById('tts-loading');
    const ttsErrorDiv = document.getElementById('tts-error');

    // Handle TTS form submission
    ttsForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Get the text from the input
        const text = textInput.value.trim();

        if (!text) {
            alert('Please enter some text to convert.');
            return;
        }

        // Show loading, hide other sections
        ttsLoadingDiv.classList.remove('hidden');
        ttsResultDiv.classList.add('hidden');
        ttsErrorDiv.classList.add('hidden');
        convertBtn.disabled = true;

        try {
            // Send the request to the API
            const response = await fetch('/text-to-speech/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text }),
            });

            if (!response.ok) {
                throw new Error('Failed to convert text to speech');
            }

            // Get the audio blob
            const audioBlob = await response.blob();

            // Create a URL for the audio blob
            const audioUrl = URL.createObjectURL(audioBlob);

            // Set the audio source and show the player
            audioPlayer.src = audioUrl;
            ttsResultDiv.classList.remove('hidden');

            // Enable download button
            downloadBtn.classList.remove('hidden');
            downloadBtn.addEventListener('click', function() {
                const a = document.createElement('a');
                a.href = audioUrl;
                a.download = 'speech.mp3';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });

        } catch (error) {
            console.error('Error:', error);
            ttsErrorDiv.classList.remove('hidden');
        } finally {
            // Hide loading and re-enable button
            ttsLoadingDiv.classList.add('hidden');
            convertBtn.disabled = false;
        }
    });

    // Speech-to-Text functionality
    const sttUploadForm = document.getElementById('stt-upload-form');
    const sttUrlForm = document.getElementById('stt-url-form');
    const audioFileInput = document.getElementById('audio-file');
    const audioUrlInput = document.getElementById('audio-url');
    const uploadConvertBtn = document.getElementById('upload-convert-btn');
    const urlConvertBtn = document.getElementById('url-convert-btn');
    const sttResultDiv = document.getElementById('stt-result');
    const transcriptionText = document.getElementById('transcription-text');
    const copyBtn = document.getElementById('copy-btn');
    const sttLoadingDiv = document.getElementById('stt-loading');
    const sttErrorDiv = document.getElementById('stt-error');

    // Handle STT upload form submission
    sttUploadForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Check if file is selected
        if (!audioFileInput.files || audioFileInput.files.length === 0) {
            alert('Please select an MP3 file to convert.');
            return;
        }

        // Show loading, hide other sections
        sttLoadingDiv.classList.remove('hidden');
        sttResultDiv.classList.add('hidden');
        sttErrorDiv.classList.add('hidden');
        uploadConvertBtn.disabled = true;

        try {
            // Create form data
            const formData = new FormData();
            formData.append('file', audioFileInput.files[0]);

            // Send the request to the API
            const response = await fetch('/speech-to-text/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to convert speech to text');
            }

            // Get the response data
            const data = await response.json();

            // Display the transcribed text
            transcriptionText.textContent = data.text;
            sttResultDiv.classList.remove('hidden');

            // Set up copy button
            copyBtn.addEventListener('click', function () {
                navigator.clipboard.writeText(data.text)
                    .then(() => {
                        const originalText = copyBtn.textContent;
                        copyBtn.textContent = 'Copied!';
                        setTimeout(() => {
                            copyBtn.textContent = originalText;
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('Failed to copy text: ', err);
                    });
            });

        } catch (error) {
            console.error('Error:', error);
            sttErrorDiv.classList.remove('hidden');
        } finally {
            // Hide loading and re-enable button
            sttLoadingDiv.classList.add('hidden');
            uploadConvertBtn.disabled = false;
        }
    });

    // Handle STT URL form submission
    sttUrlForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Get the URL from the input
        const audioUrl = audioUrlInput.value.trim();

        if (!audioUrl) {
            alert('Please enter an audio URL to convert.');
            return;
        }

        // Show loading, hide other sections
        sttLoadingDiv.classList.remove('hidden');
        sttResultDiv.classList.add('hidden');
        sttErrorDiv.classList.add('hidden');
        urlConvertBtn.disabled = true;

        try {
            // Send the request to the API
            const response = await fetch('/speech-to-text/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({audio_url: audioUrl}),
            });

            if (!response.ok) {
                throw new Error('Failed to convert speech to text');
            }

            // Get the response data
            const data = await response.json();

            // Display the transcribed text
            transcriptionText.textContent = data.text;
            sttResultDiv.classList.remove('hidden');

            // Set up copy button
            copyBtn.addEventListener('click', function () {
                navigator.clipboard.writeText(data.text)
                    .then(() => {
                        const originalText = copyBtn.textContent;
                        copyBtn.textContent = 'Copied!';
                        setTimeout(() => {
                            copyBtn.textContent = originalText;
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('Failed to copy text: ', err);
                    });
            });

        } catch (error) {
            console.error('Error:', error);
            sttErrorDiv.classList.remove('hidden');
        } finally {
            // Hide loading and re-enable button
            sttLoadingDiv.classList.add('hidden');
            urlConvertBtn.disabled = false;
        }
    });

    // STT to ChatGPT functionality
    const sttChatGPTUploadForm = document.getElementById('stt-chatgpt-upload-form');
    const sttChatGPTUrlForm = document.getElementById('stt-chatgpt-url-form');
    const chatGPTAudioFileInput = document.getElementById('chatgpt-audio-file');
    const chatGPTAudioUrlInput = document.getElementById('chatgpt-audio-url');
    const chatGPTUploadBtn = document.getElementById('chatgpt-upload-convert-btn');
    const chatGPTUrlBtn = document.getElementById('chatgpt-url-convert-btn');
    const sttChatGPTResultDiv = document.getElementById('stt-chatgpt-result');
    const chatGPTTranscriptionText = document.getElementById('chatgpt-transcription-text');
    const chatGPTResponseText = document.getElementById('chatgpt-response-text');
    const sttChatGPTLoadingDiv = document.getElementById('stt-chatgpt-loading');
    const sttChatGPTErrorDiv = document.getElementById('stt-chatgpt-error');

    // ChatGPT TTS functionality
    const chatGPTTTSResultDiv = document.getElementById('chatgpt-tts-result');
    const chatGPTAudioPlayer = document.getElementById('chatgpt-audio-player');
    const chatGPTDownloadBtn = document.getElementById('chatgpt-download-btn');
    const chatGPTTTSLoadingDiv = document.getElementById('chatgpt-tts-loading');
    const chatGPTTTSErrorDiv = document.getElementById('chatgpt-tts-error');

    // Handle STT to ChatGPT upload form submission
    sttChatGPTUploadForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Check if file is selected
        if (!chatGPTAudioFileInput.files || chatGPTAudioFileInput.files.length === 0) {
            alert('Please select an MP3 file to convert.');
            return;
        }

        // Show loading, hide other sections
        sttChatGPTLoadingDiv.classList.remove('hidden');
        sttChatGPTResultDiv.classList.add('hidden');
        sttChatGPTErrorDiv.classList.add('hidden');
        chatGPTUploadBtn.disabled = true;

        try {
            // Create form data
            const formData = new FormData();
            formData.append('file', chatGPTAudioFileInput.files[0]);

            // Send the request to the API
            const response = await fetch('/chatgpt/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to process audio');
            }

            // Get the response data
            const data = await response.json();

            // Hide loading and error states
            sttChatGPTLoadingDiv.classList.add('hidden');
            sttChatGPTErrorDiv.classList.add('hidden');

            // Display the transcribed text and ChatGPT response
            if (data.text) {
                chatGPTTranscriptionText.textContent = data.text;
            } else {
                chatGPTTranscriptionText.textContent = 'No transcription available';
            }

            if (data.response) {
                chatGPTResponseText.textContent = data.response;
                // Automatically convert the response to speech
                convertChatGPTResponseToSpeech(data.response);
            } else {
                chatGPTResponseText.textContent = 'No response available';
            }

            // Show the result container
            sttChatGPTResultDiv.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            sttChatGPTErrorDiv.classList.remove('hidden');
        } finally {
            // Hide loading and re-enable button
            sttChatGPTLoadingDiv.classList.add('hidden');
            chatGPTUploadBtn.disabled = false;
        }
    });

    // Handle STT to ChatGPT URL form submission - Removed as endpoint is no longer available
    sttChatGPTUrlForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        alert('This feature has been removed.');
    });

});
