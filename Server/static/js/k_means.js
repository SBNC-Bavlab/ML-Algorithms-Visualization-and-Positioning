const svgSection1 = d3.select("#section0")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .style("background-color", "orange");
svgSection1
    .append("foreignObject")
    .attr("width", innerWidth / 1.5)
    .attr("height", 500)
    .attr("x", 100)
    .attr("y", 50)
    .append("xhtml:body")
    .style("font", "45px 'Arial'")
    .style("color", "white")
    .html("K-Means algoritması elinizdeki verileri ortak en uygun şekilde kümelemeye çalışan bir algoritmadır" +
        "<br><br>K-Means'de boyut sınırlandırması yoktur ancak basit olsun diye burada size sadece iki boyuttaki" +
        " uygulaması gösterilecektir" +
        "<br><br>K-Means'deki K'nin anlamı oluşturmak istediğiniz küme sayısıdır");

const svgSection2 = d3.select("#section1")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .style("background-color", "orange");
svgSection2
    .append("foreignObject")
    .attr("width", innerWidth / 1.5)
    .attr("height", 500)
    .attr("x", 100)
    .attr("y", 50)
    .append("xhtml:body")
    .style("font", "45px 'Arial'")
    .style("color", "white")
    .html("Birazdan saha içinde dizilmiş ve futbol oynamak isteyen çocukları göreceksiniz" +
        "<br><br>Çocukların maça başlayabilmeleri için onları iki takıma (kümeye) bölmeniz gerekecek" +
        "<br><br>Bunun için önceden seçilmiş iki tane kaptan köşede bekliyorlar" +
        "<br><br>İlk önce onları sahanın içine uygun gördüğünüz yere sürüklemeniz gerekecek");
const svgSection3 = d3.select("#section2")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .style("background-color", "orange");
svgSection3
    .append("foreignObject")
    .attr("width", innerWidth / 1.5)
    .attr("height", 500)
    .attr("x", 100)
    .attr("y", 50)
    .append("xhtml:body")
    .style("font", "44px 'Arial'")
    .style("color", "white")
    .html("Sürükledikten sonra Kaptan Seç butonu her oyuncuyu kendisine en yakın kaptanın takımına dahil edecek" +
        "<br><br>Her oyuncu bir takıma dahil olduktan sonra kaptanın o takımın ortasına geçmesi gerekiyor bunun için Kaptanı Ortala butonuna tıklayacaksınız" +
        "<br><br>Böylece kaptanlar takım arkadaşlarına moral konuşması yapabilecek" +
        "<br><br>Ancak kaptanlar takımın ortasına geçince diğer takımdaki oyunculara yaklaşabilir böylece karşı takımdan oyuncu alabilir");

const svgSection4 = d3.select("#section3")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .style("background-color", "orange");
svgSection4
    .append("foreignObject")
    .attr("width", innerWidth / 1.5)
    .attr("height", 500)
    .attr("x", 100)
    .attr("y", 50)
    .append("xhtml:body")
    .style("font", "44px 'Arial'")
    .style("color", "white")
    .html("Bu işlem artık takımlarda bi değişiklik olmayana kadar butonlar yardımıyla devam ettirebilirsiniz" +
        "<br><br>Aklınızda bulunsun: Kaptanları ilk koyduğunuz yer bir fark oluşturabilir mi acaba?" +
        "<br><br>Takıldığınız yer olursa buraya geri dönebilirsiniz. " +
        "<br><br>Hadi işe koyulun!"
        );

const svgSection5 = d3.select("#section4")
                .attr("width", innerWidth)
                .attr("height", innerHeight);
//captain 0: not a captain; 1: captain of team A; 2: captain of team B

