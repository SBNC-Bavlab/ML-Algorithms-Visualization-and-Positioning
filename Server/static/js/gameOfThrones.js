

    const s1ScaledRadius = 0.7 * 370;
    const s2ScaledRadius = 0.3 * 370;

    const s2Gauge0Width = innerWidth * 0.75;
    const s2Gauge0Height = innerHeight * 0.05 + 10;
    const s2Gauge1Width = innerWidth * 0.75;
    const s2Gauge1Height = innerHeight * 0.6 + 10;

    const buttonWidth = 180;
    const buttonHeight = 50;

    const s1Gauge0Width = innerWidth / 2 - s1ScaledRadius;
    const s1Gauge0Height = innerHeight / 2 - s1ScaledRadius + 50;
    var circleX = 970;
    const questions = [{name: "Zengin mi?", attribute: "Evet", type: 1},
        {name: "Beyaz saçlı mı?", attribute: "Beyaz", type: 4},
        {name: "Ejderhası var mı?", attribute: "Var", type: 2},
        {name: "Tahtı istiyor mu?", attribute: "Evet", type: 3}];

    const got = [
              ["Trion Lannister", "Hayır", "Yok", "Hayır", "Sarı", "Lannıster"],
              ["Daenerys Targaryen", "Evet", "Var", "Evet", "Beyaz", "Targaryen"],
              ["John Snow", "Hayır", "Yok", "Hayır", "Siyah", "Stark"],
              ["Cercei Lannister", "Evet", "Yok", "Evet", "Sarı", "Lannıster"],
              ["Night King", "Hayır", "Var", "Hayır", "Beyaz", "Whıte Walker"],
              ["Jamie Lannister", "Evet", "Yok", "Hayır",  "Sarı", "Lannıster"],
              ["Arya Stark", "Hayır", "Yok", "Hayır", "Siyah", "Stark"],
              ["Tywin Lannister", "Evet", "Yok", "Evet",  "Sarı", "Lannıster"],
              ["Sansa Stark", "Hayır", "Yok", "Hayır", "Kızıl", "Stark"],
              ["Lieutenant W. Walker", "Hayır", "Var", "Hayır", "Beyaz", "Whıte Walker"],
              ["Viserys Targaryen", "Hayır", "Yok",  "Evet", "Beyaz", "Targaryen"],
              ["Wights", "Hayır", "Yok", "Hayır", "Beyaz", "Whıte Walker"],
              ["Eddard Stark", "Hayır", "Yok", "Hayır", "Siyah", "Stark"],
            ];
    const gotRowStroke = ['white',
              'white',
              'white',
              'white',
              'white',
              'white',
              'white',
              'white',
              'white',
              'white',
              'white',
              'white',
              'white'];
    /*const got = [
              ["Trion", "Hayır", "Yok", "Hayır", "Sarı", "Lannister"],
              ["Daenerys", "Evet", "Var", "Evet", "Beyaz", "Targaryen"],
              ["John Snow", "Hayır", "Yok", "Hayır", "Siyah", "Stark"],
              ["Cercei", "Evet", "Yok", "Evet", "Sarı", "Lannister"],
              ["Night King", "Hayır", "Var", "Hayır", "Beyaz", "White Walker"],
              ["Jamie", "Evet", "Yok", "Hayır",  "Sarı", "Lannister"],
              ["Arya", "Hayır", "Yok", "Hayır", "Siyah", "Stark"],
              ["Tywin", "Evet", "Yok", "Evet",  "Sarı", "Lannister"],
              ["Sansa", "Hayır", "Yok", "Hayır", "Kızıl", "Stark"],
              ["Lieutenant", "Hayır", "Var", "Hayır", "Beyaz", "White Walker"],
              ["Viserys", "Hayır", "Yok",  "Evet", "Beyaz", "Targaryen"],
              ["Wights", "Hayır", "Yok", "Hayır", "Beyaz", "White Walker"],
              ["Eddard", "Hayır", "Yok", "Hayır", "Siyah", "Stark"],
            ];*/
    const rowNames = ['İsim', 'Zengin mi?', 'Ejderha?', 'Tahtı istiyor?', 'Saç rengi', 'Hanesi'];
    got.sort(function(a, b){
        const str1 = a[a.length - 1];
        const str2 = b[b.length - 1];
        return str1 < str2 ? -1 : str1 > str2;
    });
    let isLoadingToBigGauge = false;
    const familyToColorIndex = {'Lannıster': 0,'Targaryen': 1,'Stark': 2,'Whıte Walker': 3};
    const gotPosArray = [];
    let colorScheme = d3.scaleOrdinal()
                    .range(d3.schemeCategory10);
    let color = [];
    for(let i = 0; i < 10; i++){
        color.push(colorScheme(i))
    }

    for(let i = 0; i < got.length; i++){
        for(let j = 0; j < got[0].length; j++) {
            if (j === 1) {
                gotPosArray.push({'x': 200 * j + 300, 'y': 53 * i + 75, 'text': got[i][j]})
            } else if(j > 1){
                gotPosArray.push({'x': 80 * j + 420, 'y': 53 * i + 75, 'text': got[i][j]})
            }else {
                gotPosArray.push({'x': 100 * j + 330, 'y': 53 * i + 75, 'text': got[i][j]})
            }
        }
    }
    //Below is for section 1

    const infoTextPost = [{x: 30, y: 200, text: "Her bir daire Game of Thrones dizisindeki bir karakteri, her bir renk ise üyesi oldukları haneyi temsil etmektedir"},
                        {x: innerWidth * 0.67, y: 200, text: "Renkleri bir suda karıştırdığımızda suyun koyuluk oranı elimizdeki verilerin entropi (karmaşıklık) miktarını göstermektedir"}];

    const generalEntropy = calculateEntropy(got);
    let averageEntropy = 0
    const svgSection0 = d3.select("#section0")
                            .attr("width", innerWidth)
                            .attr("height", innerHeight);


    const svgSection1 = d3.select("#section1")
                            .attr("width", innerWidth)
                            .attr("height", innerHeight);
    /*svgSection1.append("svg:image")
        .attr("width", innerWidth)
        .attr("height", innerHeight)
        .attr("xlink:href", "../icons/eagle.jpg")
        .lower().lower();*/

    svgSection1.selectAll("text.infoText")
        .data(infoTextPost)
        .enter()
        .append("foreignObject")
        .attr("width", 480)
        .attr("height", 500)
        .attr("x", (d)=>{
           return d.x;
        })
        .attr("y", (d)=>{
            return d.y;
        })
        .append("xhtml:body")
        .style("font", "30px 'Arial'")
        .html((d)=>{
            return d.text;
        });

    svgSection1.call(d3.liquidfillgauge, 50, {
        circleThickness: 0.15,
        circleColor: "#1CA3EC",
        textColor: "#1CA3EC",
        waveTextColor: "#FFFFAA",
        waveColor: "1CA3EC",
        backgroundColor: "white",
        textVertPosition: 0.8,
        waveAnimateTime: 1000,
        waveHeight: 0.05,
        waveAnimate: true,
        waveRise: false,
        waveOffset: 0.25,
        textSize: 0.75,
        waveCount: 3
    }, s1Gauge0Width, s1Gauge0Height, 0, 0.7);
    svgSection1.on("opacityChanged0")("hsla(193, 100%, 56%, 1)");
    const circleTextGroup = svgSection1.selectAll("g.s1circle")
                .data(got)
                .enter()
                    .append("g")
                    .attr("class", "s1circle")
                    .lower();
    circleTextGroup.append("circle")
                            .attr("cx", (d , i) => {
                                return 90 * i + 240;
                            })
                            .attr("cy", 50)
                            .attr("r", 25)
                            .attr("fill", (d, i)=>{
                                return color[familyToColorIndex[d[d.length - 1]]];
                            });
    circleTextGroup.append("svg:image")
                    .attr("x", (d , i) => {
                        return 90 * i + 240 - 25;
                    })
                    .attr("y", 50 - 25)
                    .attr("width", 50)
                    .attr("height", 50)
        .attr("xlink:href", "../static/icons/john.jpg");

    circleTextGroup.append("text")
                    .attr("x", (d , i) => {
                        return 90 * i + 240;
                    })
                    .attr("y", 88)
                    .attr("fill", "white")
                    .text((d)=>{
                        let possibleName = d[0].split(" ")[0];
                        if(possibleName === "Night"){
                            possibleName = "Night King";
                        } else if (possibleName === "John"){
                            possibleName = "John Snow";
                        }
                        return possibleName
                    });
    const resetButtonGroup = svgSection1.append("g");
    const resetButtonPos = [innerWidth * 0.7, innerHeight * 0.7];
    resetButtonGroup
        .append("rect")
        .attr("x", resetButtonPos[0])
        .attr("y", resetButtonPos[1])
        .attr("fill", "orange")
        .attr("rx", "15")
        .attr("width", buttonWidth)
        .attr("height", buttonHeight);
    resetButtonGroup
        .append("text")
        .attr("x", resetButtonPos[0] + buttonWidth / 2)
        .attr("y", resetButtonPos[1] + buttonHeight / 2)
        .attr("fill", "white")
        .attr("font-size", "15px")
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .text("Animasyonu Tekrarla");
    resetButtonGroup
        .attr("cursor", "pointer")
        .attr("opacity", "0")
        .on("click", () => {
            if(!isLoadingToBigGauge) {
                circleTextGroup.transition()
                    .attr("transform", "translate(0,0)");
                resetButtonGroup.attr("opacity", "0");
                svgSection1.on("valueChanged0")("0.00");
                svgSection1.on("opacityChanged0")("hsla(193, 100%, 56%, 1)");
                animateFill();
            }
        });
    let firstAnimationWithScrolling = true;
    startAnimation();//Initial invocation is made since user may spawn into this page
    function startAnimation() {
        const scrollPos = document.documentElement.scrollTop;
        if(!isLoadingToBigGauge && firstAnimationWithScrolling && scrollPos < innerHeight * 1.1 && scrollPos > innerHeight * 0.9) {
            firstAnimationWithScrolling = false;
            animateFill();
        }
    }
    function animateFill(){
        isLoadingToBigGauge = true;
        circleTextGroup.transition()
            .attr("transform", (d, i) => {
                const targetX = s1Gauge0Width + s1ScaledRadius
                const targetY = s1Gauge0Height + s1ScaledRadius
                const currentX = 90 * i + 240;
                const currentY = 50;
                const dx = targetX - currentX;
                const dy = targetY - currentY;
                return "translate( " + dx + "," + dy + ")";
            })
            .on('start', function (d, i) {
                setTimeout(() => {
                    const tempGot = got.slice(0, i + 1);
                    const entropySoFar = calculateEntropy(tempGot)
                    svgSection1.on("valueChanged0")(entropySoFar.toFixed(2));
                    svgSection1.on("opacityChanged0")("hsla(193, 100%, " + (56 - 15 * entropySoFar) + "%, 1)");
                    if( i === got.length - 1){
                        //it means all finished
                        isLoadingToBigGauge = false;
                        resetButtonGroup.attr("opacity", "1");
                    }
                }, 500);
            })
            .delay((d, i) => {
                return 1000 * i + 500
            })
            .duration(1000);
    }
    //Below is for section 2
    const scoreTextPos = [{x: innerWidth * 0.72, y: innerHeight / 2, text: "Ortalama Entropi: -"}];
    const buttonsPos = [{x: 60, y: 100, text: "Zengin mi?", click: () => {askQuestion(0)}},
                        {x: 60, y: 170, text: "Ejderhasi var mi?", click: () => {askQuestion(2)}},
                        {x: 60, y: 240, text: "Tahti istiyor mu?", click: () => {askQuestion(3)}},
                        {x: 60, y: 500, text: "Kendi sorunu oluştur", click: () => {createQuestion()}},
                        {x: 60, y: 570, text: "Reset", click: () => {reset()}}];

    const svg = d3.select("#section2")
                    .attr("width", innerWidth)
                    .attr("height", innerHeight);

    /*
    svg.selectAll("rect.yes_no")
        .data([{x: 250, y: 495, text: "Evet", click: () => {reset()}},
            {x: 250, y: 535, text: "Hayır", click: () => {reset()}}])
        .enter()
            .append("rect")
            .attr("class", "yes_no")
            .attr("x", (d) => {return d.x})
            .attr("y", (d) => {return d.y})
            .attr("width", buttonWidth / 2)
            .attr("height", buttonHeight / 2)
            .attr("fill", "white");
    */
    svg.selectAll("text.score_text")
        .data(scoreTextPos)
        .enter()
        .append("text")
        .attr("class", "score_text")
        .attr("font-size", "30px")
        .attr("x", (d)=>{return d.x})
        .attr("y", (d)=>{return d.y})
        .text((d)=>{return d.text});
    svg.append("rect")
        .attr("class", "button_wrapper")
        .attr('x', 50)
        .attr("y", 85)
        .attr("rx", 5)
        .attr("fill", "yellowgreen")
        .attr("width", buttonWidth + 22)
        .attr("height", buttonHeight * 3 + 70);
    svg.append("rect")
        .attr("class", "button_wrapper")
        .attr('x', 50)
        .attr("y", 490)
        .attr("rx", 5)
        .attr("fill", "yellowgreen")
        .attr("width", buttonWidth + 22)
        .attr("height", buttonHeight * 2 + 45);
    svg.append("text")
        .attr("class", "button_header")
        .attr('x', 95)
        .attr("y", 80)
        .attr("font-size", 30)
        .attr("fill", "white")
        .text("Sorular");
    svg.append("text")
        .attr("class", "button_header")
        .attr('x', 95)
        .attr("y", 480)
        .attr("fill", "white")
        .attr("font-size", 30)
        .text("Araçlar");
    const rectWidth = 600;
    const rectHeight = 40;
    const rectColor = "rgb(245, 245, 220)";
    svg.selectAll('text.header').data(rowNames)
                        .enter()
                        .append('text')
                        .attr("class", "header")
                        .attr('x', function(d, i){
                            if (i === 0){
                                return 100 * i + 370;
                            } else if (i === 1) {
                                return 200 * i + 285;
                            } else if(i === 3){
                                return 80 * i + 408;
                            } else if(i === 5){
                                return 80 * i + 415;
                            } else if(i > 1){
                                return 80 * i + 410;
                            }
                        })
                        .attr('y', function(d, i){
                            return 25;
                        })
                        .text(function (d) {
                            return d;
                        })
                        .style("font-size", "14px")
        .attr("fill", "#e6f598");
    svg.selectAll("rect.button_rect")
        .data(buttonsPos)
        .enter()
        .append("rect")
        .attr('x', (d) => {return d.x})
        .attr('y', (d) => {return d.y})
        .attr('width', buttonWidth)
        .attr('height', buttonHeight)
        .attr("fill", "green")
        .attr('class', "button_rect")
        .attr('rx', 15)
        .attr('ry', 15)
        .on('click', (d)=>{
            d.click();
        });

    svg.append('rect').lower()
        .transition()
        .ease(d3.easeLinear)
        .duration(1000)
        .attr('fill', '#d7191c')
        .attr('x', 320)
        .attr('y', 0)
        .attr('rx', 15)
        .attr('ry', 15)
        .attr('width', rectWidth)
        .attr('height', rectHeight);
    svg.selectAll("text.button_text")
        .data(buttonsPos)
        .enter()
        .append("text")
        .attr('x', (d) => {return d.x + buttonWidth / 2})
        .attr('y', (d) => {return d.y + buttonHeight / 2})
        .attr("fill", "white")
        .attr("alignment-baseline", "middle")
        .attr("text-anchor", "middle")
        .attr('class', "button_text")
        .text((d) => {return d.text})
        .on('click', (d)=>{
            d.click();
        });

    svg.selectAll("rect.item").data(got)
        .enter()
        .append("rect")
        .attr("class", "item")
        .transition()
        .ease(d3.easeLinear)
        .duration(1000)
        .attr('border', 1)
        .attr('rx', 15)
        .attr('ry', 15)
        .attr('fill', "#fc8d59")
        .attr('x', 320)
        .attr('y', function(d, i){
            return 53 * i + 50;
        })
        .attr('width', rectWidth)
        .attr('height', rectHeight);
    svg.selectAll("text.table").data(gotPosArray)
                        .enter()
                        .append("text")
                        .transition()
                        .attr('class', 'table')
                        .ease(d3.easeLinear)
                        .duration(1000)
                        .style("font-size", "12px")
                        .attr("fill", "black")
                        .attr('x', function(d){
                            return d.x;
                        })
                        .attr('y', function(d){
                           return d.y;
                        }).text(function(d){
                            return d.text.toLocaleUpperCase("tr-TR");
                        });
    svg.selectAll("circle.house_color")
        .data(got)
        .enter()
        .append('circle')
        .attr("class", "house_color")
        .transition()
        .duration(1000)
        .ease(d3.easeLinear)
        .attr('cx', circleX)
        .attr('cy', function(d, i){
            return 53 * i + 70;
        })
        .attr('r', 20)
        .attr('stroke', 'black')
        .attr('fill', function(d,i){

           return color[familyToColorIndex[d[d.length - 1]]];
        });

    svg.call(d3.liquidfillgauge, 50, {
      circleThickness: 0.15,
      circleColor: "hsla(193, 100%, 56%, 1)",
      textColor: "hsla(193, 100%, 56%, 1)",
      waveTextColor: "#FFFFAA",
      waveColor: "hsla(193, 100%, 56%, 1)",
        backgroundColor: "white",
      textVertPosition: 0.8,
      waveAnimateTime: 1000,
      waveHeight: 0.05,
      waveAnimate: true,
      waveRise: false,
      waveOffset: 0.25,
      textSize: 0.75,
      waveCount: 3
    }, s2Gauge0Width, s2Gauge0Height + 25, 0, 0.3);

    svg.call(d3.liquidfillgauge, 50, {
      circleThickness: 0.15,
      circleColor: "hsla(193, 100%, 56%, 1)",
      textColor: "hsla(193, 100%, 56%, 1)",
      waveTextColor: "#FFFFAA",
      waveColor: "hsla(193, 100%, 56%, 1)",
        backgroundColor: "white",
      textVertPosition: 0.8,
      waveAnimateTime: 1000,
      waveHeight: 0.05,
      waveAnimate: true,
      waveRise: false,
      waveOffset: 0.25,
      textSize: 0.75,
      waveCount: 3
    }, s2Gauge1Width, s2Gauge1Height + 25, 1, 0.3);
    //circleThickness : 0.15, circleColor : "#808015", textColor : "#555500", waveTextColor : "#FFFFAA", waveColor : "#AAAA39", textVertPosition : 0.8, waveAnimateTime : 1000, waveHeight : 0.05, waveAnimate : true, waveRise : false, waveHeightScaling : false, waveOffset : 0.25, textSize : 0.75, waveCount : 3,
    let createQuestionIndex = 0;
    function changeColorRect(index) {
        svg.selectAll('rect.item')
            .data(got)
            .transition()
            .attr('fill', function(d, i){
                if(i === index){
                    return 'lightblue'
                }
                return rectColor
            })
            .attr("stroke", (d, i) => {
                return gotRowStroke[i];
            })
            .attr("stroke-width", "1")
    }
    function createQuestion(){
        reset()
        changeColorRect(createQuestionIndex);
    }
    const dxs = [];
    const dys = [];
    const left = [];
    const right = [];
    function seperate(isYes, index){
        gotRowStroke[index] = (isYes) ? "green" : "red";
        svg.selectAll("circle.house_color")
        .filter(function(d,i) {return i === index;})
        .transition()
        .duration(600)
        .attr("transform", function(d, i){
            let targetY;
            let targetX;
            if (isYes) {
                targetX = s2Gauge0Width + s2ScaledRadius;
                targetY = (s2Gauge0Height) + s2ScaledRadius;
            } else {
                targetX = s2Gauge1Width + s2ScaledRadius;
                targetY = (s2Gauge1Height) + s2ScaledRadius;
            }
            const currentY = 53 * index + 40;
            const currentX = circleX;
            const dx = targetX - currentX;
            const dy = targetY - currentY;
            dxs.push(dx);
            dys.push(dy);
            return "translate(" + dx + "," + dy + ")"
        })
        .on('start', function(d){
            if (isYes) {
                left.push(d);
            } else {
                right.push(d);
            }
            console.log(left, right)

            const leftEntropy = calculateEntropy(left);
            const rightEntropy = calculateEntropy(right);
            svg.on("valueChanged0")(leftEntropy.toFixed(2));
            svg.on("valueChanged1")(rightEntropy.toFixed(2));

            svg.on("opacityChanged0")("hsla(193, 100%, " + (56 - 15 * leftEntropy) + "%, 1)");
            svg.on("opacityChanged1")("hsla(193, 100%, " + (56 - 15 * rightEntropy) + "%, 1)");

            let result = "";
            if (isYes) {
                const dx2 = 15 * (a2++ + 1) + 110;
                const dy2 = 0;
                result = "translate(" + (dxs[index] + dx2) + "," + (dys[index] + dy2) + ")"
            } else {
                const dx2 = 15 * (b2++ + 1) + 110;
                const dy2 = 0;
                result = "translate(" + (dxs[index] + dx2) + "," + (dys[index] + dy2) + ")"
            }

            if(createQuestionIndex === got.length - 1)
                calculateScore();
            createQuestionIndex++;
            changeColorRect(createQuestionIndex);
            d3.select(this).transition().duration(500).delay(500).attr('transform', result).attr('r', "5")
        })
        .delay(function(d,i){return 500 * i});
    }
    svg.append('text')
        .attr('x', (s2Gauge0Width + s2ScaledRadius) *0.97)
        .attr('y', s2Gauge0Height * 1.2)
        .style("font-size", "40px")
        .on("click", function(d) {
            seperate(true, createQuestionIndex);
        })
        .attr("fill", 'rgb(242, 247, 255)')
        .attr("stroke", 'black')
        .attr("cursor", 'pointer')
        .text("Evet");
    svg.append('text')
        .attr('x', (s2Gauge1Width + s2ScaledRadius) *0.956)
        .attr('y', s2Gauge1Height * 1.03)
        .style("font-size", "40px")
        .attr("fill", 'rgb(242, 247, 255)')
        .attr("stroke", 'black')
        .attr("cursor", 'pointer')
        .on("click", function(d) {
            seperate(false, createQuestionIndex);
        })
        .text("Hayır");

    let a = 0;
    let b = 0;
    let a2 = 0;
    let b2 = 0;
    function calculateEntropy(data){
      const totalNumber = data.length;
      const labelDict = {};
      for (let i in data){
        //get the last column which is the label
        const entry = data[i];
        const decision = entry[entry.length - 1];
        if( decision in labelDict){
            labelDict[decision]++;
        } else {
            labelDict[decision] = 1.0
        }
      }
      let entropy = 0.0;
      for(let key in labelDict){
          let prob = labelDict[key] / totalNumber;
          entropy -= prob * Math.log2(prob);
      }
      return entropy
    }
    function askQuestion(questionI){
        reset();
        svg.selectAll("circle.house_color").transition()
                            .duration(600)
                            .attr("transform", function(d,i){
                                const isLeft = d[questions[questionI].type] === questions[questionI].attribute;
                                var targetY;
                                var targetX;
                                if(isLeft) {
                                    targetX = s2Gauge0Width + s2ScaledRadius;
                                    targetY = s2Gauge0Height + s2ScaledRadius;
                                } else {
                                    targetX = s2Gauge1Width + s2ScaledRadius;
                                    targetY = s2Gauge1Height + s2ScaledRadius;
                                }
                                const currentY =  53 * i + 40;
                                const currentX = circleX;
                                const dx = targetX - currentX;
                                const dy = targetY - currentY;

                                dxs.push(dx);
                                dys.push(dy);
                                return "translate(" + dx + "," + dy +  ")"
                            })
                            .on('start', function(d, i){
                                const isLeft = d[questions[questionI].type] === questions[questionI].attribute;

                                if(isLeft) {
                                    left.push(d);
                                } else {
                                    right.push(d);
                                }

                                gotRowStroke[createQuestionIndex] = (isLeft) ? "green" : "red";
                                const leftEntropy = calculateEntropy(left);
                                const rightEntropy = calculateEntropy(right);
                                svg.on("valueChanged0")(leftEntropy.toFixed(2));
                                svg.on("valueChanged1")(rightEntropy.toFixed(2));
                                svg.on("opacityChanged0")("hsla(193, 100%, " + (56 - 15 * leftEntropy) + "%, 1)");
                                svg.on("opacityChanged1")("hsla(193, 100%, " + (56 - 15 * rightEntropy) + "%, 1)");

                                var result = "";
                                if(isLeft) {
                                    var dx2 = 15 * (a2++ + 1) + 110;
                                    var dy2 = 0;
                                    result = "translate(" + (dxs[i] + dx2) + "," + (dys[i] + dy2)+ ")"
                                } else {
                                    var dx2 = 15 * (b2++ + 1) + 110;
                                    var dy2 = 0;
                                    result = "translate(" + (dxs[i] + dx2) + "," + (dys[i] + dy2)+ ")"
                                }
                                if(createQuestionIndex === got.length - 1)
                                    calculateScore();
                                createQuestionIndex++;
                                changeColorRect(createQuestionIndex)
                                d3.select(this).transition().duration(500).delay(500).attr('transform', result).attr('r', "5")
                            })
                            .delay(function(d,i){return 500 * i});
    }
    function reset(){
        svg.selectAll("circle.house_color").transition()
            .duration(600)
            .attr('transform', "translate(0,0)").attr('r', "20");
        svg.on("opacityChanged0")("hsla(193, 100%, 56%, 1)");
        svg.on("opacityChanged1")("hsla(193, 100%, 56%, 1)");
        svg.on("valueChanged0")("0.00");
        svg.on("valueChanged1")("0.00");
        a = 0;
        b = 0;
        svg.selectAll("rect.item")
            .transition()
            .attr('fill', "#fc8d59")
            .attr('stroke', "white");
        for(let i = 0; i < gotRowStroke.length; i++){
            gotRowStroke[i] = 'white';
        }
        scoreTextPos[0].text = "Ortalama Entropi: -";
        svg.selectAll("text.score_text")
            .data(scoreTextPos)
            .text((d)=>{return d.text})
        createQuestionIndex = 0;
        a2 = 0;
        b2 = 0;
        dxs.length = 0;
        dys.length = 0;
        left.length = 0;
        right.length = 0;
    }
    function calculateScore(){
        if (createQuestionIndex === got.length - 1) {
            const featuresMatrix = [];
            for(let i = 0; i < left.length; i++){
                const item = left[i];
                let attributeArr = item;
                featuresMatrix.push([]);
                //First and last col not included
                for(let j = 0; j < attributeArr.length; j++){
                    featuresMatrix[i].push(attributeArr[j])
                }
            }
            console.log('features', featuresMatrix)
            let validSplit = false;
            let col;
            //col started from 1 so that name is not taken into account
            for(col = 1; featuresMatrix.length !== 0 && col < featuresMatrix[0].length - 1 && !validSplit; col++){
                let previous = featuresMatrix[0][col];// first element is previous
                let differentFound = false;
                for(let row = 0; !differentFound && row < featuresMatrix.length; row++){
                    if(featuresMatrix[row][col] !== previous){
                        differentFound = true;
                    }
                }
                if(!differentFound){
                    //Let's check if the same column is valid in the right list
                    if(right.length > 0) {
                        let sameFound = false;
                        for (let i = 0; i < right.length; i++) {
                            const rightItem = right[i];
                            const current = rightItem[col];
                            if(current === previous){
                                sameFound = true;
                            }
                        }
                        validSplit = !sameFound
                    } else {
                        validSplit = true
                    }
                }
            }
            if(validSplit) {
                const totalNumber = got.length;
                const leftEntropy = calculateEntropy(left);
                const leftSize = left.length;
                //right
                const rightEntropy = calculateEntropy(right);
                const rightSize = right.length;
                averageEntropy = (leftSize / totalNumber) * leftEntropy + (rightSize / totalNumber) * rightEntropy;
                console.log(leftSize, rightSize, totalNumber)
                const gain = generalEntropy - averageEntropy;
                scoreTextPos[0].text = "Ortalama Entropi: " + averageEntropy.toFixed(2);
                svg.selectAll("text.score_text")
                    .data(scoreTextPos)
                    .text((d)=>{return d.text})
                    const text = "Sistemin tüm entropisi " + generalEntropy.toFixed(2) + " idi.<br><br> Sorduğunuz soru sonunda 'Evet' ve 'Hayir' havuzlarinin agirlikli" +
                                " ortalama entropisi " + averageEntropy.toFixed(2) + " oldu.<br><br> Sorunun karmaşıklığı azaltma miktarı yani skoru bu ikisinin farkıdır:   " + (generalEntropy - averageEntropy).toFixed(2);
                svgSection3.select(".text_itself")
                            .html(text)
                svgSection3.select(".equals_sign")
                    .text("= " + gain.toFixed(2))
                svgSection3.on('valueChanged1')(leftEntropy.toFixed(2));
                svgSection3.on('opacityChanged1')("hsla(193, 100%, " + (56 - 15 * leftEntropy) + "%, 1)");

                svgSection3.on('valueChanged2')(rightEntropy.toFixed(2));
                svgSection3.on('opacityChanged2')("hsla(193, 100%, " + (56 - 15 * rightEntropy) + "%, 1)");
            }  else {
                console.log("Verilerinizi herhangi bir soruya veya ortak özelliğe göre bölmediniz bu yüzden skor hesaplanamadı.");
                //$error.slideDown().delay(5000).slideUp();
            }
        } else {
            console.log("Bütün elemanlar paylaştırılmadan sorunun skoru hesaplanamaz");
            //$error.slideDown().delay(5000).slideUp();
        }
    }
    //Section 3
    const svgSection3 = d3.select("#section3")
                            .attr("width", innerWidth)
                            .attr("height", innerHeight);
    const text = "Sistemin tüm entropisi " + generalEntropy.toFixed(2) + " idi.<br><br> Sorduğunuz soru sonunda 'Evet' ve 'Hayir' havuzlarinin agirlikli" +
        " ortalama entropisi " + averageEntropy.toFixed(2) + " oldu.<br><br>Sorunun karmaşıklığı azaltma miktarı yani skoru bu ikisinin farkıdır: " + (generalEntropy - averageEntropy).toFixed(2);
    svgSection3.append("foreignObject")
        .attr("class", "info_text")
        .attr("width", innerWidth)
        .attr("height", 500)
        .attr("x", innerWidth * 0.05)
        .attr("y", innerHeight * 0.7)
        .append("xhtml:body")
        .attr("class", "text_itself")
        .style("color", "white")
        .style("font", "30px 'Arial'")
        .html(text);
    svgSection3.append("text")
        .attr("class","minus_sign")
        .attr("x", innerWidth * 0.335)
        .attr("y", innerHeight * 0.45)
        .attr("font-size", "200px")
        .attr("fill", "white")
        .text("-");
    svgSection3.append("text")
        .attr("class","paran_sign")
        .attr("font-size", "300px")
        .attr("text-anchor", "middle")
        .attr("transform", "translate(" + innerWidth * 0.43 + ", " + s2Gauge0Height + ") rotate(90)")
        .attr("fill", "white")
        .text("(");svgSection3.append("text")
        .attr("class","paran_sign")
        .attr("font-size", "300px")
        .attr("text-anchor", "middle")
        .attr("transform", "translate(" + innerWidth * 0.43 + ", " + innerHeight * 0.7 + ") rotate(90)")
        .attr("fill", "white")
        .text(")");
    svgSection3.append("text")
        .attr("class","equals_sign")
        .attr("x", innerWidth * 0.55)
        .attr("y", innerHeight * 0.47)
        .attr("font-size", "200px")
        .attr("fill", "white")
        .text("= ?");
    svgSection3.call(d3.liquidfillgauge, 50, {
      circleThickness: 0.15,
      circleColor: "hsla(193, 100%, 56%, 1)",
      textColor: "hsla(193, 100%, 56%, 1)",
      waveTextColor: "#FFFFAA",
      waveColor: "hsla(193, 100%, 56%, 1)",
        backgroundColor: "white",
      textVertPosition: 0.8,
      waveAnimateTime: 1000,
      waveHeight: 0.05,
      waveAnimate: true,
      waveRise: false,
      waveOffset: 0.25,
      textSize: 0.75,
      waveCount: 3
    }, innerWidth * 0.05, innerHeight * 0.12, 0, 0.48);

    svgSection3.on('valueChanged0')(generalEntropy.toFixed(2));
    svgSection3.on('opacityChanged0')("hsla(193, 100%, " + (56 - 15 * generalEntropy) + "%, 1)");

    svgSection3.call(d3.liquidfillgauge, 50, {
      circleThickness: 0.15,
      circleColor: "hsla(193, 100%, 56%, 1)",
      textColor: "hsla(193, 100%, 56%, 1)",
      waveTextColor: "#FFFFAA",
      waveColor: "hsla(193, 100%, 56%, 1)",
        backgroundColor: "white",
      textVertPosition: 0.8,
      waveAnimateTime: 1000,
      waveHeight: 0.05,
      waveAnimate: true,
      waveRise: false,
      waveOffset: 0.25,
      textSize: 0.75,
      waveCount: 3
    }, innerWidth * 0.437, innerHeight * 0.10, 1, 0.2);
    const leftEntropy = calculateEntropy(left);
    const rightEntropy = calculateEntropy(right);
    svgSection3.on('valueChanged1')(leftEntropy.toFixed(2));
    svgSection3.on('opacityChanged1')("hsla(193, 100%, " + (56 - 15 * leftEntropy) + "%, 1)");

    svgSection3.call(d3.liquidfillgauge, 50, {
      circleThickness: 0.15,
      circleColor: "hsla(193, 100%, 56%, 1)",
      textColor: "hsla(193, 100%, 56%, 1)",
      waveTextColor: "#FFFFAA",
      waveColor: "hsla(193, 100%, 56%, 1)",
        backgroundColor: "white",
      textVertPosition: 0.8,
      waveAnimateTime: 1000,
      waveHeight: 0.05,
      waveAnimate: true,
      waveRise: false,
      waveOffset: 0.25,
      textSize: 0.75,
      waveCount: 3
    }, innerWidth * 0.437, innerHeight * 0.48, 2, 0.2);
    svgSection3.on('valueChanged2')(rightEntropy.toFixed(2));
    svgSection3.on('opacityChanged2')("hsla(193, 100%, " + (56 - 15 * rightEntropy) + "%, 1)");


    const svgSection4 = d3.select("#section4")
                .attr("width", innerWidth)
                .attr("height", innerHeight);
    const next_button_group = svgSection4.append("g");
    next_button_group.append("rect")
        .attr("class", "next_button")
        .attr("x", 100)
        .attr("y", 400)
        .attr("fill", "white")
        .attr("width", buttonWidth)
        .attr("height", buttonHeight);
    next_button_group
        .append("text")
        .attr("class", "next_button_text")
        .attr("x", 100 + buttonWidth / 2)
        .attr("y", 400 + buttonHeight / 2)
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .attr("color", "black")
        .attr("font-size", "30")
        .text("İlerle");
    next_button_group
        .attr("cursor", "pointer")
    next_button_group.on('click', () => {
       location.href = "charts.html"
    });
    svgSection4.append("foreignObject")
            .attr("class", "info_text")
            .attr("width", innerWidth * 0.7)
            .attr("height", 300)
            .attr("x", innerWidth * 0.05)
            .attr("y", innerHeight * 0.1)
            .append("xhtml:body")
            .attr("class", "text_itself")
            .style("color", "white")
            .style("font", "30px 'Arial'")
            .html("Game of Thrones örneğini tamamladınız. <br><br>" +
                "Bir kişinin yaşı, göz bozukluğu, göz yaşı üretimi ve astigmatizm özellikleri ile o kişinin " +
                "lens takmaya uygunluğu arasındaki ilişkiyi gösteren bir veri seti ile tanışacaksınız.");

    // set scroll items

    d3.select("#scroll2").style("top", 2 * innerHeight * 0.95+ "px");
    d3.select("#scroll1").style("top", innerHeight * 0.9 + "px");
    d3.select("#scroll1").style("left", innerWidth * 0.68 + "px");
    d3.select("#scroll2").style("left", innerWidth * 0.68 + "px");

