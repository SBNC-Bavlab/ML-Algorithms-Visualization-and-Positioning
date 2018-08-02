var theValue = 0;
var slider = d3.sliderHorizontal()
.min(4)
.max(31)
.step(1)
.width(510)
.displayValue(false)
.on('onchange', val => {
    theValue = val;
    update(theValue);
});

d3.select("#section2").append("g").attr("class", "sliderAll").transition().duration(1000).delay(1400)
    .attr("transform", "translate(" + innerWidth * 0.96 + ",100) rotate(90)")
    .call(slider);