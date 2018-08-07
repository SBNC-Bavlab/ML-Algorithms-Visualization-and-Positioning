
const train_data = [
  ["Sarı", 1, "Kavun"], ["Sarı", 1, "Kavun"], ["Sarı", 1, "Kavun"],  ["Sarı", 1, "Kavun"], ["Sarı", 1, "Kavun"],
  ["Sarı", 2, "Kavun"], ["Sarı", 2, "Kavun"], ["Sarı", 2, "Kavun"], ["Sarı", 2, "Kavun"], ["Sarı", 2, "Kavun"],
  ["Sarı", 3, "Kavun"], ["Sarı", 3, "Kavun"], ["Sarı", 3, "Kavun"], ["Sarı", 3, "Kavun"], ["Sarı", 3, "Kavun"], ["Sarı", 3, "Kavun"], ["Sarı", 3, "Kavun"],
  ["Sarı", 4, "Kavun"], ["Sarı", 4, "Kavun"], ["Sarı", 4, "Kavun"], ["Sarı", 4, "Kavun"],
  ["Sarı", 5, "Kavun"], ["Sarı", 5, "Kavun"], ["Sarı", 5, "Kavun"], ["Sarı", 5, "Kavun"],
  ["Sarı", 6, "Kavun"], ["Sarı", 6, "Kavun"], ["Sarı", 6, "Kavun"],
  ["Sarı", 7, "Kavun"],
  ["Sarı", 10, "Kavun"], ["Sarı", 10, "Kavun"],
  ["Sarı", 12, "Kavun"], ["Sarı", 12, "Kavun"],
  ["Yeşil", 3, "Karpuz"],
  ["Yeşil", 4, "Karpuz"],
  ["Yeşil", 6, "Karpuz"], ["Yeşil", 6, "Karpuz"],
  ["Yeşil", 7, "Karpuz"],
  ["Yeşil", 9, "Karpuz"], ["Yeşil", 9, "Karpuz"], ["Yeşil", 9, "Karpuz"], ["Yeşil", 9, "Karpuz"],
  ["Yeşil", 10, "Karpuz"], ["Yeşil", 10, "Karpuz"], ["Yeşil", 10, "Karpuz"], ["Yeşil", 10, "Karpuz"], ["Yeşil", 10, "Karpuz"],
  ["Yeşil", 11, "Karpuz"], ["Yeşil", 11, "Karpuz"], ["Yeşil", 11, "Karpuz"], ["Yeşil", 11, "Karpuz"], ["Yeşil", 11, "Karpuz"],
  ["Yeşil", 12, "Karpuz"], ["Yeşil", 12, "Karpuz"], ["Yeşil", 12, "Karpuz"], ["Yeşil", 12, "Karpuz"],
  ["Yeşil", 13, "Karpuz"], ["Yeşil", 13, "Karpuz"], ["Yeşil", 13, "Karpuz"], ["Yeşil", 13, "Karpuz"], ["Yeşil", 13, "Karpuz"], ["Yeşil", 13, "Karpuz"], ["Yeşil", 13, "Karpuz"],
  ["Yeşil", 14, "Karpuz"], ["Yeşil", 14, "Karpuz"], ["Yeşil", 14, "Karpuz"], ["Yeşil", 14, "Karpuz"], ["Yeşil", 14, "Karpuz"], ["Yeşil", 14, "Karpuz"], ["Yeşil", 14, "Karpuz"], ["Yeşil", 14, "Karpuz"],
];

const test_data = [["Sarı", 3, "Kavun"], ["Sarı", 4, "Kavun"], ["Sarı", 5, "Kavun"],
  ["Sarı", 5, "Kavun"], ["Sarı", 5, "Kavun"], ["Sarı", 6, "Kavun"],
  ["Sarı", 6, "Kavun"], ["Yeşil", 7, "Karpuz"], ["Yeşil", 7, "Karpuz"],
  ["Sarı", 7, "Kavun"], ["Yeşil", 8, "Karpuz"], ["Yeşil", 9, "Karpuz"],
  ["Yeşil", 9, "Karpuz"], ["Yeşil", 9, "Karpuz"], ["Yeşil", 11, "Karpuz"],
  ["Yeşil", 12, "Karpuz"], ["Yeşil", 12, "Karpuz"], ["Yeşil", 13, "Karpuz"]];

