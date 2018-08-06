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

const childPos = [];
const numberOfCustomer = 45;

let isPlacingCaptains = false;
svgSection5.on('click', (event)=>{
    //childPos.push({x: d3.event.x, y: d3.event.y, image: "boy.png", captain: 0, team: 0})
    //console.log(childPos)
});
const barcaRatio = 1.60714286;
const barcaWidth = innerWidth * 0.7;
const barcaHeight = barcaWidth / barcaRatio;
const pitchX = innerWidth * 0.01;
const pitchY = innerHeight * 0.01;
let captainAmount = 2;
svgSection5.selectAll("image.pitch")
    .data([{x: pitchX, y: pitchY, image: "barcelona4.png"}])
    .enter()
    .append("svg:image")
    .attr("x", (d)=>{return d.x;})
    .attr("y", (d)=>{return d.y;})
    .attr("width", barcaWidth)
    .attr("class", "pitch")
    .attr("xlink:href", (d)=>{
        return "../static/icons/" + d.image;
    }).lower();
const childrenWidthHeight = innerWidth * 0.05;
for(let i = 0; i < numberOfCustomer; i++){
    childPos.push({x: d3.randomUniform(pitchX, pitchX + barcaWidth - childrenWidthHeight)(),
        y: d3.randomUniform(pitchY, pitchY + barcaHeight - childrenWidthHeight)(),
        image: "boy.png", captain: 0, team: 0})
}

childPos.push({x: innerWidth * 0.71, y: innerHeight * 0.08, image: "courier_1.png", captain: 1, team: 1});
childPos.push({x: innerWidth * 0.75, y: innerHeight * 0.08, image: "courier_2.png", captain: 1, team: 2});
svgSection5.selectAll("image.children")
    .data(childPos)
    .enter()
    .append("svg:image")
    .attr("x", (d)=>{return d.x;})
    .attr("y", (d)=>{return d.y;})
    .attr("width", childrenWidthHeight)
    .attr("height", childrenWidthHeight)
    .attr("class", "children")
    .attr("xlink:href", (d)=>{
        return "../static/icons/" + d.image;
    });

const drag = d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
svgSection5.selectAll("image.children")
    .data(childPos)
    .filter((d, i) => {
        return i > childPos.length - 3 //last two elements are the captains
    })
    .attr("width", childrenWidthHeight)
    .attr("height", childrenWidthHeight)
    .call(drag);

let isAssignment = true;
const add_courier = () => {
    if(!isPlacingCaptains) {

        if(captainAmount === 5) {
            return;
        }
        childPos.push({
            x: innerWidth * (0.71 + captainAmount * 0.04),
            y: innerHeight * 0.08,
            image: "courier_" + (captainAmount + 1) + ".png",
            captain: 1,
            team: captainAmount + 1
        });
        svgSection5.selectAll("image.children")
            .data(childPos)
            .enter()
            .append("svg:image")
            .attr("x", (d) => {
                return d.x;
            })
            .attr("y", (d) => {
                return d.y;
            })
            .attr("width", childrenWidthHeight)
            .attr("height", childrenWidthHeight)
            .attr("class", "children")
            .attr("xlink:href", (d) => {
                return "../static/icons/" + d.image;
            });
        svgSection5.selectAll("image.children")
            .filter((d, i) => {
                return i === childPos.length - 1;
            })
            .call(drag);
        captainAmount++;
    } else {
        d3.select(".alert")
            .transition()
                .style("opacity", "1")
            .transition()
                .delay(3000)
                .style("opacity", "0");
        d3.select("#alert_text")
            .transition()
                .text("Bilgilendirme: Kuryeler yerleştirilirken kurye ekleme işlemi yapılamaz")
            .transition()
                .delay(3200)
                .text("Bilgilendirme: ");
    }
};
const remove_courier = () => {
    if(!isPlacingCaptains) {
        if (captainAmount > 1) {
            childPos.pop();
            svgSection5.selectAll("image.children")
                .data(childPos)
                .exit()
                .remove();
            captainAmount--;
        }
    } else {
        d3.select(".alert")
            .transition()
                .style("opacity", "1")
            .transition()
                .delay(3000)
                .style("opacity", "0");
        d3.select("#alert_text")
            .transition()
                .text("Bilgilendirme: Kuryeler yerleştirilirken kurye silme işlemi yapılamaz")
            .transition()
                .delay(3200)
                .text("Bilgilendirme: ");
    }
};
const button_click_listener = () => {
    isPlacingCaptains = true;
    let newButtonText = "";
    if(isAssignment) {
        assignChildrenToTeam();
        newButtonText = "Kuryeyi Ortala";
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

const buttonWidth = innerWidth * 0.1;
const buttonHeight = innerHeight * 0.05;

const buttonTextPos = [{x: innerWidth * 0.72, y: innerHeight * 0.20, text: "Kurye Ata", click: button_click_listener},
    {x: innerWidth * 0.72, y: pitchY + barcaHeight - buttonHeight, text: "Reset", click: reset},
    {x: innerWidth * 0.72, y: innerHeight * 0.35, text: "Kurye Ekle", click: add_courier},
    {x: innerWidth * 0.72, y: innerHeight * 0.46, text: "Kurye Çıkar", click: remove_courier}];
const buttonGroup = svgSection5.selectAll("g.button_and_text")
                        .data(buttonTextPos)
                        .enter()
                        .append("g");
buttonGroup
    .append("rect")
    .attr("class", "assign_button")
    .attr("x", (d) => {return d.x})
    .attr("y", (d) => {return d.y})
    .attr("width", buttonWidth)
    .attr("height", buttonHeight)
    .attr("fill", "red");
buttonGroup.append("text")
    .attr("class", "assign_button_text")
    .attr("alignment-baseline", "middle")
    .attr("text-anchor", "middle")
    .attr("x", (d) => {return d.x + buttonWidth / 2})
    .attr("y", (d) => {return d.y + buttonHeight / 2})
    .attr("fill", "white")
    .attr("font-size", innerWidth * 0.012)
    .text((d) => {return d.text});
buttonGroup
    .attr("cursor", "pointer")
    .on('click', (d) => {
        d.click();
    });
// Add title text 'Kuryeler'
svgSection5.append("text")
    .attr("x", innerWidth * 0.72)
    .attr("y", innerHeight * 0.06)
    .style("fill", "black")
    .attr("font-size", innerWidth * 0.02)
    .text("Kuryeler");
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
    isPlacingCaptains = false;
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
        captain.x = innerWidth * ( 0.67 + captain.team * 0.04);
        captain.y = innerHeight * 0.08;
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
    isPlacingCaptains = true;
    d3.select(this).raise().classed("active", true);
}

function dragged(d) {
    d3.select(this).attr("x", d.x = d3.event.x).attr("y", d.y = d3.event.y);
}

function dragended(d) {
    d3.select(this).classed("active", false);
}