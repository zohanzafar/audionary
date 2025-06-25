const uploadForm = document.getElementById('uploadForm');
const pdfFile = document.getElementById('pdfFile');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const narrationPreview = document.getElementById('narrationPreview');
const audioPlayer = document.getElementById('audioPlayer');
const copyNarration = document.getElementById('copyNarration');
const downloadAudio = document.getElementById('downloadAudio');
const toastContainer = document.getElementById('toastContainer');

// Function to show toast notification
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast bg-red-500 text-white p-4 rounded-lg shadow-lg flex items-center justify-between max-w-sm';
    toast.innerHTML = `
        <span>${message}</span>
        <button class="ml-4 text-white hover:text-gray-200 focus:outline-none" onclick="this.parentElement.remove()">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    `;
    toastContainer.appendChild(toast);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        toast.classList.add('opacity-0', 'transition-opacity', 'duration-300');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Function to validate file type
function isValidPDF(file) {
    return file && file.type === 'application/pdf';
}

// Handle drag and drop
const dropZone = pdfFile.parentElement;
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-indigo-500');
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-indigo-500');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-indigo-500');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        if (isValidPDF(files[0])) {
            pdfFile.files = files;
        } else {
            showToast('Only PDF files are allowed.');
        }
    }
});

// Handle file input change
pdfFile.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file && !isValidPDF(file)) {
        showToast('Only PDF files are allowed.');
        pdfFile.value = ''; // Clear the input
    }
});

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const file = pdfFile.files[0];
    if (!file) {
        showToast("Please upload a PDF");
        return;
    }

    if (!isValidPDF(file)) {
        showToast("Only PDF files are allowed.");
        pdfFile.value = ''; // Clear the input
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    loading.classList.remove("hidden");
    result.classList.add("hidden");

    try {
        const response = await fetch("api/upload-pdf/", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Network response was not ok");
        }

        loading.classList.add("hidden");
        narrationPreview.textContent = data.narration_preview;
        audioPlayer.src = data.audio_url;
        result.classList.remove("hidden");
        result.classList.add('animate-fade-in');
    } catch (err) {
        loading.classList.add("hidden");
        showToast(err.message || "Error occurred while processing PDF.");
        console.error(err);
    }
});

// Copy Narration Text
copyNarration.addEventListener('click', () => {
    const text = narrationPreview.textContent;
    navigator.clipboard.writeText(text).then(() => {
        copyNarration.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> Copied!';
        setTimeout(() => {
            copyNarration.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg> Copy';
        }, 2000);
    }).catch(err => {
        showToast("Failed to copy text.");
        console.error(err);
    });
});

// Download Audio
downloadAudio.addEventListener('click', () => {
    const audioUrl = audioPlayer.src;
    if (!audioUrl) {
        showToast("No audio available to download.");
        return;
    }
    const link = document.createElement('a');
    link.href = audioUrl;
    link.download = 'audionary_podcast.mp3';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});