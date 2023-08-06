export const utilities = {

  remove_all_child_nodes : function(parent) {
    while (parent.firstChild) { parent.removeChild(parent.firstChild); }
  },
  
  removeclass : function(slctr, cls) { 
    [].forEach.call(document.querySelectorAll(slctr), el => el.classList.remove(cls));
  },

  addclass : function(slctr, cls) { 
    [].forEach.call(document.querySelectorAll(slctr), el => el.classList.add(cls));
  },

  toggleclass : function(slctr, cls) { 
    [].forEach.call(document.querySelectorAll(slctr), el => el.classList.toggle(cls));
  },

  serverfetch : function(topic,d,cb) {
    fetch(topic, {
        headers:{"content-type":"application/json; charset=UTF-8"},
        body:JSON.stringify(d),
        method:"POST"
      })
      .then(data=>{ return data.json(); })
      .then(res=>{ if (cb) cb(res); })
      .catch(error=>console.error(`Failed in fetch or callback of ${topic} with data ${JSON.stringify(d)}: ${error}`))
  },

  get_event_target : function(e) {
    e = e || window.event;
    return e.target || e.srcElement; 
  },
  
  get_data_until : function(t,i,u) {
    return ((!t) ? null : (t.dataset[i]) ? t.dataset[i] : 
      ((t.tagName == u) ? null : this.get_data_until(t.parentElement,i,u)));
  },
  
  get_native : function() {
    this.removeclass('div.workspacetabs div','active');
    this.addclass('div.workspacetabs div.native','active');
    return document.querySelector('div.workspacetabs div.native');
  },

  is_native : function() {
    return document.querySelector('div.workspacetabs div.native').classList.contains('active');
  },

  get_iframe : function() {
    let iframe = document.querySelector('div.workspacetabs div.iframe iframe');
    this.removeclass('div.workspacetabs div','active');
    this.addclass('div.workspacetabs div.iframe','active');
    return iframe;  
  }

}
