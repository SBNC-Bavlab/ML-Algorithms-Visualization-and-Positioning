const combinations = [{0: ["Kedi", "Köpek", "Köpek", "Kedi"],
                        1: ["Köpek", "Köpek", "Köpek", "Köpek"],
                        2: ["Köpek", "Kedi", "Köpek", "Kedi"],
                        3: ["Kedi", "Kedi", "Kedi", "Kedi"]},
                        {0: ["Köpek", "Kedi", "Köpek", "Kedi"],
                        1: ["Kedi", "Kedi", "Kedi", "Köpek"],
                        2: ["Köpek", "Kedi", "Köpek", "Kedi"],
                        3: ["Kedi", "Köpek", "Kedi", "Köpek"]},
                        {0: ["Kedi", "Köpek", "Köpek", "Kedi"],
                        1: ["Kedi", "Köpek", "Kedi", "Köpek"],
                        2: ["Kedi", "Kedi", "Köpek", "Köpek"],
                        3: ["Köpek", "Kedi", "Köpek", "Kedi"]},
                        {0: ["Kedi", "Kedi", "Kedi", "Kedi"],
                        1: ["Kedi", "Köpek", "Kedi", "Köpek"],
                        2: ["Köpek", "Kedi", "Köpek", "Köpek"],
                        3: ["Köpek", "Köpek", "Kedi", "Kedi"]}];
const svgSection0 = d3_v4.select("#section0")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .style("background-color", "orange");
const svgSection1 = d3_v4.select("#section1")
                .attr("width", innerWidth)
                .attr("height", innerHeight);
let indexOfFirstKnob = 0;
let indexOfSecondKnob = 0;
// Drawing knob
function drawKnob(g, r) {
    g.append("image")
            .attr("x", -r)
            .attr("y", -r)
            .attr("width", 2 * r)
            .attr("height", 2 * r)
            .attr("xlink:href", "http://iop.io/demo/iopctrl/knob.png")
}

const vol = iopctrl.arcslider()
            .radius(50)
            .indicator(drawKnob)
            .ease("cubic-in");
vol.axis().orient("out")
        .normalize(true)
        .tickSize(10)
        .scale(d3.scale.ordinal()
                .domain(["1", "2", "3", "4"])
                .rangeBands([-Math.PI/2,  Math.PI/2]));

svgSection1.append("g")
    .attr("class", "knob")
    .attr("transform", "scale(0.5)")
    .attr("transform", "translate(300, 0)")
    .call(vol);

vol.onValueChanged(function(value){
    indexOfFirstKnob = +value - 1;
    const combination = combinations[indexOfFirstKnob][indexOfSecondKnob];
    for(let i = 0; i <= animalIndex; i++){
        decisionText[i].text = combination[i];
    }
    svgSection1.selectAll("text.decision")
        .text((d) => {return d.text});
});

//Second knob drawn
const vol_2 = iopctrl.arcslider()
                .radius(50)
                .indicator(drawKnob)
                .ease("cubic-in");
vol_2.axis().orient("out")
        .normalize(true)
        .tickSize(10)
        .scale(d3.scale.ordinal()
                .domain(["1", "2", "3", "4"])
                .rangeBands([-Math.PI/2, Math.PI/2]));
vol_2.onValueChanged(function(value){
        indexOfSecondKnob = +value - 1;
        const combination = combinations[indexOfFirstKnob][indexOfSecondKnob];
        for(let i = 0; i <= animalIndex; i++){
            decisionText[i].text = combination[i];
        }
        svgSection1.selectAll("text.decision")
            .text((d) => {return d.text});
    });
svgSection1.append("g")
    .attr("class", "knob")
    .attr("transform", "scale(0.5)")
    .attr("transform", "translate(300, 200)")
    .call(vol_2);

// Drawing Knob finished
const imageWidth = 150;
const imageHeight = 150;
const animalX = 100;
const animalY = 230;
const initTextX = 600;
const initTextY = 240 + imageHeight / 2;
const decisions = ["Kedi", "Köpek"];
const imagePosInitial = [{x: animalX, y: animalY, text: "Kedi", image: 'cat_1.png'},
                    {x: 0, y: 0, text: "Köpek", image: 'dog_1.png'},
                    {x: -300, y: 0, text: "Kedi", image: 'cat_2.png'},
                    {x: -300, y: 0, text: "Köpek", image: 'dog_2.png'}];
const decisionText = [{x: initTextX, y: initTextY, text: decisions[0]}];
let imagePos = [];
function initImagePos() {
    imagePos.length = 0;
    for(let i = 0; i < imagePosInitial.length; i++){
        imagePos.push(Object.assign({}, imagePosInitial[i]))
    }
}
initImagePos();
const buttonWidth = 140;
const buttonHeight = 50;
const resetButtonGroup = svgSection1.append("g");
resetButtonGroup.append("rect")
    .attr("x", 850)
    .attr("y", 220)
    .attr("width", buttonWidth)
    .attr("height", buttonHeight)
    .attr("fill", "red");