const buttonWidth = innerWidth * 0.16;
const buttonHeight = innerHeight * 0.07;
const maxFrequency = 8;
const rectWidth = innerWidth / 22;
const rectHeight = 70;
const maxDiameter = 14;
const buttonX = innerWidth * 0.7;
const buttonY = innerHeight * 0.84;
const radius_label = [4,6,7,10,12,13,16,18,21,23,24,27,30];

let fruitPlaces = [];
let validDiameterIndex = 1;
let radiusDict = {};
let rectangleData = [];
let isDatasetTraining = true;
function manipulateRectangleData(data){
    radiusDict = {};
    rectangleData = [];
    data.forEach((entry)=>{
        if (radiusDict.hasOwnProperty(entry[1])){
            radiusDict[entry[1]].push(entry[2]);
        } else {
            radiusDict[entry[1]] = [entry[2]];
        }
    });
    Object.keys(radiusDict).forEach(function(d, i){
        rectangleData.push({'x': innerWidth * (i + 1) * 0.07 - innerWidth * 0.05, 'y': 10, 'label': d, 'text': radius_label[i], 'color': 'beige'})
    });
}
function calculateFruitPlaces(){
    fruitPlaces = [];
    for(let i = 0; i < maxFrequency; i++){
        for(let j = 1; j <= maxDiameter; j++){
            if(j in radiusDict) {
                if (i < radiusDict[j].length) {
                    if (radiusDict[j][i] === 'Karpuz') {
                        fruitPlaces.push({'x': innerWidth * validDiameterIndex * 0.07 - innerWidth * 0.05, 'y': innerHeight * 0.086 * i + innerHeight * 0.1, 'fruit_img': 'watermelon.png'})
                    } else {
                        fruitPlaces.push({'x': innerWidth * validDiameterIndex * 0.07 - innerWidth * 0.05, 'y': innerHeight * 0.086 * i + innerHeight * 0.1, 'fruit_img': 'melon.png'})
                    }
                }
                validDiameterIndex++;
            }
        }
        validDiameterIndex = 1
    }
}

//Section 0
const s0svg = d3.select("#section0")
                .style("background-color", "blue")
                .attr("width", innerWidth)
                .attr("height", innerHeight);
const infotTextPosS0 = [{x : innerWidth * 0.05, y : innerHeight * 0.1, text: "<br><br><br>asgfadgsdfsad"}];
s0svg.selectAll("text.infoText")
        .data(infotTextPosS0)
        .enter()
            .append("foreignObject")
            .attr("width", innerWidth / 1.5)
            .attr("height", innerHeight * 0.5)
            .attr("x", (d)=>{
               return d.x;
            })
            .attr("y", (d)=>{
                return d.y;
            })
            .append("xhtml:body")
            .style("font", innerWidth * 0.03 + "px 'Arial'")
            .style("color", "white")
            .html((d)=>{
                return d.text;
            });


//Section 1

const s1svg = d3.select("#section1")
                .style("background-color", "blue")
                .attr("width", innerWidth)
                .attr("height", innerHeight);
const paletteHeight = innerHeight * 0.084;
const infoTextPost = [{x : innerWidth * 0.05, y : innerHeight * 0.15, text: "Elimizde Mehmet ve Ahmet'in tezgahlarındaki karpuz ve kavunların çap bilgileri var." +
    "<br><br>Amacımız karpuz ve kavunları birbirinden ayıran bir çap değeri bulmak." +
    "<br><br>Yani öyle bir çap değeri bulmalıyız ki onun üstündekilere karpuz altındakilere kavun diyebilelim"}] //'Faruk reistir'

s1svg.selectAll("text.infoText")
        .data(infoTextPost)
        .enter()
        .append("foreignObject")
        .attr("width", innerWidth / 1.5)
        .attr("height", innerHeight * 0.5)
        .attr("x", (d)=>{
           return d.x;
        })
        .attr("y", (d)=>{
            return d.y;
        })
        .append("xhtml:body")
        .style("font", innerWidth * 0.03 + "px 'Arial'")
        .style("color", "white")
        .html((d)=>{
            return d.text;
        });
