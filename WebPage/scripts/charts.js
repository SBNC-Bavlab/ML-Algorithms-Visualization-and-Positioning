const descriptions = ["Verimizden Astigmat olan insanların sadece sert lens kullanabildiklerini; olmayanların ise yalnızca yumuşak lens kullanabildiklerini çıkarabilriiz.",
                    "Bu verimizde ise yaş arttıkça lens takmaya müsaade etme oranının azaldığını göürüyoruz",
                    "Bu kısım gösteriyor ki; göz bozukluğu hipermetrop olanlar daha çok yumuşak lens kullanabiliyorken, miyop olanlar sert lense yönlendiriliyor.",
                    "Hadi şimdi de siz grafikleri keşfedip çıkarımlarda bulunun"];
const features = {"Yaş": ["Genç", "Orta", "Yaşlı"], "Göz Bozukluğu" : ["Miyop", "Hipermetrop"], "Astigmat" : ["Yok", "Var"], "Göz yaşı üretimi" : ["Az", "Normal"]};
const labelDict = {1 : "Sert Lens Kullananlar", 2: "Yumuşak Lens Kullananlar", 3: "Lens Kullanamayanlar"};
function readTextFileAndPlot(file)
{
    const rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status === 0)
            {
                const allText = rawFile.responseText;
                const df = [];
                const tokenized = allText.split("\n");
                for(let i = 0; i < tokenized.length; i++){
                    const tokens = tokenized[i].split("  ");
                    df.push(tokens);
                }
                const chartAreaDiv = document.getElementById("chartArea");
                const textDiv = document.createElement("div");
                textDiv.classList.add("col-sm-1");
                textDiv.style.marginTop = "3%";
                chartAreaDiv.appendChild(textDiv);

                for(let i = 0; i < Object.keys(features).length; i++){
                    const canvas = document.createElement('canvas');
                    canvas.id = "myChart" + i;
                    canvas.classList.add("col-sm-2");
                    canvas.style.width = "600px";
                    if(i !== Object.keys(features).length - 1) {
                            canvas.style.borderLeft = "1px solid black"
                    }else{
                        canvas.style.borderLeft = "1px solid black";
                        canvas.style.borderRight = "1px solid black"
                    }
                    canvas.style.height = "175px";
                    chartAreaDiv.appendChild(canvas);
                    const key = Object.keys(features)[i];
                    drawGraph(Object.values(calculateFrequence(df, i)), features[key], key, "myChart" + i)
                }
                const hr = document.createElement("hr");
                hr.style.backgroundColor = "black";
                document.body.appendChild(hr);
                for(let i = 0; i < Object.keys(labelDict).length; i++){
                    const div = document.createElement("div");
                    div.classList.add("row");
                    div.style.marginRight = "0px";
                    div.style.marginLeft = "0px";
                    const tempArray = [];
                    for(let k = 0; k < df.length; k++){
                        if(Number(df[k][4]) === i + 1){
                            tempArray.push(df[k])
                        }
                    }
                    document.body.appendChild(div);

                    const textDiv = document.createElement("div");
                    textDiv.classList.add("col-sm-1");
                    textDiv.id = "label" + i;
                    textDiv.innerHTML = labelDict[i + 1];
                    textDiv.style.marginTop = "3%";
                    div.appendChild(textDiv);
                    for(let j = 0; j < Object.keys(features).length; j++){
                        const canvas = document.createElement('canvas');
                        canvas.id = "myLabelChart" + i + "" + j;
                        canvas.classList.add("col-sm-2");
                        div.appendChild(canvas);
                        canvas.style.width = "600px";
                        canvas.style.height = "175px";
                        if(j !== Object.keys(features).length - 1) {
                            canvas.style.borderLeft = "1px solid black";
                        }else{
                            canvas.style.borderLeft = "1px solid black";
                            canvas.style.borderRight = "1px solid black";
                        }
                        const key = Object.keys(features)[j];
                        drawGraph(Object.values(calculateFrequence(tempArray, j)), features[key], key, "myLabelChart" + i + "" + j)
                    }
                }
            }
        }
        afterGraphCompleted()
    };
    rawFile.send(null);

}
/**
1. age of the patient: (1) young, (2) pre-presbyopic, (3) presbyopic
2. spectacle prescription:  (1) myope, (2) hypermetrope
3. astigmatic:     (1) no, (2) yes
4. tear production rate:  (1) reduced, (2) normal
 */
