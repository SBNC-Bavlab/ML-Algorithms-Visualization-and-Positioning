const initialInnerWidth = innerWidth;
const refreshOnResize = () => {
    if(innerWidth !== initialInnerWidth) {
        window.history.go(0)
    }
};
window.addEventListener("resize", refreshOnResize);
const combinations = [{0: ["Köpek", "Köpek", "Köpek", "Köpek"],
                        1: ["Kedi", "Köpek", "Köpek", "Kedi"],
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
const initialText = "Anahtarı çevirerek isimle fotoğrafı eşleştirmeye çalışın";
const svgSection0 = d3_v4.select("#section0")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .style("background-color", "orange");


svgSection0.append("foreignObject")
        .attr("class", "info_text")
        .attr("width", innerWidth * 0.7)
        .attr("height", innerHeight * 0.3)
        .attr("x", innerWidth * 0.05)
        .attr("y", innerHeight * 0.3)
        .append("xhtml:body")
        .attr("class", "text_itself")
        .style("color", "white")
        .style("font", innerWidth * 0.02 + "px 'Arial'")
        .html("Bu örnekte Yapay Sinir Ağlarının çalışma prensibini inceleyeceğiz. <br><br>" +
            "Size sırasıyla kedi ve köpek resimleri gösterilecek yapmanız gereken anahtarı çevirerek isim ile resmi eşleştirmek" +
            "<br><br>Unutmadan söyleyelim anahtarı çevirdikçe önceden ayarladığınız eşleşmelerde değişebilir buna da dikkat etmelisiniz." +
            "<br><br>Bakalım yüzde kaçlık tahmin başarısı yakalayacaksınız." +
            "<br><br>Bol şans!");

const svgSection1 = d3_v4.select("#section1")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .style("background-color", "orange");
let indexOfFirstKnob = 0;
let indexOfSecondKnob = 0;
const positionForFirstCase = [innerWidth * 0.412, innerHeight * 0.275];
const positionsForSecondCase = [[innerWidth * 0.412, innerHeight * 0.1], [innerWidth * 0.412, innerHeight * 0.45]];
const trials = [false, false, false, false];
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
    .attr("id", "knob")
    .attr("opacity", "0")
    .attr("transform", "translate(" + positionsForSecondCase[0][0]+ ", " + positionsForSecondCase[0][1] + " ) scale(" + innerWidth * 0.00064 + ")")
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
        //Check trials to warn
        if(animalIndex === 2 && helpWarning){
            trials[indexOfSecondKnob] = true;
            let allExhausted = true;
            for(let i = 0; i < trials.length && allExhausted; i++){
                if(!trials[i]){
                    allExhausted = false;
                }
            }

            if(allExhausted){
                svgSection1.select("text.explanation")
                    .transition()
                        .text("Görünüşe göre tek bir anahtar ile bunu başarması zor.")
                    .transition()
                        .delay(3000)
                        .text("İşte size bir anahtar daha böylece kombinasyon sayısı artacak.")
                    .transition()
                        .delay(3000);
                switchToSecondCase();
                helpWarning = false;
            }
        }

    });
svgSection1.append("g")
    .attr("class", "knob")
    .attr("id", "knob2")
    .attr("transform", "translate(" + positionForFirstCase[0] + ", " + positionForFirstCase[1] + ") scale(" + innerWidth * 0.00064 + ")")
    .call(vol_2);
const arrow_places = [{x: innerWidth * 0.42, y: innerHeight * 0.31, left:true, rotate: -50},
                    {x: innerWidth * 0.51, y: innerHeight * 0.26, left:false, rotate: 50}];
svgSection1
    .selectAll("image.arrow")
    .data(arrow_places)
    .enter()
        .append("svg:image")
        .attr("class", "arrow")
        .attr("x", 0)
        .attr("y", 0)
    .attr("opacity", "0")
        .attr("width", innerWidth * 0.06)
        .attr("height", innerWidth * 0.06)
    .attr("transform", (d) => {
        return "translate(" + d.x + "," + d.y + ") rotate(" + d.rotate + ") scale( " + innerWidth * 0.00035 +  " )";
    })
        .attr("xlink:href", (d) => {return "../static/icons/" + ((d.left) ? "left.png" : "right.png")})
    .on('click', function(){
        vol_2.redraw(3, 500);
    })