const childPos = [
{x: 308, y: 140, image: "boy.png", captain: 0, team: 0},
{x: 381, y: 70, image: "boy.png", captain: 0, team: 0},
{x: 451, y: 91, image: "boy.png", captain: 0, team: 0},
{x: 464, y: 163, image: "boy.png", captain: 0, team: 0},
{x: 394, y: 248, image: "boy.png", captain: 0, team: 0},
{x: 706, y: 143, image: "boy.png", captain: 0, team: 0},
{x: 795, y: 112, image: "boy.png", captain: 0, team: 0},
{x: 893, y: 90, image: "boy.png", captain: 0, team: 0},
{x: 888, y: 150, image: "boy.png", captain: 0, team: 0},
{x: 872, y: 199, image: "boy.png", captain: 0, team: 0},
{x: 838, y: 567, image: "boy.png", captain: 0, team: 0},
{x: 777, y: 521, image: "boy.png", captain: 0, team: 0},
{x: 724, y: 616, image: "boy.png", captain: 0, team: 0},
{x: 824, y: 657, image: "boy.png", captain: 0, team: 0},
{x: 868, y: 639, image: "boy.png", captain: 0, team: 0},
{x: 400, y: 515, image: "boy.png", captain: 0, team: 0},
{x: 356, y: 565, image: "boy.png", captain: 0, team: 0},
{x: 380, y: 649, image: "boy.png", captain: 0, team: 0},
{x: 300, y: 537, image: "boy.png", captain: 0, team: 0},
{x: 446, y: 503, image: "boy.png", captain: 0, team: 0},
{x: 442, y: 590, image: "boy.png", captain: 0, team: 0},
{x: 612, y: 432, image: "boy.png", captain: 0, team: 0},
{x: 556, y: 381, image: "boy.png", captain: 0, team: 0},
{x: 618, y: 279, image: "boy.png", captain: 0, team: 0},
{x: 654, y: 291, image: "boy.png", captain: 0, team: 0},
{x: 625, y: 371, image: "boy.png", captain: 0, team: 0},
{x: 640, y: 419, image: "boy.png", captain: 0, team: 0},
{x: 706, y: 399, image: "boy.png", captain: 0, team: 0}];

svgSection5.on('click', (event)=>{
    //childPos.push({x: d3.event.x, y: d3.event.y, image: "boy.png", captain: 0, team: 0})
    //console.log(childPos)
});
childPos.push({x: innerWidth * 0.79, y: innerHeight * 0.05, image: "courier_1.png", captain: 1, team: 1});
childPos.push({x: innerWidth * 0.83, y: innerHeight * 0.05, image: "courier_2.png", captain: 1, team: 2});
svgSection5.selectAll("image.children")
    .data(childPos)
    .enter()
    .append("svg:image")
    .attr("x", (d)=>{return d.x;})
    .attr("y", (d)=>{return d.y;})
    .attr("width", 80)
    .attr("height", 80)
    .attr("class", "children")
    .attr("xlink:href", (d)=>{
        return "../static/icons/" + d.image;
    });
const barcaHeight = innerHeight * 1.01;
const barcaWidth = innerWidth * 0.76;
let captainAmount = 2;
svgSection5.selectAll("image.pitch")
    .data([{x: 40, y: 0, image: "barcelona4.png"}])
    .enter()
    .append("svg:image")
    .attr("x", (d)=>{return d.x;})
    .attr("y", (d)=>{return d.y;})
    .attr("width", barcaWidth)
    .attr("height", barcaHeight)
    .attr("class", "pitch")
    .attr("xlink:href", (d)=>{
        return "../static/icons/" + d.image;
    }).lower();
const drag = d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
svgSection5.selectAll("image.children")
    .data(childPos)
    .filter((d, i) => {
        return i > childPos.length - 3 //last two elements are the captains
    })
    .attr("width", 80)
    .attr("height", 80)
    .call(drag);

let isAssignment = true;
const add_courier = () => {
    childPos.push({x: innerWidth * (0.79 + captainAmount * 0.04), y: innerHeight * 0.05, image: "courier_" + (captainAmount + 1) + ".png", captain: 1, team: captainAmount + 1});
    svgSection5.selectAll("image.children")
    .data(childPos)
    .enter()
    .append("svg:image")
    .attr("x", (d)=>{return d.x;})
    .attr("y", (d)=>{return d.y;})
    .attr("width", 80)
    .attr("height", 80)
    .attr("class", "children")
    .attr("xlink:href", (d)=>{
        return "../static/icons/" + d.image;
    });
    svgSection5.selectAll("image.children")
        .filter((d, i) => {
            return i === childPos.length - 1;
        })
        .call(drag);
    captainAmount++;
};
const button_click_listener = () => {
    let newButtonText = "";
    if(isAssignment) {
        assignChildrenToTeam();
        newButtonText = "Kuryeyı Ortala";
    } else {
        calculateNewCenters();
        newButtonText = "Kurye Ata";
    }
    buttonTextPos[0].text = newButtonText;
    isAssignment = !isAssignment;
    d3.selectAll("image.children").on("mousedown.drag", null);
    d3.selectAll("text.assign_button_text")
        .data(buttonTextPos)
        .text((d) => {return d.text;});
};

const buttonTextPos = [{x: innerWidth * 0.8, y: innerHeight * 0.2, text: "Kurye Ata", click: button_click_listener},
    {x: innerWidth * 0.8, y: innerHeight * 0.8, text: "Reset", click: reset},
    {x: innerWidth * 0.8, y: innerHeight * 0.35, text: "Kurye Ekle", click: add_courier}];
