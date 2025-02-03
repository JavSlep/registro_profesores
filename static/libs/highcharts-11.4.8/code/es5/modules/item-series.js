!/**
 * Highcharts JS v11.4.8 (2024-08-29)
 *
 * Item series type for Highcharts
 *
 * (c) 2019 Torstein Honsi
 *
 * License: www.highcharts.com/license
 */function(t){"object"==typeof module&&module.exports?(t.default=t,module.exports=t):"function"==typeof define&&define.amd?define("highcharts/modules/item-series",["highcharts"],function(e){return t(e),t.Highcharts=e,t}):t("undefined"!=typeof Highcharts?Highcharts:void 0)}(function(t){"use strict";var e=t?t._modules:{};function o(e,o,i,r){e.hasOwnProperty(o)||(e[o]=r.apply(null,i),"function"==typeof CustomEvent&&t.win.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:o,module:e[o]}})))}o(e,"Series/Item/ItemPoint.js",[e["Core/Series/SeriesRegistry.js"],e["Core/Utilities.js"]],function(t,e){var o,i=this&&this.__extends||(o=function(t,e){return(o=Object.setPrototypeOf||({__proto__:[]})instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&(t[o]=e[o])})(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw TypeError("Class extends value "+String(e)+" is not a constructor or null");function i(){this.constructor=t}o(t,e),t.prototype=null===e?Object.create(e):(i.prototype=e.prototype,new i)}),r=t.series.prototype.pointClass,s=t.seriesTypes.pie.prototype.pointClass,n=e.extend,a=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return i(e,t),e}(s);return n(a.prototype,{haloPath:r.prototype.haloPath}),a}),o(e,"Series/Item/ItemSeriesDefaults.js",[e["Core/Series/SeriesDefaults.js"],e["Core/Utilities.js"]],function(t,e){return{endAngle:void 0,innerSize:"40%",itemPadding:.1,layout:"vertical",marker:(0,e.merge)(t.marker,{radius:null}),rows:void 0,crisp:!1,showInLegend:!0,startAngle:void 0}}),o(e,"Series/Item/ItemSeries.js",[e["Series/Item/ItemPoint.js"],e["Series/Item/ItemSeriesDefaults.js"],e["Core/Series/SeriesRegistry.js"],e["Core/Utilities.js"]],function(t,e,o,i){var r,s=this&&this.__extends||(r=function(t,e){return(r=Object.setPrototypeOf||({__proto__:[]})instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&(t[o]=e[o])})(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw TypeError("Class extends value "+String(e)+" is not a constructor or null");function o(){this.constructor=t}r(t,e),t.prototype=null===e?Object.create(e):(o.prototype=e.prototype,new o)}),n=o.seriesTypes.pie,a=i.defined,l=i.extend,h=i.fireEvent,p=i.isNumber,u=i.merge,c=i.pick,f=function(t){function o(){return null!==t&&t.apply(this,arguments)||this}return s(o,t),o.prototype.animate=function(t){var e=this.group;e&&(t?e.attr({opacity:0}):e.animate({opacity:1},this.options.animation))},o.prototype.drawDataLabels=function(){if(this.center&&this.slots)t.prototype.drawDataLabels.call(this);else for(var e=0,o=this.points;e<o.length;e++)o[e].destroyElements({dataLabel:1})},o.prototype.drawPoints=function(){for(var t=this.options,e=this.chart.renderer,o=t.marker,i=this.borderWidth%2?.5:1,r=this.getRows(),s=Math.ceil(this.total/r),n=this.chart.plotWidth/s,h=this.chart.plotHeight/r,p=this.itemSize||Math.min(n,h),u=0,f=0,d=this.points;f<d.length;f++){var g=d[f],y=g.marker||{},m=y.symbol||o.symbol,v=c(y.radius,o.radius),w=a(v)?2*v:p,S=w*t.itemPadding,_=void 0,b=void 0,j=void 0,M=void 0,C=void 0,A=void 0,P=void 0;if(g.graphics=b=g.graphics||[],this.chart.styledMode||(j=this.pointAttribs(g,g.selected&&"select")),!g.isNull&&g.visible){g.graphic||(g.graphic=e.g("point").add(this.group));for(var O=0;O<(g.y||0);++O){if(this.center&&this.slots){var I=this.slots.shift();M=I.x-p/2,C=I.y-p/2}else"horizontal"===t.layout?(M=u%s*n,C=h*Math.floor(u/s)):(M=n*Math.floor(u/r),C=u%r*h);M+=S,C+=S,P=A=Math.round(w-2*S),this.options.crisp&&(M=Math.round(M)-i,C=Math.round(C)+i),_={x:M,y:C,width:A,height:P},void 0!==v&&(_.r=v),j&&l(_,j);var x=b[O];x?x.animate(_):x=e.symbol(m,void 0,void 0,void 0,void 0,{backgroundSize:"within"}).attr(_).add(g.graphic),x.isActive=!0,b[O]=x,++u}}for(var E=0;E<b.length;E++){var x=b[E];if(!x)return;x.isActive?x.isActive=!1:(x.destroy(),b.splice(E,1),E--)}}},o.prototype.getRows=function(){var t,e=this.chart,o=this.total||0,i=this.options.rows;if(!i){if(t=e.plotWidth/e.plotHeight,i=Math.sqrt(o),t>1)for(i=Math.ceil(i);i>0&&!(o/i/i>t);)i--;else for(i=Math.floor(i);i<o&&!(o/i/i<t);)i++}return i},o.prototype.getSlots=function(){for(var t,e,o,i,r,s,n,a,l,h,p,u,c=this.center,f=c[2],d=this.slots=this.slots||[],g=this.endAngleRad-this.startAngleRad,y=this.options.rows,m=g%(2*Math.PI)==0,v=this.total||0,w=c[3],S=0,_=Number.MAX_VALUE,b=(f-w)/f;_>v+(p&&m?p.length:0);){h=_,d.length=0,_=0,p=u,u=[],l=f/++S/2,y?(w=(l-y)/l*f)>=0?l=y:(w=0,b=1):l=Math.floor(l*b);for(var j=l;j>0;j--)r=Math.ceil((i=g*(o=(w+j/l*(f-w-S))/2))/S),u.push({rowRadius:o,rowLength:i,colCount:r}),_+=r+1}if(p){for(var M=h-this.total-(m?p.length:0),C=function(t){M>0&&(t.row.colCount--,M--)};M>0;)p.map(function(t){return{angle:t.colCount/t.rowLength,row:t}}).sort(function(t,e){return e.angle-t.angle}).slice(0,Math.min(M,Math.ceil(p.length/2))).forEach(C);for(var A=0,P=p;A<P.length;A++){var j=P[A],O=j.rowRadius,I=j.colCount;for(a=0,s=I?g/I:0;a<=I;a+=1)n=this.startAngleRad+a*s,t=c[0]+Math.cos(n)*O,e=c[1]+Math.sin(n)*O,d.push({x:t,y:e,angle:n})}return d.sort(function(t,e){return t.angle-e.angle}),this.itemSize=S,d}},o.prototype.translate=function(e){0===this.total&&p(this.options.startAngle)&&p(this.options.endAngle)&&(this.center=this.getCenter()),this.slots||(this.slots=[]),p(this.options.startAngle)&&p(this.options.endAngle)?(t.prototype.translate.call(this,e),this.slots=this.getSlots()):(this.generatePoints(),h(this,"afterTranslate"))},o.defaultOptions=u(n.defaultOptions,e),o}(n);return l(f.prototype,{markerAttribs:void 0,pointClass:t}),o.registerSeriesType("item",f),f}),o(e,"masters/modules/item-series.src.js",[e["Core/Globals.js"]],function(t){return t})});