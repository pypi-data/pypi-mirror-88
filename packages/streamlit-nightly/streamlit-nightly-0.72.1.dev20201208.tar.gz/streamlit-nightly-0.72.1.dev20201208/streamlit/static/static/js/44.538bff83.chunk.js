(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[44],{3825:function(e,t,r){"use strict";r.r(t);var o=r(9),i=r(13),n=r(20),a=r(21),c=r(0),s=r.n(c),l=r(38),d=r(14),u=r(23),h=r(136),b=Object.freeze({default:"default",toggle:"toggle",toggle_round:"toggle_round"});Object.freeze({top:"top",right:"right",bottom:"bottom",left:"left"});function g(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,o)}return r}function p(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?g(Object(r),!0).forEach((function(t){m(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):g(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function m(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function f(e){var t=e.$disabled,r=e.$checked,o=e.$isIndeterminate,i=e.$isError,n=e.$isHovered,a=e.$isActive,c=e.$theme,s=e.$checkmarkType===b.toggle,l=c.colors;return t?s?l.sliderTrackFillDisabled:r||o?l.tickFillDisabled:l.tickFill:i&&(o||r)?a?l.tickFillErrorSelectedHoverActive:n?l.tickFillErrorSelectedHover:l.tickFillErrorSelected:i?a?l.tickFillErrorHoverActive:n?l.tickFillErrorHover:l.tickFillError:o||r?a?l.tickFillSelectedHoverActive:n?l.tickFillSelectedHover:l.tickFillSelected:a?s?l.sliderTrackFillActive:l.tickFillActive:n?s?l.sliderTrackFillHover:l.tickFillHover:s?l.sliderTrackFill:l.tickFill}function v(e){var t=e.$disabled,r=e.$theme.colors;return t?r.contentSecondary:r.contentPrimary}var k=Object(u.a)("label",(function(e){var t=e.$disabled,r=e.$labelPlacement;return{flexDirection:"top"===r||"bottom"===r?"column":"row",display:"flex",alignItems:"top"===r||"bottom"===r?"center":"flex-start",cursor:t?"not-allowed":"pointer",userSelect:"none"}}));k.displayName="Root";var $=Object(u.a)("span",(function(e){var t=e.$checked,r=e.$disabled,o=e.$isError,i=e.$isIndeterminate,n=e.$theme,a=e.$isFocusVisible,c=n.sizing,s=n.animation,l=r?n.colors.tickMarkFillDisabled:o?n.colors.tickMarkFillError:n.colors.tickMarkFill,d=encodeURIComponent('\n    <svg width="14" height="4" viewBox="0 0 14 4" fill="none" xmlns="http://www.w3.org/2000/svg">\n      <path d="M14 0.5H0V3.5H14V0.5Z" fill="'.concat(l,'"/>\n    </svg>\n  ')),u=encodeURIComponent('\n    <svg width="17" height="13" viewBox="0 0 17 13" fill="none" xmlns="http://www.w3.org/2000/svg">\n      <path d="M6.50002 12.6L0.400024 6.60002L2.60002 4.40002L6.50002 8.40002L13.9 0.900024L16.1 3.10002L6.50002 12.6Z" fill="'.concat(l,'"/>\n    </svg>\n  ')),h=n.borders.inputBorderRadius,b=function(e){var t=e.$disabled,r=e.$checked,o=e.$isError,i=e.$isIndeterminate,n=e.$theme,a=e.$isFocusVisible,c=n.colors;return t?c.tickFillDisabled:r||i?"transparent":o?c.borderError:a?c.borderSelected:c.tickBorder}(e);return{flex:"0 0 auto",transitionDuration:s.timing200,transitionTimingFunction:s.easeOutCurve,transitionProperty:"background-image, border-color, background-color",width:c.scale700,height:c.scale700,left:"4px",top:"4px",boxSizing:"border-box",borderLeftStyle:"solid",borderRightStyle:"solid",borderTopStyle:"solid",borderBottomStyle:"solid",borderLeftWidth:"3px",borderRightWidth:"3px",borderTopWidth:"3px",borderBottomWidth:"3px",borderLeftColor:b,borderRightColor:b,borderTopColor:b,borderBottomColor:b,borderTopLeftRadius:h,borderTopRightRadius:h,borderBottomRightRadius:h,borderBottomLeftRadius:h,outline:a&&t?"3px solid ".concat(n.colors.accent):"none",display:"inline-block",verticalAlign:"middle",backgroundImage:i?"url('data:image/svg+xml,".concat(d,"');"):t?"url('data:image/svg+xml,".concat(u,"');"):null,backgroundColor:f(e),backgroundRepeat:"no-repeat",backgroundPosition:"center",backgroundSize:"contain",marginTop:n.sizing.scale0,marginBottom:n.sizing.scale0,marginLeft:n.sizing.scale0,marginRight:n.sizing.scale0}}));$.displayName="Checkmark";var y=Object(u.a)("div",(function(e){var t=e.$theme,r=e.$checkmarkType,o=t.typography;return p({flex:r===b.toggle?"auto":null,verticalAlign:"middle"},function(e){var t,r=e.$labelPlacement,o=void 0===r?"":r,i=e.$theme,n=i.sizing.scale300;switch(o){case"top":t="Bottom";break;case"bottom":t="Top";break;case"left":t="Right";break;default:case"right":t="Left"}return"rtl"===i.direction&&"Left"===t?t="Right":"rtl"===i.direction&&"Right"===t&&(t="Left"),m({},"padding".concat(t),n)}(e),{color:v(e)},o.LabelMedium,{lineHeight:"24px"})}));y.displayName="Label";var R=Object(u.a)("input",{opacity:0,width:0,height:0,overflow:"hidden",margin:0,padding:0,position:"absolute"});R.displayName="Input";var w=Object(u.a)("div",(function(e){if(e.$checkmarkType===b.toggle){var t=e.$theme.borders.useRoundedCorners?e.$theme.borders.radius200:null;return p({},Object(h.b)(e.$theme.borders.border300),{alignItems:"center",backgroundColor:e.$theme.colors.mono100,borderTopLeftRadius:t,borderTopRightRadius:t,borderBottomRightRadius:t,borderBottomLeftRadius:t,boxShadow:e.$isFocusVisible?"0 0 0 3px ".concat(e.$theme.colors.accent):e.$theme.lighting.shadow400,outline:"none",display:"flex",justifyContent:"center",height:e.$theme.sizing.scale800,width:e.$theme.sizing.scale800})}if(e.$checkmarkType===b.toggle_round){var r=e.$theme.colors.toggleFill;return e.$disabled?r=e.$theme.colors.toggleFillDisabled:e.$checked&&e.$isError?r=e.$theme.colors.borderError:e.$checked&&(r=e.$theme.colors.toggleFillChecked),{backgroundColor:r,borderTopLeftRadius:"50%",borderTopRightRadius:"50%",borderBottomRightRadius:"50%",borderBottomLeftRadius:"50%",boxShadow:e.$isFocusVisible?"0 0 0 3px ".concat(e.$theme.colors.accent):e.$isHovered&&!e.$disabled?e.$theme.lighting.shadow500:e.$theme.lighting.shadow400,outline:"none",height:e.$theme.sizing.scale700,width:e.$theme.sizing.scale700,transform:e.$checked?"translateX(".concat("rtl"===e.$theme.direction?"-100%":"100%",")"):null,transition:"transform ".concat(e.$theme.animation.timing200)}}return{}}));w.displayName="Toggle";var O=Object(u.a)("div",(function(e){if(e.$checkmarkType===b.toggle){return{height:e.$theme.sizing.scale300,width:e.$theme.sizing.scale0,borderTopLeftRadius:e.$theme.borders.radius100,borderTopRightRadius:e.$theme.borders.radius100,borderBottomRightRadius:e.$theme.borders.radius100,borderBottomLeftRadius:e.$theme.borders.radius100,backgroundColor:e.$disabled?e.$theme.colors.sliderHandleInnerFillDisabled:e.$isActive&&e.$checked?e.$theme.colors.sliderHandleInnerFillSelectedActive:e.$isHovered&&e.$checked?e.$theme.colors.sliderHandleInnerFillSelectedHover:e.$theme.colors.sliderHandleInnerFill}}return e.$checkmarkType,b.toggle_round,{}}));O.displayName="ToggleInner";var T=Object(u.a)("div",(function(e){if(e.$checkmarkType===b.toggle){var t=e.$theme.borders.useRoundedCorners?e.$theme.borders.radius200:null;return{alignItems:"center",backgroundColor:f(e),borderTopLeftRadius:t,borderTopRightRadius:t,borderBottomRightRadius:t,borderBottomLeftRadius:t,display:"flex",height:e.$theme.sizing.scale600,justifyContent:e.$checked?"flex-end":"flex-start",marginTop:e.$theme.sizing.scale100,marginBottom:e.$theme.sizing.scale100,marginLeft:e.$theme.sizing.scale100,marginRight:e.$theme.sizing.scale100,width:e.$theme.sizing.scale1000}}if(e.$checkmarkType===b.toggle_round){var r=e.$theme.colors.toggleTrackFill;return e.$disabled?r=e.$theme.colors.toggleTrackFillDisabled:e.$isError&&e.$checked&&(r=e.$theme.colors.tickFillError),{alignItems:"center",backgroundColor:r,borderTopLeftRadius:"7px",borderTopRightRadius:"7px",borderBottomRightRadius:"7px",borderBottomLeftRadius:"7px",display:"flex",height:e.$theme.sizing.scale550,marginTop:e.$theme.sizing.scale200,marginBottom:e.$theme.sizing.scale100,marginLeft:e.$theme.sizing.scale200,marginRight:e.$theme.sizing.scale100,width:e.$theme.sizing.scale1000}}return{}}));T.displayName="ToggleTrack";var F=r(40);function j(e){return(j="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function x(){return(x=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var o in r)Object.prototype.hasOwnProperty.call(r,o)&&(e[o]=r[o])}return e}).apply(this,arguments)}function L(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function S(e,t){for(var r=0;r<t.length;r++){var o=t[r];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function E(e,t){return!t||"object"!==j(t)&&"function"!==typeof t?C(e):t}function B(e){return(B=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function C(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function z(e,t){return(z=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function M(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var P=function(e){function t(){var e,r;L(this,t);for(var o=arguments.length,i=new Array(o),n=0;n<o;n++)i[n]=arguments[n];return M(C(r=E(this,(e=B(t)).call.apply(e,[this].concat(i)))),"state",{isFocused:r.props.autoFocus||!1,isFocusVisible:!1,isHovered:!1,isActive:!1}),M(C(r),"onMouseEnter",(function(e){r.setState({isHovered:!0}),r.props.onMouseEnter(e)})),M(C(r),"onMouseLeave",(function(e){r.setState({isHovered:!1,isActive:!1}),r.props.onMouseLeave(e)})),M(C(r),"onMouseDown",(function(e){r.setState({isActive:!0}),r.props.onMouseDown(e)})),M(C(r),"onMouseUp",(function(e){r.setState({isActive:!1}),r.props.onMouseUp(e)})),M(C(r),"onFocus",(function(e){r.setState({isFocused:!0}),r.props.onFocus(e),Object(F.d)(e)&&r.setState({isFocusVisible:!0})})),M(C(r),"onBlur",(function(e){r.setState({isFocused:!1}),r.props.onBlur(e),!1!==r.state.isFocusVisible&&r.setState({isFocusVisible:!1})})),M(C(r),"isToggle",(function(){return r.props.checkmarkType===b.toggle||r.props.checkmarkType===b.toggle_round})),r}var r,o,i;return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&z(e,t)}(t,e),r=t,(o=[{key:"componentDidMount",value:function(){var e=this.props,t=e.autoFocus,r=e.inputRef;t&&r.current&&r.current.focus()}},{key:"render",value:function(){var e=this.props.checkmarkType,t=this.props,r=t.overrides,o=void 0===r?{}:r,i=t.onChange,n=t.labelPlacement,a=void 0===n?this.isToggle()?"left":"right":n,s=t.inputRef,l=t.isIndeterminate,u=t.isError,h=t.disabled,b=t.value,g=t.name,p=t.type,m=t.checked,f=t.children,v=t.required,F=t.title,j=o.Root,L=o.Checkmark,S=o.Label,E=o.Input,B=o.Toggle,C=o.ToggleInner,z=o.ToggleTrack,M=Object(d.a)(j)||k,P=Object(d.a)(L)||$,H=Object(d.a)(S)||y,D=Object(d.a)(E)||R,I=Object(d.a)(B)||w,V=Object(d.a)(C)||O,A=Object(d.a)(z)||T,_={onChange:i,onFocus:this.onFocus,onBlur:this.onBlur},W={onMouseEnter:this.onMouseEnter,onMouseLeave:this.onMouseLeave,onMouseDown:this.onMouseDown,onMouseUp:this.onMouseUp},U={$isFocused:this.state.isFocused,$isFocusVisible:this.state.isFocusVisible,$isHovered:this.state.isHovered,$isActive:this.state.isActive,$isError:u,$checked:m,$isIndeterminate:l,$required:v,$disabled:h,$value:b,$checkmarkType:e},N=c.createElement(H,x({$labelPlacement:a},U,Object(d.b)(S)),f);return c.createElement(M,x({"data-baseweb":"checkbox",title:F||null,$labelPlacement:a},U,W,Object(d.b)(j)),("top"===a||"left"===a)&&N,this.isToggle()?c.createElement(A,x({role:"checkbox","aria-checked":l?"mixed":m,"aria-invalid":u||null},U,Object(d.b)(z)),c.createElement(I,x({},U,Object(d.b)(B)),c.createElement(V,x({},U,Object(d.b)(C))))):c.createElement(P,x({role:"checkbox",checked:m,"aria-checked":l?"mixed":m,"aria-invalid":u||null},U,Object(d.b)(L))),c.createElement(D,x({value:b,name:g,checked:m,required:v,"aria-checked":l?"mixed":m,"aria-describedby":this.props["aria-describedby"],"aria-errormessage":this.props["aria-errormessage"],"aria-invalid":u||null,"aria-required":v||null,disabled:h,type:p,ref:s},U,_,Object(d.b)(E))),("bottom"===a||"right"===a)&&N)}}])&&S(r.prototype,o),i&&S(r,i),t}(c.Component);M(P,"defaultProps",{overrides:{},checked:!1,disabled:!1,autoFocus:!1,isIndeterminate:!1,inputRef:c.createRef(),isError:!1,type:"checkbox",checkmarkType:b.default,onChange:function(){},onMouseEnter:function(){},onMouseLeave:function(){},onMouseDown:function(){},onMouseUp:function(){},onFocus:function(){},onBlur:function(){}});var H=P,D=r(28),I=function(e){Object(n.a)(r,e);var t=Object(a.a)(r);function r(){var e;Object(o.a)(this,r);for(var i=arguments.length,n=new Array(i),a=0;a<i;a++)n[a]=arguments[a];return(e=t.call.apply(t,[this].concat(n))).state={value:e.initialValue},e.setWidgetValue=function(t){var r=e.props.element.id;e.props.widgetMgr.setBoolValue(r,e.state.value,t)},e.onChange=function(t){var r=t.target.checked;e.setState({value:r},(function(){return e.setWidgetValue({fromUi:!0})}))},e.render=function(){var t=e.props,r=t.theme,o=t.width,i=r.colors,n=r.fontSizes,a=r.radii,c={width:o};return s.a.createElement("div",{className:"row-widget stCheckbox",style:c},s.a.createElement(H,{checked:e.state.value,disabled:e.props.disabled,onChange:e.onChange,overrides:{Root:{style:function(e){var t=e.$isFocused;return{marginBottom:0,marginTop:0,paddingRight:n.twoThirdSmDefault,backgroundColor:t?i.lightestGray:"",borderTopLeftRadius:a.md,borderTopRightRadius:a.md,borderBottomLeftRadius:a.md,borderBottomRightRadius:a.md}}},Checkmark:{style:function(e){var t=e.$isFocusVisible,r=e.$checked;return{borderLeftWidth:"2px",borderRightWidth:"2px",borderTopWidth:"2px",borderBottomWidth:"2px",outline:0,boxShadow:t&&r?"0 0 0 0.2rem ".concat(Object(D.transparentize)(i.primary,.5)):""}}},Label:{style:{color:i.bodyText}}}},e.props.element.label))},e}return Object(i.a)(r,[{key:"componentDidMount",value:function(){this.setWidgetValue({fromUi:!1})}},{key:"initialValue",get:function(){var e=this.props.element.id,t=this.props.widgetMgr.getBoolValue(e);return void 0!==t?t:this.props.element.default}}]),r}(s.a.PureComponent),V=Object(l.withTheme)(I);r.d(t,"default",(function(){return V}))}}]);
//# sourceMappingURL=44.538bff83.chunk.js.map