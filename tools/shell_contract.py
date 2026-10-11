"""Selector/property contracts for complete, independently loadable Shell variants.

This validates generated source, not live St or compositor rendering.
"""
import tinycss2

def parse(css):
 result={}
 for rule in tinycss2.parse_stylesheet(css,skip_comments=True,skip_whitespace=True):
  assert rule.type=='qualified-rule',rule
  declarations=tinycss2.parse_declaration_list(rule.content,skip_comments=True,skip_whitespace=True)
  assert all(d.type=='declaration' for d in declarations),declarations
  for d in declarations:assert all(t.type!='error' for t in d.value)
  ds={d.name:tinycss2.serialize(d.value).strip() for d in declarations}
  for selector in tinycss2.serialize(rule.prelude).strip().split(','):result.setdefault(selector.strip(),{}).update(ds)
 return result

def validate(css,variant):
 rules=parse(css) if isinstance(css,str) else css
 dark=variant=='dark'
 text='#F4F4F5' if dark else '#1C1C1F'
 surface='#202023' if dark else '#FFFFFF'
 popup='rgba(40,40,44,.98)' if dark else '#FFFFFF'
 control='#28282C' if dark else '#F2F2F4'
 hover='#303035' if dark else '#ECECEF'
 active='#38383D' if dark else '#E2E2E6'
 disabled='#7F7F88' if dark else '#8A8A92'
 def expect(selector,prop,value):
  actual=rules.get(selector,{}).get(prop)
  assert actual==value,(variant,selector,prop,actual,value)
 expect('#panel','background-color',surface);expect('#panel','color',text)
 for child in ['', ' .system-status-icon',' .clock',' .clock-display',' .panel-status-menu-box',' StLabel',' StIcon',' .system-status-icon StIcon']:expect('#panel .panel-button'+child,'color',text)
 for selector in ['.popup-menu-content','.quick-settings','.calendar','.message-list','.notification-banner','.modal-dialog','.osd-window']:
  expect(selector,'background-color',popup);expect(selector,'color',text)
 containers=['.popup-menu-item','.quick-settings','.quick-toggle','.quick-menu-toggle','.quick-slider','.quick-settings .icon-button','.quick-settings-system-item .icon-button','.quick-settings-system-item .power-item','.calendar','.calendar-day','.message-list','.message','.notification-banner','.modal-dialog','.modal-dialog-button']
 for selector in containers:
  for child in ['', ' StLabel',' StIcon']:expect(selector+child,'color',text)
 for selector in ['.quick-toggle .quick-toggle-label','.quick-toggle .quick-toggle-icon','.quick-toggle .quick-toggle-arrow','.quick-menu-toggle .quick-toggle-arrow','.quick-menu-toggle .quick-toggle-arrow-button']:expect(selector,'color',text)
 for selector in ['.quick-settings .icon-button','.quick-settings-system-item .icon-button']:
  expect(selector,'border-radius','4px')
  for state,paint in [('',control),(':hover',hover),(':active',active)]:
   expect(selector+state,'background-color',paint);expect(selector+state,'color',text)
 for selector in ['.quick-toggle','.quick-menu-toggle','.quick-settings .icon-button','.quick-settings-system-item .icon-button']:
  expect(selector+':insensitive','background-color',control)
  for child in ['', ' *',' StLabel',' StIcon','.quick-toggle-label','.quick-toggle-icon','.quick-toggle-arrow','.quick-toggle-arrow-button']:
   if child.startswith('.'):child=' '+child
   expect(selector+':insensitive'+child,'color',disabled)
 for selector in ['.popup-menu-item:checked','.quick-toggle:checked','.quick-menu-toggle:checked']:
  expect(selector,'background-color','#6366F1');expect(selector,'color','#FFFFFF')
  for child in ['*','StLabel','StIcon','.quick-toggle-label','.quick-toggle-icon','.quick-toggle-arrow','.quick-toggle-arrow-button']:expect(selector+' '+child,'color','#FFFFFF')
 expect('.search-entry','background-color',control if dark else '#FFFFFF');expect('.search-entry','color',text)
 expect('.search-entry','border','1px solid '+('#3B3B40' if dark else '#D8D8DD'))
 expect('.search-entry:focus','border-color','#818CF8' if dark else '#6366F1')
 return rules
