<script>
  const device = navigator.platform;
  document.getElementById('device').value = device;

  const timeCondition = "{{time}}"; // Jinja2-safe string

  if (timeCondition === "timeslap") {
    let r = 0;

    const interval = setInterval(() => {
      r += 1;

      document.getElementById("username").disabled = true;
      document.getElementById("password").disabled = true;
      document.getElementById("button").disabled = true;

      if (r >= 300) {
        document.getElementById("username").disabled = false;
        document.getElementById("password").disabled = false;
        document.getElementById("button").disabled = false;

        // Fix: GET request with query parameters
        fetch('/login/delete?device=' + encodeURIComponent(device), {
          method: "GET"
        });

        clearInterval(interval); // Stop interval after execution
      }
    }, 1000); // Every second
  }
</script>