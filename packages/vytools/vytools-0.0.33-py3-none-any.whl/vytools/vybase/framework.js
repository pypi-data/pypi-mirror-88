import { MODEL } from './model.js';
import { utilities } from './utilities.js';
import './messages.js';
import { MENU } from './menuitems.js';
import { type_buttons } from './typebuttons.js';
import { draw_graph, add_graphs } from './graph_model.js';

window.toggleclass = utilities.toggleclass;
window.addEventListener('message',function(e) {
  let iframe = document.querySelector('iframe');
  if (e.origin == 'null' && e.source === iframe.contentWindow) {
    utilities.serverfetch(e.data.topic, e.data.data, function(r) {
      iframe.contentWindow.postMessage({id:e.data.id,data:r},'*');
    });
  }
});

window.iframe_loaded = function(self) {
  self.contentWindow.postMessage({id:'__initialize__',data:MODEL.selected.loaded},'*');
}

window.togglemessages = function() {
  let sm = document.querySelector('i.showmessages');
  let mm = document.querySelector('div.mymessages');
  if (sm.classList.contains('fa-bell-slash')) {
    sm.classList.remove('fa-bell-slash')
    mm.style.display = 'block';
    sm.classList.add('fa-bell')
  } else {
    sm.classList.remove('fa-bell');
    mm.style.display = 'none';
    sm.classList.add('fa-bell-slash')
  }
}

window.add_item = function(self) { 
  add_to_menu(self.value);
  select_item(self.value);
}

window.add_to_menu = function (v) {
  if (MODEL.menu.indexOf(v) == -1) { 
    MODEL.menu.push(v);
    utilities.serverfetch('__menu__',MODEL.menu,null);
    MENU.update();
  }
}

const remove_from_menu = function (v) {
  let idx = MODEL.menu.indexOf(v);
  if (idx > -1) {
    MODEL.menu.splice(idx,1);
    utilities.serverfetch('__menu__',MODEL.menu,null);
    if (v == MODEL.selected.name) MODEL.clear_selected();
    MENU.update();
  }
}

const select_item = function(v) {
  if (!v) return;
  MENU.select(v);
  MODEL.selected.name = v;
}

const compose_view = function(v) {
  select_item(v);
  let iframe = utilities.get_iframe();
  let split_name = v.split(':');
  let typ = `__${split_name[0]}__`;
  if (['__compose__', '__episode__'].indexOf(typ) > -1) {
    utilities.serverfetch(typ, {name:v},function(d) {
      MODEL.selected.loaded = d;
      let src = (d.hasOwnProperty('html')) ? d.html : '<p>not found</p>';
      iframe.setAttribute('srcdoc',src);
    });
  } else if (typ === '__ui__' && v.endsWith('.html')) {
    fetch(split_name[1]) // Call the fetch function passing the url of the API as a parameter
      .then((resp) => resp.text())
      .then((resp) => iframe.setAttribute('srcdoc',resp))
      .catch(error=>console.error(error))
  }
}

window.item_action = function(item, action) {
  if (item) {
    if (action=='remove') {
      remove_from_menu(item);
    } else if (action=='add') {
      add_to_menu(item);
    } else if (action=='build') {
      let kwargs = window.prompt("Build key word arguments",'{"build_args":{}, "build_level":1}');
      utilities.serverfetch('__build__',{list:[item],kwargs:JSON.parse(kwargs)},function(res) {
        if (res.starting) {
        } else {
          window.MESSAGES.push({level:'warning',message:'Please wait until current job finishes',timeout:2});
        }
      });
    } else if (action=='run') {
      let kwargs = window.prompt("Run key word arguments",'{"build_args":{}, "clean":false}');
      utilities.serverfetch('__run__',{list:[item],kwargs:JSON.parse(kwargs)},function(res) {
        if (res.starting) {
          compose_view(item)
        } else {
          window.MESSAGES.push({level:'warning',message:'Please wait until current job finishes',timeout:2});
        }
      });
    } else if (action=='compose') {
      compose_view(item);
    } else { //  default and (action=='graph')
      select_item(item);
      add_graphs();
      draw_graph();
    }
  } else {
    console.log('unknown item in itemlist');
  }
}

document.querySelector('div.itemlist').onclick = function(event) {
  var target = utilities.get_event_target(event);
  let item = utilities.get_data_until(target,'item','LI');
  let action = utilities.get_data_until(target,'action','LI');
  if (action=='remove' && event.detail <=1 ) return;
  item_action(item, action);
}

const init = function() {
  MODEL.init(function(it) {

    if (it) {
      item_action(it,'compose');
      utilities.removeclass('.panel','expand');
    }

    type_buttons();
    MENU.init(MODEL.menu); // hook up menu
    MENU.update();
  });
}

window.onresize = function() { 
  draw_graph();
}

init();  // INITIALIZATION ============================