//Initial settings
manipulateRectangleData(train_data);
calculateFruitPlaces();

const s2svg = d3.select("#section2")
    .attr("width", innerWidth)
    .attr("height", innerHeight);

s2svg.append("text")
    .attr("x", innerWidth / 2.1)
    .attr("y", innerHeight * 0.9)
    .attr("baseline-alignment", "middle")
    .attr("text-anchor", "middle")
    .attr("font-size", innerWidth * 0.04)
    .attr("class", "tezgah_name")
    .text("Mehmet'in Tezgahı");

s2svg.append("rect")
        .attr('x', buttonX)
        .attr('y', buttonY)
        .attr('width', buttonWidth)
        .attr('height', buttonHeight)
        .attr("fill", "green")
        .attr('class', "button_rect")
        .attr('rx', 15)
        .attr('ry', 15)
        .on('click', ()=>{
            (isDatasetTraining)? calculateTest() : againTrain()
        });

s2svg.append("text")
    .attr("x", buttonX + buttonWidth / 2)
    .attr("y", buttonY + buttonHeight / 2)
    .attr("alignment-baseline", "middle")
    .attr("text-anchor", "middle")
    .attr("font-size", innerWidth * 0.018)
    .attr("class", "button_text")
    .attr("fill", "white")
    .attr("cursor", "pointer")
    .on('click', () =>{ (isDatasetTraining)? calculateTest() : againTrain() })
    .text("Modeli Test Et");


var rectangles = s2svg.selectAll("rect.palette")
                            .data(rectangleData)
                            .enter()
                            .append("rect")
                            .attr("fill","beige")
                            .attr("class", "palette")
                            .attr("x", function (d) { return d.x; })
                            .attr("y", function (d) { return d.y; })
                            .attr("rx", 15)
                            .attr("width", rectWidth)
                            .attr("height", function (d, i) { return paletteHeight * radiusDict[Object.keys(radiusDict)[i]].length + 80});
s2svg.selectAll("text.label")
    .data(rectangleData)
    .enter()
    .append('text')
    .attr("alignment-baseline", "middle")
    .attr("text-anchor", "middle")
    .classed('label', true)
    .transition()
    .duration(1000)
    .attr('x', calculateXForText)
    .attr('y', function (d) {
        return innerHeight * 0.06;
    })
    .attr("fill", "black")
    .text(function (d) {
        return d.text + "cm";
    })
    .style("font-size", innerWidth / 62 + "px");
s2svg.selectAll("image")
    .data(fruitPlaces)
    .enter()
        .append("svg:image")
        .classed('fruit', true)
        .transition().delay(1000).ease(d3.easeElastic).duration(2000)
        .attr('x', function(d){
            return d.x;
        })
        .attr('y', function(d){
            return d.y;
        })
        .attr('width', rectWidth)
        .attr('height', rectHeight)
        .attr("xlink:href", function (d) {
            return "../static/icons/" + d.fruit_img;
        });

const s3svg = d3.select("#section3")
                .attr("width", innerWidth)
                .attr("height", innerHeight);
const next_button_group = s3svg.append("g");
next_button_group.append("rect")
    .attr("class", "next_button")
    .attr("x", innerWidth * 0.1)
    .attr("y", innerHeight * 0.5)
    .attr("fill", "orange")
    .attr("width", buttonWidth)
    .attr("height", buttonHeight);
next_button_group
    .append("text")
    .attr("class", "next_button_text")
    .attr("x", innerWidth * 0.1 + buttonWidth / 2)
    .attr("y", innerHeight * 0.5 + buttonHeight / 2)
    .attr("text-anchor", "middle")
    .attr("alignment-baseline", "middle")
    .attr("color", "black")
    .attr("font-size", innerWidth * 0.02)
    .text("İlerle");
next_button_group
    .attr("cursor", "pointer")
next_button_group.on('click', () => {
   location.href = "gameOfThrones.html"
});

s2svg.selectAll(".tick > text").attr("fill", "white");

