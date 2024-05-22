
    const hour = document.getElementById('hour');
    const min = document.getElementById('min');
    const sec = document.getElementById('sec');

    const clock = setInterval(function time() {
        let today = new Date();
        let hr = today.getHours();
        let mn = today.getMinutes();
        let se = today.getSeconds();

        if (hr < 10) hr = '0' + hr;
        if (mn < 10) min = '0' + mn;
        if (se < 10) se = '0' + se;

        hour.textContent = hr;
        min.textContent = mn;
        sec.textContent = se;
    })