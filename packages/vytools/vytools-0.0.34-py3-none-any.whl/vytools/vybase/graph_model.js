import { MODEL, create_menu_item } from './model.js';
import { partition_graph, svg_partition_graph } from './graph.js';
import { utilities } from './utilities.js';

let EDITOR_ITEM = null;
window.EDITOR = null;
let tooltip = document.querySelector("div.globaltooltip");
let overlay = document.querySelector('.overlay')
  
window.showTooltip = function(evt, text) {
  tooltip.innerHTML = text;
  tooltip.style.display = "block";
  tooltip.style.left = evt.pageX + 10 + 'px';
  tooltip.style.top = evt.pageY + 10 + 'px';
}

window.hideTooltip = function() {
  tooltip.style.display = "none";
  if (EDITOR_ITEM != MODEL.selected.name) {
    set_editor(MODEL.selected.name);
  }
  // overlay.style.display = "none";
}

window.click_graph_item = function(evt, item) {
  if (evt.detail == 1) {
    set_editor(item);
  } else if (evt.detail == 2) {
    add_to_menu(item);
  } else if (evt.detail == 3) {
    item_action(item,'graph');
  }
  // overlay.style.display = "block";
  // overlay.innerText = item
}

const re_editor = function() {
  if (EDITOR) {
    EDITOR.resize();
    EDITOR.setFontSize(15);
    EDITOR.setFontSize(16);
  }
}

const set_editor = function(item) {
  document.querySelector('div.native div.textheader').innerHTML = `${item}<br/><span><small>contents:</small></span>`;
  EDITOR_ITEM = item;
  utilities.serverfetch('__item__',{name:item},function(res) {
    if (res && res.text) {
      EDITOR.setValue(res.text);
      if (item.endsWith('.html')) {
        EDITOR.session.setMode("ace/mode/html");  
      } else if (item.endsWith('.js')) {
        EDITOR.session.setMode("ace/mode/javascript");  
      } else if (item.endsWith('.json')) {
        EDITOR.session.setMode("ace/mode/json");  
      } else if (item.startsWith('stage:')) {
        EDITOR.session.setMode("ace/mode/dockerfile");        
      } else if (item.startsWith('compose:')) {
        EDITOR.session.setMode("ace/mode/yaml");        
      } else {
        EDITOR.session.setMode("ace/mode/json");        
      }
      EDITOR.clearSelection();
      EDITOR.gotoLine(0, 0);
      re_editor();
    }
  })

}

let DEPENDS = null;
let DEPENDED = null;