s3svg.append("foreignObject")
        .attr("class", "info_text")
        .attr("width", innerWidth * 0.7)
        .attr("height", innerHeight * 0.3)
        .attr("x", innerWidth * 0.05)
        .attr("y", innerHeight * 0.1)
        .append("xhtml:body")
        .attr("class", "text_itself")
        .style("color", "black")
        .style("font", innerWidth * 0.03 + "px 'Arial'")
        .html("Karpuz kavun örneğini tamamladınız. <br><br>" +
            "Son zamanların popüler dizisi Game of Thrones'un kullanıldığı bir sonraki örneğe geçmek için butona tıklayınız.");
function calculateXForText(d, i){
    return innerWidth * (i + 1) * 0.07 - innerWidth * 0.026;
}

function paintRectangles(){
    rectangleData.forEach(function (d, index) {
        if(+radius_label[index] >= theValue){
            d.color = "rgb(11, 229, 15)"
        } else {
            d.color = "rgb(228, 239, 14)"
        }
    });
}
function update(theValue){
    paintRectangles();
    s2svg.selectAll("rect.palette")
                            .data(rectangleData)
                            .transition()
                            .attr('fill', function (d) {
                                return d.color;
                            })
                            .duration(1100)
                            .ease(d3.easeBounce)
}
function calculateAccuracy(){
    let checkImgsData = [];
    let valid = 0;
    let invalid = 0;
    rectangleData.forEach(function(d, i){
        radiusDict[d.label].forEach(function(fruit, j){
            console.log(fruit, d.color);
            var resultImg = "success.png";
            if(d.color === "rgb(228, 239, 14)" && fruit === "Karpuz"){
                invalid++;
                resultImg = "error.png";
            }else if (d.color === "rgb(228, 239, 14)" && fruit === "Kavun"){
                valid++;
                resultImg = "success.png";
            }else if (d.color === "rgb(11, 229, 15)" && fruit === "Karpuz"){
                valid++;
                resultImg = "success.png"
            }else if (d.color === "rgb(11, 229, 15)" && fruit === "Kavun"){
                invalid++;
                resultImg = "error.png";
            }
            checkImgsData.push({'x': innerWidth * (i + 1) * 0.07 - innerWidth * 0.05,'y': innerHeight * 0.086 * j + innerHeight * 0.1, 'resultImg': resultImg})
        });
    });
    const accuracy = valid / (valid + invalid) * 100;
    return [checkImgsData, accuracy];
}

function calculateTest(){
    isDatasetTraining = false;
    manipulateRectangleData(test_data);
    paintRectangles();
    calculateFruitPlaces();
    d3.select("text.button_text").text("Yeni Model Kur")
    d3.select("text.tezgah_name").text("Ahmet'in Tezgahı")

    //DANGEROUS HERE ANY OTHER g would be affected by that
    d3.select('.sliderAll').style('opacity','0');

    s2svg.selectAll("rect.palette")
                            .data(rectangleData)
                            .attr("height", function (d, i) { return paletteHeight * radiusDict[Object.keys(radiusDict)[i]].length + 80})
                            .attr('fill', function(d){return d.color})
                            .exit()
                                .remove();
    s2svg.selectAll("text.label")
        .data(rectangleData)
        .text(function(d){return d.text + "cm"})
        .attr('x', calculateXForText).exit().remove();



    const accuracyResults = calculateAccuracy();
    const checkImgsData = accuracyResults[0];
    const accuracy = accuracyResults[1].toFixed(0);

    s2svg.selectAll("image.tick").style('display', "block")
                            .data(checkImgsData)
                            .attr("xlink:href", function (d) {
                                return "../static/icons/" + d.resultImg;
                            })
                            .raise()
                            .enter()
                                .append("svg:image")
                                .classed('tick', true)
                                .transition()
                                .attr('x', function(d){
                                    return d.x;
                                })
                                .attr('y', function(d){
                                    return d.y;
                                })
                                .attr('width', rectWidth / 2)
                                .attr('height', rectHeight / 2)
                                .attr("xlink:href", function (d) {
                                    return "../static/icons/" + d.resultImg;
                                });

    s2svg.selectAll("image.fruit").data(fruitPlaces)
                            .attr('x', function(d){
                                return d.x;
                            })
                            .attr('y', function(d){
                                return d.y;
                            })
                            .attr('width', rectWidth)
                            .attr('height', rectHeight)
                            .attr("xlink:href", function (d) {
                                return "../static/icons/" + d.fruit_img;
                            }).exit().remove();

    s2svg.selectAll("text.accuracy").style('display',"block")
        .data([accuracy])
        .text("Başarı oranı: %" + 0)
        .enter()
        .append("text")
        .classed("accuracy", true)
        .text("Başarı oranı: %" + 0)
        .transition()
        .ease(d3.easeCircle)
        .duration(200)
        .attr("x", innerWidth * 0.7)
        .attr("y", innerHeight / 2);

    s2svg.selectAll("text.accuracy")
        .data([accuracy])
        .style("font-size", innerWidth * 0.025 + "px")
        .transition()
        .duration(3000)
                .tween("text", function(d) {
                    var self = this;
                    var i = d3.interpolate(this.textContent, d),
                        prec = (d + "").split("."),
                        round = (prec.length > 1) ? Math.pow(10, prec[1].length) : 1;

                    return function(t) {
                        self.textContent = "Başarı oranı: %" + Math.round(i(t) * round) / round;
                    };
                });
}

