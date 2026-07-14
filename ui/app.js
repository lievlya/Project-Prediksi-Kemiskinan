async function checkApiStatus() {    const statusText = document.getElementById('status-text');
    statusText.innerText = "Menghubungkan...";
    
    try {
        const response = await fetch('http://localhost:5000/api/status');
        const data = await response.json();
        
        statusText.innerText = "Integrasi Berhasil: " + data.message;
        console.log("Data diterima:", data);
        
    } catch (error) {
        statusText.innerText = "Gagal terhubung ke Backend. Pastikan Backend sudah jalan.";
        console.error("Error:", error);
    }
}