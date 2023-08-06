import { utilities } from './utilities.js';
window.MESSAGES = [{level:'info',message:'hi',timeout:1}];
let SERVER_MESSAGES = [];

setInterval(function() {
  MESSAGES = MESSAGES.filter(function(m) {
    if (m.hasOwnProperty('timeout')) {
      if (!m.hasOwnProperty('start')) m.start = Date.now();
      return Date.now() - m.start < m.timeout*1000;
    } else {
      return true;
    }
  });

  let msgdiv = document.querySelector('div.mymessages');
  utilities.remove_all_child_nodes(msgdiv);
  SERVER_MESSAGES.concat(MESSAGES).forEach(function(m) {
    let mdiv = document.createElement('div');
    mdiv.classList.add('alert','alert-'+m.level,'mb-1');
    mdiv.textContent = m.message;
    msgdiv.appendChild(mdiv);
  });
  
},500);

let connection = new WebSocket('ws://'+window.location.host+'/server_status');
connection.onmessage = function (e) {
  SERVER_MESSAGES = JSON.parse(e.data);
};