function againTrain(){
    isDatasetTraining = true;
    manipulateRectangleData(train_data);
    paintRectangles();
    calculateFruitPlaces();

    console.log(radiusDict);
    console.log(rectangleData);

    d3.selectAll('text.button_text').text("Modeli Test Et");
    d3.selectAll('text.tezgah_name').text("Mustafa'nın Tezgahı");
    s2svg.selectAll("image.tick").style('display','none');
    s2svg.select(".sliderAll").style("opacity", '1');
    s2svg.selectAll('text.accuracy').style('display', 'none');
    s2svg.selectAll("rect.palette")
                            .data(rectangleData)
                            .enter()
                                .append("rect")
                                .attr('x', function(d) {return d.x})
                                .attr('y', function(d) {return d.y})
                                .attr("class", "palette")
                                .attr('width', rectWidth)
                                .attr("rx", 15)
                                .attr('height', paletteHeight)
                                .attr('fill', function(d){return d.color});
    //Apply to both new-comers and old ones
    s2svg.selectAll("rect.palette").data(rectangleData)
        .attr("height", function (d, i) { return paletteHeight * radiusDict[Object.keys(radiusDict)[i]].length + 80})
    //    .lower();
    s2svg.selectAll("text.label")
                .data(rectangleData)
                .text(function(d){return d.text + "cm"})
                .enter()
                    .append('text')
                    .classed('label', true)
                    .text(function(d){return d.text + "cm"})
                    .attr("alignment-baseline", "middle")
                    .attr("text-anchor", "middle")
                    .attr('x', calculateXForText)
                    .attr('y', innerHeight * 0.06)
                    .attr("fill", "black")
                    .style("font-size", innerWidth / 62 + "px");
    s2svg.selectAll("image.fruit")
                .data(fruitPlaces)
                .attr('x', function(d){
                    return d.x;
                })
                .attr('y', function(d){
                    return d.y;
                })
                .attr("xlink:href", function (d) {
                    return "../static/icons/" + d.fruit_img;
                })
                .raise()
                .enter()
                    .append("svg:image")
                    .classed("fruit", true)
                    .attr('x', function(d){
                        return d.x;
                    })
                    .attr('y', function(d){
                        return d.y;
                    })
                        .attr("rx", 15)
                    .attr('width', rectWidth)
                    .attr('height', rectHeight)
                    .attr("xlink:href", function (d) {
                        return "../static/icons/" + d.fruit_img;
                    });
}
//scroll
d3.select("#scroll2").style("top", 2 * innerHeight * 0.95+ "px");
d3.select("#scroll1").style("top", innerHeight * 0.9 + "px");
d3.select("#scroll1").style("left", innerWidth * 0.68 + "px");
d3.select("#scroll2").style("left", innerWidth * 0.68 + "px");