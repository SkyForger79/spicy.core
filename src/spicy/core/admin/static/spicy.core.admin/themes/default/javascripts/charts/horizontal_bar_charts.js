(function(){$(function(){var e,t,n,r,i,s,o;o=function(e,t,n,r){var i;return i="body",$('<div id="tooltip3" class="tooltip">'+n+"</div>").css({position:"absolute",display:"none",top:t-35,left:e-5,"z-index":"9999",color:"#fff","font-size":"11px",opacity:.8}).prependTo(i).show()},s=void 0,e=[],i=0;while(i<=3)e.push([parseInt(Math.random()*30),i]),i+=1;t=[],i=0;while(i<=3)t.push([parseInt(Math.random()*30),i]),i+=1;n=[],i=0;while(i<=3)n.push([parseInt(Math.random()*30),i]),i+=1;return r=new Array,r.push({data:e,bars:{horizontal:!0,show:!0,barWidth:.2,order:1}}),r.push({data:t,bars:{horizontal:!0,show:!0,barWidth:.2,order:2}}),r.push({data:n,bars:{horizontal:!0,show:!0,barWidth:.2,order:3}}),$.plot($("#placeholder1_hS"),r,{grid:{hoverable:!0}}),$("#placeholder1_hS").bind("plothover",function(e,t,n){var r,u;if(!n)return $(".tooltip").remove(),s=null;if(s!==n.datapoint){s=n.datapoint,$(".tooltip").remove(),r=n.datapoint[0];if(n.series.bars.order){i=0;while(i<n.series.data.length)n.series.data[i][3]===n.datapoint[0]&&(r=n.series.data[i][0]),i++}return u=n.datapoint[1],o(n.pageX+5,n.pageY+5,r+" = "+u)}})})}).call(this);