resetButtonGroup
    .append("text")
    .attr("x", 850 + buttonWidth / 2)
    .attr("y", 220 + buttonHeight / 2)
    .attr("alignment-baseline", "middle")
    .attr("text-anchor", "middle")
    .attr("fill", "white")
    .style("font-size", "20px")
    .text("Reset")
    .raise();
resetButtonGroup
    .attr("cursor", "pointer")
    .on("click", reset);
function reset(){
    initImagePos();
    svgSection1.selectAll("image.animal")
                .data(imagePos)
                .transition()
                .attr("x", (d) => {return d.x})
                .attr("y", (d) => {return d.y});
    animalIndex = 0;
    decisionText.length = 0;
    decisionText.push({x: initTextX, y: initTextY, text: decisions[0]});
    svgSection1.selectAll("text.decision")
                .data(decisionText)
                .attr("x", (d) => {return d.x})
                .attr("y", (d) => {return d.y})
                    .exit()
                    .remove();
    svgSection1.select("text.accuracy")
        .transition()
        .attr("opacity", "0")
}
const trainButtonGroup = svgSection1.append("g");
trainButtonGroup.append("rect")
                .attr("class", "button")
                .attr("x", 700)
                .attr("y", 220)
                .attr("width", buttonWidth)
                .attr("height", buttonHeight)
                .attr("fill", "orange");
trainButtonGroup
    .append("text")
    .attr("x", 700 + buttonWidth / 2)
    .attr("y", 220 + buttonHeight / 2)
    .attr("alignment-baseline", "middle")
    .attr("text-anchor", "middle")
    .attr("fill", "white")
    .style("font-size", "20px")
    .text("Öğret")
    .raise();
let animalIndex = 0;
trainButtonGroup
    .attr("cursor", "pointer")
    .on('click', () => {
        if(animalIndex < imagePos.length) {
            //Image positions set
            for (let i = imagePos.length - 2; i >= animalIndex; i--) {
                imagePos[i + 1].x = imagePos[i].x;
                imagePos[i + 1].y = imagePos[i].y;
            }
            imagePos[animalIndex].x = 300 * animalIndex + 120;
            imagePos[animalIndex].y = 500;
            svgSection1.selectAll("image.animal")
                .data(imagePos)
                .transition()
                .attr("x", (d) => {
                    return d.x
                })
                .attr("y", (d) => {
                    return d.y
                });

            //Texts set
            decisionText[decisionText.length - 1].x = 300 * animalIndex + 160;
            decisionText[decisionText.length - 1].y = 490;
            decisionText.push({x: initTextX, y: initTextY, text: decisions[0]});
            const texts = svgSection1.selectAll("text.decision")
                .data(decisionText)
                .enter()
                .append("text")
                .attr("class", "decision")
                .attr("text-anchor", "middle")
                .attr("alignment-baseline", "middle")
                .attr("font-size", "30")
                .text((d) => {
                    return d.text
                });
            svgSection1.selectAll("text.decision")
                .attr("x", (d) => {
                    return d.x
                })
                .attr("y", (d) => {
                    return d.y
                });
            animalIndex++;

            const combination = combinations[indexOfFirstKnob][indexOfSecondKnob];
            for (let i = 0; i <= animalIndex; i++) {
                decisionText[i].text = combination[i];
            }
            svgSection1.selectAll("text.decision")
                .text((d) => {
                    return d.text
                })
        }
        if (animalIndex >= imagePos.length){
            let valid = 0;
            let invalid = 0;
            for(let i = 0; i < imagePos.length; i++){
                const image = imagePos[i];
                const decision = decisionText[i];
                if(image.text === decision.text){
                    valid++;
                } else {
                    invalid++;
                }
            }
            const accuracy = valid / (valid + invalid) * 100;
            svgSection1.select("text.accuracy")
                .transition()
                .attr("opacity", "1")
                .attr("font-size", "23")
                .text("Doğru bilme oranı: %" + accuracy);
        }
});
// Layout
svgSection1.selectAll("image.animal")
    .data(imagePos)
    .enter()
        .append("svg:image")
        .attr("class", "animal")
        .attr("x", (d) => {return d.x})
        .attr("y", (d) => {return d.y})
        .attr("width", imageWidth)
        .attr("height", imageHeight)
        .attr("xlink:href", (d) => {return "../static/icons/" + d.image});

//Texts laid out
svgSection1.selectAll("text.decision")
    .data(decisionText)
    .enter()
        .append("text")
        .attr("class", "decision")
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .attr("font-size", "30")
        .attr("x", (d) => {return d.x})
        .attr("y", (d) => {return d.y})
        .text((d) => {return d.text});
svgSection1.append("text")
            .attr("class", "accuracy")
            .attr("x", innerWidth * 0.78)
            .attr("y", innerHeight * 0.76)
            .attr("opacity", "0")
            .text("Doğru bilme oranı: ");
