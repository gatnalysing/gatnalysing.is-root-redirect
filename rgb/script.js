document.getElementById('colorSlider').addEventListener('input', function() {
    const angle = parseInt(this.value, 10);
    const color = colorData.find(c => c.angle === angle);
    if (color) {
        document.body.style.backgroundColor = color.hex;
        document.getElementById('colorValue').innerText = `Hex Color Value: ${color.hex.toUpperCase()}`;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const image1 = document.getElementById('colorBanner');
    const image2 = document.getElementById('colorBanner2');
    const colorValueDisplay = document.getElementById('colorValue');
    const brightnessSlider = document.getElementById('brightnessSlider');
    const brightnessValueDisplay = document.getElementById('brightnessValue');
    const submitBtn = document.getElementById('submitBtn'); // Get the submit button

    // Update the displayed brightness value as the slider moves
    brightnessSlider.addEventListener('input', function() {
        brightnessValueDisplay.innerText = this.value;
    });

    function updateColorFromImage(event, colorDataArray) {
        const rect = event.target.getBoundingClientRect();
        const clickX = event.clientX - rect.left;
        const imageWidth = rect.width;
        const clickPositionPercentage = clickX / imageWidth;
        const angle = Math.round(clickPositionPercentage * 360);
        const color = colorDataArray.find(c => c.angle === angle);
        if (color) {
            document.body.style.backgroundColor = color.hex;
            colorValueDisplay.innerText = `${color.hex.toUpperCase()}`;
        }
    }

    image1.addEventListener('click', function(event) {
        updateColorFromImage(event, colorData); // Use colorData for the first banner
    });

    image2.addEventListener('click', function(event) {
        updateColorFromImage(event, colorData2); // Use colorData2 for the second banner
    });

    // Event listener for the submit button
    submitBtn.addEventListener('click', function() {
        const selectedColor = colorValueDisplay.innerText; // Get the selected color hex value
        const brightness = brightnessValueDisplay.innerText; // Get the brightness value
        fetch('http://10.0.0.31:5000/sendColor', {  // Replace with your Flask backend URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                color: selectedColor,
                brightness: brightness
            }),
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
