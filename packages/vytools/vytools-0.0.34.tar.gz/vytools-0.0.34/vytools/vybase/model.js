import { utilities } from './utilities.js';

export let MODEL = {
  config : {
    thingtypes:{
      repo:{bl:'Re',cl:'item-repository',color:'yellow'},
      definition:{bl:'De',cl:'item-definition',color:'red'},
      object:{bl:'Ob',cl:'item-object',color:'orange'},
      ui:{bl:'Ui',cl:'item-ui',color:'blue'},
      stage:{bl:'St',cl:'item-stage',color:'purple'},
      compose:{bl:'Co',cl:'item-compose',color:'green'},
      episode:{bl:'Ep',cl:'item-episode',color:'black'},
    }  
  },
  items : {},
  ilist : [],
  selected : {},
  menu : [],
  clear_selected: function() {
    MODEL.selected.name = null;
    MODEL.selected.loaded = null;
    let iframe = document.querySelector('iframe')
    if (iframe) iframe.setAttribute('srcdoc','');  
  },
  init : function(cb) {
    utilities.serverfetch('__init__',{},function(r) {
      if(!r) return;
      if (r.items) Object.keys(r.items).forEach(k => MODEL.items[k] = r.items[k]);
      if (r.menu) MODEL.menu = r.menu;
      MODEL.ilist = Object.keys(MODEL.items);
      if (cb) cb(r.load);
    });
  }  
};

const add_action_button = function(item,action) {
  let a = document.createElement('a');
  a.classList.add('btn');
  a.setAttribute('data-action',action.action);
  let typ = item.split(':')[0];
  if (action.hasOwnProperty('enabled') && action.enabled.indexOf(typ) == -1) {
    a.disabled = true;
    a.classList.add('disabled');
  }
  let i = document.createElement('i');
  i.classList.add('fas',action.icon);
  a.appendChild(i);
  return a;
}

const create_li = function(z) {
  let li = document.createElement('li');
  li.classList.add('list-group-item','ellips','actionitem',z.class);
  li.setAttribute('data-item',z.item);
  let div = document.createElement('div');
  div.classList.add('btn-group','hide','action-item-group');
  z.actions.forEach( a => div.appendChild(add_action_button(z.item,a)));
  li.innerText = z.label;
  li.appendChild(div);
  return li;
}

export function create_menu_item(v,actions) {
  let item = MODEL.items[v];
  let cfg = MODEL.config.thingtypes[item.thingtype];
  let act = (actions) ? actions : [
    {'action':'graph','icon':'fa-bullseye'},
    {'action':'build','icon':'fa-hard-hat','enabled':['stage','compose','episode']},
    {'action':'run','icon':'fa-running','enabled':['episode']},
    {'action':'compose','icon':'fa-users-cog','enabled':['episode','compose','ui']},
    {'action':'remove','icon':'fa-times-circle'}
  ];
  return create_li({
    label:`${cfg.bl}:${item['name']}`,
    item:v,
    class:`color-${cfg.color}-4`,
    actions:act
  });
}

export function make_item_list(lst) {
  return lst.filter(v => MODEL.items.hasOwnProperty(v))
            .map(v => create_menu_item(v,null));
}

MODEL.clear_selected();