// Drawing Knob finished
const imageWidth = innerWidth * 0.1;
const imageHeight = innerWidth * 0.1;
const animalX = innerWidth * 0.3;
const animalY = innerHeight * 0.3;
const initTextX = innerWidth * 0.6;
const initTextY = innerHeight * 0.3 + imageHeight / 2;
const decisions = ["Kedi", "Köpek"];
let helpWarning = true;
const imagePosInitial = [{x: animalX, y: animalY, text: "Kedi", image: 'cat_1.png'},
                    {x: -300, y: 0, text: "Köpek", image: 'dog_1.png'},
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
const buttonWidth = innerWidth * 0.09;
const buttonHeight = innerHeight * 0.05;
const resetButtonGroup = svgSection1.append("g");
resetButtonGroup.append("rect")
    .attr("x", innerWidth * 0.45)
    .attr("y", innerHeight * 0.8)
    .attr("width", buttonWidth)
    .attr("height", buttonHeight)
    .attr("fill", "red");
resetButtonGroup
    .append("text")
    .attr("x", innerWidth * 0.45 + buttonWidth / 2)
    .attr("y", innerHeight * 0.8 + buttonHeight / 2)
    .attr("alignment-baseline", "middle")
    .attr("text-anchor", "middle")
    .attr("fill", "white")
    .style("font-size", innerWidth * 0.014 + "px")
    .text("Reset")
    .raise();
resetButtonGroup
    .attr("cursor", "pointer")
    .on("click", reset);
function reset(){
    initImagePos();
    svgSection1.select("text.explanation")
        .text(initialText);
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
                .attr("x", innerWidth * 0.35)
                .attr("y", innerHeight * 0.8)
                .attr("width", buttonWidth)
                .attr("height", buttonHeight)
                .attr("fill", "blue");
trainButtonGroup
    .append("text")
    .attr("x", innerWidth * 0.35 + buttonWidth / 2)
    .attr("y", innerHeight * 0.8 + buttonHeight / 2)
    .attr("alignment-baseline", "middle")
    .attr("text-anchor", "middle")
    .attr("fill", "white")
    .style("font-size", innerWidth * 0.014 + "px")
    .text("Öğret")
    .raise();
let animalIndex = 0;
trainButtonGroup
    .attr("cursor", "pointer")
    .on('click', () => {
        if(animalIndex < imagePos.length) {
            if(animalIndex === 1){
                svgSection1.select("text.explanation")
                    .text("Artık üç görseli birden ismi ile eşleştirmeniz gerekiyor.")
            } else if(animalIndex === 2){
                svgSection1.select("text.explanation")
                    .text("Şimdi de dört görseli birden ismi ile eşleştirmeniz gerekiyor.")
            }
            //Image positions set
            for (let i = imagePos.length - 2; i >= animalIndex; i--) {
                imagePos[i + 1].x = imagePos[i].x;
                imagePos[i + 1].y = imagePos[i].y;
            }
            imagePos[animalIndex].x = 0.8 * innerWidth;
            imagePos[animalIndex].y = 0.2 * innerHeight * animalIndex;
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
            decisionText[decisionText.length - 1].x = 0.8 * innerWidth + innerWidth * 0.03 + imageWidth;
            decisionText[decisionText.length - 1].y = 0.2 * innerHeight * animalIndex + imageHeight / 2;
            decisionText.push({x: initTextX, y: initTextY, text: decisions[0]});
            svgSection1.selectAll("text.decision")
                .data(decisionText)
                .enter()
                .append("text")
                .attr("class", "decision")
                .attr("text-anchor", "middle")
                .attr("alignment-baseline", "middle")
                .attr("font-size", innerWidth * 0.02)
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
                .text("Doğru bilme oranı: %" + accuracy);
            if(accuracy === 100) {
                svgSection1.select("text.explanation")
                    .text("Tebrikler! Hepsini doğru bilen ayarı buldunuz.")
            } else {
                svgSection1.select("text.explanation")
                    .text("Resetleyip daha yüksek skora ulaşmayı deneyebilirsiniz.")
            }
        }
});
function switchToSecondCase(){
    svgSection1.select("#knob")
        .transition()
            .delay(4000)
            .attr("opacity", "1");

    svgSection1.select("#knob2")
        .transition()
            .delay(4000)
            .attr("transform", "translate(" + positionsForSecondCase[1][0]+ ", " + positionsForSecondCase[1][1] + " )")
}
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
        .attr("font-size", innerWidth * 0.02)
        .attr("x", (d) => {return d.x})
        .attr("y", (d) => {return d.y})
        .text((d) => {return d.text});
svgSection1.append("text")
        .attr("class", "accuracy")
        .attr("x", innerWidth * 0.7)
        .attr("y", innerHeight * 0.85)
        .attr("opacity", "0")
        .attr("font-size", innerWidth * 0.02)
        .text("Doğru bilme oranı: ");
svgSection1.append("text")
        .attr("class", "explanation")
        .attr("x", innerWidth * 0.5)
        .attr("y", innerHeight * 0.05)
        .attr("alignment-baseline", "middle")
        .attr("text-anchor", "middle")
        .attr("font-size", innerWidth * 0.016)
        .text(initialText);
const rectPos = [innerWidth * 0.41, innerHeight * 0.1];
const rectSize = [innerWidth * 0.13, innerHeight * 0.6];
const screwSize = imageWidth * 0.1;
svgSection1.append("rect")
        .attr("x", rectPos[0])
        .attr("y", rectPos[1])
        .attr("width", rectSize[0])
        .attr("height", rectSize[1])
        .attr("fill", "gray")
        .lower();
const screwPos = [{x: rectPos[0], y: rectPos[1]},
                {x: rectPos[0] + rectSize[0] - screwSize, y: rectPos[1]},
                {x: rectPos[0], y: rectPos[1] + + rectSize[1] - screwSize},
                {x: rectPos[0] + rectSize[0] - screwSize, y: rectPos[1] + + rectSize[1] - screwSize}];
svgSection1.selectAll("image.screw")
    .data(screwPos)
    .enter()
        .append("svg:image")
        .classed('screw', true)
        .attr('x', function(d){
            return d.x;
        })
        .attr('y', function(d){
            return d.y;
        })
        .attr('width', screwSize)
        .attr('height', screwSize)
        .attr("xlink:href", "../static/icons/screw.png");
const svgSection2 = d3_v4.select("#section2")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .style("background-color", "white");
const next_button_group = svgSection2.append("g");
next_button_group.append("rect")
    .attr("class", "next_button")
    .attr("x", innerWidth * 0.1)
    .attr("y", innerHeight * 0.6)
    .attr("fill", "orange")
    .attr("width", innerWidth * 0.16)
    .attr("height", innerHeight * 0.07);
next_button_group
    .append("text")
    .attr("class", "next_button_text")
    .attr("x", innerWidth * 0.1 + innerWidth * 0.16 / 2)
    .attr("y", innerHeight * 0.6 + innerHeight * 0.07 / 2)
    .attr("text-anchor", "middle")
    .attr("alignment-baseline", "middle")
    .attr("color", "black")
    .attr("font-size", innerWidth * 0.02)
    .text("İlerle");
next_button_group
    .attr("cursor", "pointer");
next_button_group.on('click', () => {
   location.href = "ag"
});

svgSection2.append("foreignObject")
        .attr("class", "info_text")
        .attr("width", innerWidth * 0.7)
        .attr("height", innerHeight * 0.3)
        .attr("x", innerWidth * 0.05)
        .attr("y", innerHeight * 0.1)
        .append("xhtml:body")
        .attr("class", "text_itself")
        .style("color", "black")
        .style("font", innerWidth * 0.02 + "px 'Arial'")
        .html("Gerçekten de Yapay Sinir Ağları bu şekilde çalışıyor. <br><br>Fotoğraf ile onun yazısı arasında karmaşık bir ağ yapısı var " +
            "<br><br>Ağdaki her bir bağın bir sayısal değeri var ve o sayısal değerler her yeni fotoğraf geldikçe güncelleniyor böylece" +
            " algoritma en doğru sayısal değerleri bularak yüksek tahmin başarısı yakalamaya çalışıyor.<br><br>" +
            "Hadi şimdi gerçek bir yapay sinir ağı nasıl görünür ona bakalım.");