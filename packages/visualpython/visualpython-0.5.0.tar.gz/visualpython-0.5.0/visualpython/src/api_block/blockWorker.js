// main에서 postMessage의 값을 받는다. 
onmessage = (e)=>{
    // 받은 값을 echo를 붙여서 다시 보낸다.
    for( var i = 0; i < 100; i++) {
        (async() => {
            console.log(i);
        })();
    }
    postMessage("echo "+e.data);
}
  
  