export function draw_graph() {
  if (!MODEL.selected.name || !utilities.is_native()) return
  let div = utilities.get_native();
  let w = div.offsetWidth, h = div.offsetHeight;
  let headerheight = 43;
  let h2 = headerheight;
  if (w == 0 || h == 0) { w = 400; h = 400 };
  let r = (h<w) ? h/2 : w/2;
  if (r - headerheight < 150) return;

  let divA = document.querySelector('div.native div.dependson');
  let divB = document.querySelector('div.native div.dependedon');
  let divC = document.querySelector('div.native div.itemtext');
  let divD = document.querySelector('div.native div.textheader');
  // let divD = document.querySelector('div.native div.overlay');
  if (h<w) {
    divA.setAttribute('style',`position:absolute; top:0px; left:0px; height:50%; width:${r}px`);
    divB.setAttribute('style',`position:absolute; bottom:0px; left:0px; height:50%; width:${r}px`);
    divC.setAttribute('style',`position:absolute; top:${h2}px; right:0px; height:calc(100% - ${h2}px); width:calc(100% - ${r}px)`);
    divD.setAttribute('style',`position:absolute; top:0px; right:0px; width:calc(100% - ${r}px)`);
    // divD.setAttribute('style',`position:absolute; top:${pad}px; right:${pad}px; height:calc(100% - ${2*pad}px); width:calc(100% - ${r+2*pad}px);background-color: white; opacity: 0.6; display: none`);
  } else {
    divA.setAttribute('style',`position:absolute; top:0px; left:0px; width:50%; height:${r}px`);
    divB.setAttribute('style',`position:absolute; top:0px; right:0px; width:50%; height:${r}px`);
    divC.setAttribute('style',`position:absolute; top:${r+h2}px; left:0px; width:100%; height:calc(100% - ${r+h2}px)`);
    divD.setAttribute('style',`position:absolute; top:${r}px; left:0px;`);
    // divD.setAttribute('style',`position:absolute; bottom:${pad}px; left:${pad}px; width:calc(100% - ${2*pad}px); height:calc(100% - ${r+2*pad}px);background-color: white; opacity: 0.6; display: none`);
  }
  divA.querySelector('div.graphheader').innerHTML = `${MODEL.selected.name}<br/><span><small>depends on:</small></span>`
  divB.querySelector('div.graphheader').innerHTML = `${MODEL.selected.name}<br/><span><small>depended on by:</small></span>`
  let svgA = divA.querySelector('svg'); if (svgA) svgA.parentNode.removeChild(svgA);
  let svgB = divB.querySelector('svg'); if (svgB) svgB.parentNode.removeChild(svgB);
  svgA = svg_partition_graph(r-headerheight, DEPENDS);
  svgB = svg_partition_graph(r-headerheight, DEPENDED);
  divA.appendChild(svgA);
  divB.appendChild(svgB);
  // let code = document.createElement('code'); code.classList.add('doc')
  // let pre = document.createElement('pre');
  // pre.innerText = JSON.stringify(DEPENDS,null,2);
  // code.appendChild(pre);
  // div.appendChild(code);
  re_editor();
}



const add_graph_actions = function(item) {
  item.graphp.class = `color-${MODEL.config.thingtypes[item.thingtype].color}-svg`;
  // item.graphp.onmouseover = `console.log('over ${item.thingtype+':'+item.name}')`;
  item.graphp.onclick = `click_graph_item(evt,'${item.thingtype+':'+item.name}');`;
  item.graphp.onmousemove=`showTooltip(evt, '${item.thingtype+':'+item.name}');`;
  item.graphp.onmouseout="hideTooltip();";
}

export function add_graphs() {
  if (!EDITOR) {
    EDITOR = ace.edit("itemtext");
    // EDITOR.setTheme("ace/theme/twilight");
    EDITOR.setTheme("ace/theme/github");
  }

  DEPENDED = partition_graph(MODEL.selected.name, MODEL.items, 'depended_on');
  DEPENDS = partition_graph(MODEL.selected.name, MODEL.items, 'depends_on');
  DEPENDS.forEach(add_graph_actions);
  DEPENDED.forEach(add_graph_actions);
  set_editor(MODEL.selected.name); 
  utilities.get_native();
}

// let add_expand_dep_list = function(i, items, found, div, childkey) {
//   if (items.hasOwnProperty(i)) {
//     let item = items[i];
//     let li = create_menu_item(i, [{'action':'add','icon':'fa-plus'}]);
//     div.appendChild(li);
//     if (found.indexOf(i) == -1 && item.hasOwnProperty(childkey) && item[childkey].length > 0) {
//       found.push(i);
//       let ol = document.createElement('ol');
//       // ol.classList.add('list-group');
//       item[childkey].forEach(ii => add_expand_dep_list(ii, items, found, ol, childkey));
//       div.appendChild(ol);
//     }
//   }
// }

// const draw_dependencies = function() {
//   let div = utilities.get_native();
//   let found = [];
//   let div2 = document.createElement('div');
//   div2.classList.add('depcontainer');
//   add_expand_dep_list(MODEL.selected.name, MODEL.items, found, div2, 'depends_on');
//   div2.onclick = function(event) {
//     var target = utilities.get_event_target(event);
//     let item = utilities.get_data_until(target,'item','LI');
//     if (item) add_to_menu(item);
//   }
//   div.appendChild(div2);
// }
