var theValue = 0;
var slider = d3.sliderHorizontal()
.min(1)
.max(15)
.step(1)
.width(510)
.displayValue(false)
.on('onchange', val => {
    theValue = val;
    update(theValue);
});

d3.select("svg").append("g").transition().duration(1000).delay(1400)
    .attr("transform", "translate(" + innerWidth * 0.95 + ",100) rotate(90)")
    .call(slider);;