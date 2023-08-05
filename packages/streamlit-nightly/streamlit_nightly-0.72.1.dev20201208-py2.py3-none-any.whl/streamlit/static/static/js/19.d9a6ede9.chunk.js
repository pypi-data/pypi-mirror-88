(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[19],{1855:function(e,t){},1867:function(e,t){},1869:function(e,t){},1880:function(e,t){},1902:function(e,t){},3823:function(e,t,a){"use strict";a.r(t);var n=a(9),i=a(13),r=a(20),o=a(21),c=a(6),s=a(0),l=a.n(s),u=a(2244),h=a.n(u),p=a(1791),m=a.n(p),b=a(1814),f=a(1201),w=a(2235),d=a(1646),v=a(1641),g=a(2223),k=a(1206),S=a(232),j=a(18),O=a.n(j),x=a(30),E=a(134),y=a(43),V=a(1758),T=a(152),C=a.n(T),M=a(29),L=function(e){Object(r.a)(a,e);var t=Object(o.a)(a);function a(){return Object(n.a)(this,a),t.apply(this,arguments)}return a}(Object(V.a)(Error)),F=function(e){Object(r.a)(a,e);var t=Object(o.a)(a);function a(){return Object(n.a)(this,a),t.apply(this,arguments)}return a}(Object(V.a)(Error)),N=function(){function e(){Object(n.a)(this,e)}return Object(i.a)(e,null,[{key:"get",value:function(){var t=Object(x.a)(O.a.mark((function t(){var a,n,i;return O.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(a=M.a.current,n=a.commandLine,i=a.userMapboxToken,e.token&&e.commandLine===n.toLowerCase()){t.next=10;break}if(""===i){t.next=6;break}e.token=i,t.next=9;break;case 6:return t.next=8,this.fetchToken("https://data.streamlit.io/tokens.json","mapbox");case 8:e.token=t.sent;case 9:e.commandLine=n.toLowerCase();case 10:return t.abrupt("return",e.token);case 11:case"end":return t.stop()}}),t,this)})));return function(){return t.apply(this,arguments)}}()},{key:"fetchToken",value:function(){var e=Object(x.a)(O.a.mark((function e(t,a){var n,i;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,C.a.get(t);case 3:if(n=e.sent,null!=(i=n.data[a])&&""!==i){e.next=7;break}throw new Error('Missing token "'.concat(a,'"'));case 7:return e.abrupt("return",i);case 10:throw e.prev=10,e.t0=e.catch(0),new F("".concat(e.t0.message," (").concat(t,")"));case 13:case"end":return e.stop()}}),e,null,[[0,10]])})));return function(t,a){return e.apply(this,arguments)}}()}]),e}();N.token=void 0,N.commandLine=void 0,N.isRunningLocal=function(){var e=window.location.hostname;return"localhost"===e||"127.0.0.1"===e};var D=a(84),J=a.n(D),P=a(135),z=function(e){var t=e.error,a=e.width,n=e.deltaType;return t instanceof L?l.a.createElement(P.a,{width:a,name:"No Mapbox token provided",message:l.a.createElement(l.a.Fragment,null,l.a.createElement("p",null,"To use ",l.a.createElement("code",null,"st.",n)," or ",l.a.createElement("code",null,"st.map")," you need to set up a Mapbox access token."),l.a.createElement("p",null,"To get a token, create an account at"," ",l.a.createElement("a",{href:"https://mapbox.com"},"https://mapbox.com"),". It's free for moderate usage levels!"),l.a.createElement("p",null,"Once you have a token, just set it using the Streamlit config option ",l.a.createElement("code",null,"mapbox.token")," and don't forget to restart your Streamlit server at this point if it's still running, then reload this tab."),l.a.createElement("p",null,"See"," ",l.a.createElement("a",{href:"https://docs.streamlit.io/cli.html#view-all-config-options"},"our documentation")," ","for more info on how to set config options."))}):t instanceof F?l.a.createElement(P.a,{width:a,name:"Error fetching Streamlit Mapbox token",message:l.a.createElement(l.a.Fragment,null,l.a.createElement("p",null,"This app requires an internet connection."),l.a.createElement("p",null,"Please check your connection and try again."),l.a.createElement("p",null,"If you think this is a bug, please file bug report"," ",l.a.createElement("a",{href:"https://github.com/streamlit/streamlit/issues/new/choose"},"here"),"."))}):l.a.createElement(P.a,{width:a,name:"Error fetching Streamlit Mapbox token",message:t.message})},A=function(e){return function(t){var a=function(a){Object(r.a)(c,a);var i=Object(o.a)(c);function c(a){var r;return Object(n.a)(this,c),(r=i.call(this,a)).initMapboxToken=Object(x.a)(O.a.mark((function e(){var t;return O.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,N.get();case 3:t=e.sent,r.setState({mapboxToken:t,isFetching:!1}),e.next=10;break;case 7:e.prev=7,e.t0=e.catch(0),r.setState({mapboxTokenError:e.t0,isFetching:!1});case 10:case"end":return e.stop()}}),e,null,[[0,7]])}))),r.render=function(){var a=r.state,n=a.mapboxToken,i=a.mapboxTokenError,o=a.isFetching,c=r.props.width;return i?l.a.createElement(z,{width:c,error:i,deltaType:e}):o?l.a.createElement(E.a,{body:"Loading...",kind:y.a.INFO,width:c}):l.a.createElement(t,Object.assign({mapboxToken:n},r.props))},r.state={isFetching:!0,mapboxToken:void 0,mapboxTokenError:void 0},r.initMapboxToken(),r}return c}(s.PureComponent);return a.displayName="withMapboxToken(".concat(t.displayName||t.name,")"),J()(a,t)}},I=a(5),q=a.n(I)()("div",{target:"e1q4dr930"})((function(e){var t=e.width;return{position:"relative",height:e.height,width:t}}),""),G=(a(1851),{classes:Object(c.a)(Object(c.a)(Object(c.a)({},f),v),d)});Object(k.registerLoaders)([g.CSVLoader]);var R=new w.JSONConverter({configuration:G}),W=function(e){Object(r.a)(a,e);var t=Object(o.a)(a);function a(){var e;Object(n.a)(this,a);for(var i=arguments.length,r=new Array(i),o=0;o<i;o++)r[o]=arguments[o];return(e=t.call.apply(t,[this].concat(r))).state={viewState:{bearing:0,pitch:0,zoom:11},initialized:!1,initialViewState:{}},e.componentDidMount=function(){e.setState({initialized:!0})},e.createTooltip=function(t){var a=e.props.element;if(!t||!t.object||null==a.tooltip)return!1;var n=JSON.parse(a.tooltip);return n.html?n.html=e.interpolate(t,n.html):n.text=e.interpolate(t,n.text),n},e.interpolate=function(e,t){var a=t.match(/{(.*?)}/g);return a&&a.forEach((function(a){var n=a.substring(1,a.length-1);e.object.hasOwnProperty(n)&&(t=t.replace(a,e.object[n]))})),t},e.onViewStateChange=function(t){var a=t.viewState;e.setState({viewState:a})},e}return Object(i.a)(a,[{key:"render",value:function(){var e=a.getDeckObject(this.props),t=this.state.viewState;return l.a.createElement(q,{className:"stDeckGlJsonChart",width:e.initialViewState.width,height:e.initialViewState.height},l.a.createElement(h.a,{viewState:t,onViewStateChange:this.onViewStateChange,height:e.initialViewState.height,width:e.initialViewState.width,layers:this.state.initialized?e.layers:[],getTooltip:this.createTooltip,controller:!0},l.a.createElement(b.StaticMap,{height:e.initialViewState.height,width:e.initialViewState.width,mapStyle:e.mapStyle&&("string"===typeof e.mapStyle?e.mapStyle:e.mapStyle[0]),mapboxApiAccessToken:this.props.mapboxToken})))}}],[{key:"getDerivedStateFromProps",value:function(e,t){var n=a.getDeckObject(e);if(!m()(n.initialViewState,t.initialViewState)){var i=Object.keys(n.initialViewState).reduce((function(e,a){return n.initialViewState[a]===t.initialViewState[a]?e:Object(c.a)(Object(c.a)({},e),{},{[a]:n.initialViewState[a]})}),{});return{viewState:Object(c.a)(Object(c.a)({},t.viewState),i),initialViewState:n.initialViewState}}return null}}]),a}(s.PureComponent);W.getDeckObject=function(e){var t=e.element,a=e.width,n=e.height,i=JSON.parse(t.json);return n?(i.initialViewState.height=n,i.initialViewState.width=a):(i.initialViewState.height||(i.initialViewState.height=500),t.useContainerWidth&&(i.initialViewState.width=a)),delete i.views,R.convert(i)};var _=A("st.pydeck_chart")(Object(S.a)(W));a.d(t,"default",(function(){return _}))}}]);
//# sourceMappingURL=19.d9a6ede9.chunk.js.map