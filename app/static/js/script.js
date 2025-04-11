document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('tts-form');
    const textInput = document.getElementById('text-input');
    const convertBtn = document.getElementById('convert-btn');
    const resultDiv = document.getElementById('result');
    const audioPlayer = document.getElementById('audio-player');
    const downloadBtn = document.getElementById('download-btn');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get the text from the input
        const text = textInput.value.trim();

        if (!text) {
            alert('Please enter some text to convert.');
            return;
        }

        // Show loading, hide other sections
        loadingDiv.classList.remove('hidden');
        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
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
            resultDiv.classList.remove('hidden');

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
            errorDiv.classList.remove('hidden');
        } finally {
            // Hide loading and re-enable button
            loadingDiv.classList.add('hidden');
            convertBtn.disabled = false;
        }
    });
});