function calculateFrequence(data, colNumber){
    const freqDict = {};
    const key = Object.keys(features)[colNumber];
    for (let j = 0; j < features[key].length; j++) {
        freqDict[j + 1] = 0
    }
    for(let i = 0; i < data.length; i++){
        if(Number(data[i][colNumber]) in freqDict){
            freqDict[Number(data[i][colNumber])]++;
        } else {
            freqDict[Number(data[i][colNumber])] = 1;
        }
    }
    return freqDict;
}
function drawGraph(data, labels, label, chartID){
    const datalist = {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgb(252, 200, 42)',
                    'rgb(160, 190, 239)',
                    'rgb(77, 193, 73)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgb(252, 200, 42)',
                    'rgb(160, 190, 239)',
                    'rgb(77, 193, 73)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        };
    const ctx = document.getElementById(chartID).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: datalist,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        max: 12,
                        beginAtZero:true
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Kişi Sayısı'
                    }
                }]
            },
            legend: {
                display: false
            },
            title: {
                display: true,
                text: label
            }
        }
    });
}
$( function() {
    readTextFileAndPlot("lens.txt")
});
let descIndex = 0;
function afterGraphCompleted(){
    $("#header0, #myChart0, #myLabelChart00, #myLabelChart10, #myLabelChart20").addClass("blur");
    $("#header1, #myChart1, #myLabelChart01, #myLabelChart11, #myLabelChart21").addClass("blur");
    $("#myLabelChart22").addClass("blur");
    $("#label2").addClass("blur");
    $("#header3, #myChart3, #myLabelChart03, #myLabelChart13, #myLabelChart23").addClass("blur")
                                                                        .css("border-left", "");
    $("#myChart2, #myLabelChart02, #myLabelChart12, #myLabelChart22").css("border-right", "1px solid black");
    $("#infoText").html(descriptions[0]);
    descIndex++;
    //Borders were mainpulated so that when blurring there would not be any collision
    $("#next").click(()=>{
        $("*").removeClass("blur");
        $("#infoText").html(descriptions[descIndex]);
        if(descIndex === 1){
            $("#header1, #myChart1, #myLabelChart01, #myLabelChart11, #myLabelChart21").addClass("blur");
            $("#header2, #myChart2, #myLabelChart02, #myLabelChart12, #myLabelChart22").addClass("blur");
            $("#header3, #myChart3, #myLabelChart03, #myLabelChart13, #myLabelChart23").addClass("blur");
            $("#myChart1, #myLabelChart01, #myLabelChart11, #myLabelChart21").css("border-left", "");
            $("#myChart0, #myLabelChart00, #myLabelChart10, #myLabelChart20").css("border-right", "1px solid black");
            $("#text_overlay").css("left", "35%");
        }else if(descIndex === 2){
            $("#header0, #myChart0, #myLabelChart00, #myLabelChart10, #myLabelChart20").addClass("blur");
            $("#myChart1, #myLabelChart01, #myLabelChart11, #myLabelChart21").css("border-left", "1px solid black")
                                                                            .css("border-right", "1px solid black");
            $("#myLabelChart21").addClass("blur");
            $("#header2, #myChart2, #myLabelChart02, #myLabelChart12, #myLabelChart22").addClass("blur");
            $("#myChart2, #myLabelChart02, #myLabelChart12, #myLabelChart22").css("border-left", "");
            $("#label2").addClass("blur");
            $("#header3, #myChart3, #myLabelChart03, #myLabelChart13, #myLabelChart23").addClass("blur");
            $("#text_overlay").css("left", "45%");
        } else if(descIndex === 3){
            $("#header0, #myChart0, #myLabelChart00, #myLabelChart10, #myLabelChart20").addClass("blur");
            $("#header1, #myChart1, #myLabelChart01, #myLabelChart11, #myLabelChart21").addClass("blur");
            $("#header2, #myChart2, #myLabelChart02, #myLabelChart12, #myLabelChart22").addClass("blur");
            $("#header3, #myChart3, #myLabelChart03, #myLabelChart13, #myLabelChart23").addClass("blur");
            $("#next").html("Olur");
            $("#text_overlay").css("left", "35%");
        } else if(descIndex === 4){
            $("#myChart1, #myLabelChart01, #myLabelChart11, #myLabelChart21").css("border-left", "");
            $("#text_overlay").css("display", "none");
        }
        descIndex++;
    });
}