const buttonGroup = svgSection5.selectAll("g.button_and_text")
                        .data(buttonTextPos)
                        .enter()
                        .append("g");
const buttonWidth = 200;
const buttonHeight = 80;

buttonGroup
    .append("rect")
    .attr("class", "assign_button")
    .attr("x", (d) => {return d.x})
    .attr("y", (d) => {return d.y})
    .attr("width", buttonWidth)
    .attr("height", buttonHeight)
    .attr("fill", "red")
    .on('click', (d) => {
        d.click();
    });
buttonGroup.append("text")
    .attr("class", "assign_button_text")
    .attr("alignment-baseline", "middle")
    .attr("text-anchor", "middle")
    .attr("x", (d) => {return d.x + buttonWidth / 2})
    .attr("y", (d) => {return d.y + buttonHeight / 2})
    .attr("fill", "white")
    .attr("font-size", 30)
    .text((d) => {return d.text})
    .on('click', (d) => {d.click();});

function calculateNewCenters(){
    for(let captainIndex = childPos.length - captainAmount; captainIndex < childPos.length; captainIndex++){
        const captain = childPos[captainIndex];
        let sum = [0, 0]; //for both x and y axes
        let count = 0;
        for (let i = 0; i < childPos.length - (captainAmount); i++) {
            const child = childPos[i];
            if (child.team === captain.team) {
                sum[0] += child.x;
                sum[1] += child.y;
                count++;
            }
        }
        const teamNewCenter = {x: (count > 0) ? sum[0] / count : captain.x, y: (count > 0) ? sum[1] / count : captain.y};

        captain.x = teamNewCenter.x;
        captain.y = teamNewCenter.y;
    }

    d3.selectAll("image.children")
        .data(childPos)
        .transition()
        .attr("x", (d) => {
            return d.x;
        })
        .attr("y", (d) => {
            return d.y;
        });
}
function assignChildrenToTeam(){
    console.log(childPos);
    //proced with center calculation
    for(let i = 0; i < childPos.length - captainAmount; i++){
        const player = childPos[i];
        //First captain is assigned to be the minimum at first
        const first_captain = childPos[childPos.length - captainAmount];
        let min_dist = euclidianDistance(player.x, player.y, first_captain.x, first_captain.y);
        let min_dist_captain = first_captain;

        for(let captainIndex = (childPos.length - captainAmount) + 1; captainIndex < childPos.length; captainIndex++){
            const captain = childPos[captainIndex];
            const dist = euclidianDistance(player.x, player.y, captain.x, captain.y);
            if(dist < min_dist){
                min_dist = dist;
                min_dist_captain = captain;
            }
        }
        // subtracting (childPos.length - captainAmount) to know the ranking within the captains
        childPos[i].image = "boy_" + min_dist_captain.team + ".png";
        childPos[i].team = min_dist_captain.team;
    }
    d3.selectAll("image.children")
        .data(childPos)
        .attr("x", (d)=>{return d.x;})
        .attr("y", (d)=>{return d.y;})
        .attr("xlink:href", (d) =>{
            return "../static/icons/" + d.image;
    })
}

function reset(){
    if(!isAssignment) {
        buttonTextPos[0].text = "Kurye Ata";
        d3.selectAll("text.assign_button_text")
            .data(buttonTextPos)
            .text((d) => {return d.text;});
        isAssignment = true
    }
    svgSection5.selectAll("image.children").filter((d, i) => {
            return i >= childPos.length - captainAmount //last two elements are the captains
        })
        .call(drag);

    for(let captainIndex = childPos.length - captainAmount; captainIndex < childPos.length; captainIndex++){
        const captain = childPos[captainIndex];
        captain.x = innerWidth * (0.75 + captain.team * 0.04);
        captain.y = innerHeight * 0.05;
    }


    for (let i = 0; i < childPos.length - captainAmount; i++) {
        const child = childPos[i];
        child.image = "boy.png"
    }

    svgSection5.selectAll("image.children")
        .data(childPos)
        .transition()
        .attr("x", (d)=>{return d.x;})
        .attr("y", (d)=>{return d.y;})
        .attr("xlink:href", (d) =>{
            return "../static/icons/" + d.image;
        });
}
function euclidianDistance(x1, y1, x2, y2){
    return Math.sqrt(Math.pow(y2 - y1, 2) + Math.pow(x2 - x1, 2));
}
function dragstarted(d) {
  d3.select(this).raise().classed("active", true);
}

function dragged(d) {
    d3.select(this).attr("x", d.x = d3.event.x).attr("y", d.y = d3.event.y);
}

function dragended(d) {
    d3.select(this).classed("active", false);
}