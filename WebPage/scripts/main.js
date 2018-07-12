const data = [
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

const indexOfNumericValue = 1;
const idToObject = {};
const labelToImage = {"Karpuz" : "watermelon.png", "Kavun" : "melon.png", "Elma" : {"Kırmızı" : "apple.png", "Yeşil": "green_apple.png"}, "Üzüm": "grapes.png", "Limon": "lemon.png"};
const tutorial = ["Elimizde pazar satıcısı Mustafa'nın tezgahındaki karpuz ve kavunlara ait veriler var",
  "Karpuz ve kavunu bir küre varsayarsanız çap değeri onun büyüklüğünü gösterir",
  "Bizim amacımız karpuz ve kavunları birbirinden ayıran bir çap değeri bulmak",
  "Yani öyle bir çap değeri bulmalıyız ki çapı onun üstündeki meyvelere karpuz diğerlerine kavun diyebilelim",
  "Yalnız karpuz boyutunda kavun veya kavun boyutunda karpuz olabileceği için bu göründüğü kadar kolay olmayabilir",
  "Sürükleyici ile bir sayı seçip butona tıklayın.",
  "Eğer kritik noktanızı 1 olarak belirlerseniz modeliniz çapı 1'den büyük herşeyi karpuz kabul etmiş oluyorsunuz.",
  "Hadi şimdi Mustafa'nın tezgahını kullanarak oluşturduğunuz model yardımıyla Ahmet'in tezgahında bulunan ve sadece çapı bilinen meyvelerin ne olduğunu tahmin etmeye çalışalım.",
  "Modeliniz bu şekilde tahmnin etti",
  "Ancak gerçek değerler bu şekildeydi",
  "Yeni Model Kur butonuna tıklayarak yeni bir model kurup, test edip; en yüksek başarı oranını yakalamaya çalışabilirsiniz"];
const guide = [".a0 .a1", ".b0 .slider", ".c0 .c1"];
let criticalValue = 0;
//Data is sorted in advance
data.sort((a, b) => {
    return a[indexOfNumericValue] - b[indexOfNumericValue];
});
test_data.sort((a, b) => {
    return a[indexOfNumericValue] - b[indexOfNumericValue];
});
//Accuracy is calculated from test_list div
function calculateAccuracyOfList(){
    let valid = 0;
    let invalid = 0;
    const testItems = $("#test_list > div");
    for(let i = 0; i < testItems.length; i++){
       const $item = $(testItems[i]);
       const color = $item.css("backgroundColor");
       const label = idToObject[$item.attr("id")]["attributeValues"][2];
       if(color === "rgb(255, 255, 0)" && label === "Karpuz"){
            invalid++;
       }else if (color === "rgb(255, 255, 0)" && label === "Kavun"){
            valid++;
       }else if (color === "rgb(0, 128, 0)" && label === "Karpuz"){
            valid++;
       }else if (color === "rgb(0, 128, 0)" && label === "Kavun"){
            invalid++;
       }
    }
    return [valid, invalid, (100 * valid / (valid + invalid)).toFixed(0)]
}
$( function() {
    const $splitter = $("#splitter");
    const $accuracy = $("#accuracy");

    let tutorialIndex = 0;
    let bringForthIndex = 0;
    let isTutorial = true;

    $("#overlay").css("display", "block");
    $("#overlay_text").html(tutorial[tutorialIndex]);

    tutorialIndex++;
    $splitter.bootstrapSlider();

    //When overlay_button is clicked tutorial proceeds
    $("#overlay_button").click(()=>{
        if(tutorialIndex === 5){
            bringForthIndex++;
            $(guide[bringForthIndex - 1]).css("z-index", "-999");
            $("#overlay_button").css("display", "none");
        }else if (tutorialIndex === 6){
            $("#splitter").bootstrapSlider("disable")
        }
        else if(tutorialIndex === 7){
            $("#main_list").css("display", "none");
            $("#tezgahName").html("Ahmet'in Tezgahı");
            test_data.forEach((entry, i)=>{
                const obje = { attributeValues : entry};
                const table = document.createElement("table");
                const tr = table.insertRow();
                //only diameter
                cell = tr.insertCell();
                cell.innerHTML = entry[indexOfNumericValue];

                const $newNode = $("<div>").attr("id", "test_" + i).addClass("col-sm-1 c1").append($(table));
                idToObject[$newNode.attr("id")] = obje;
                $("#test_list").append($newNode);
            });
            $(guide[2]).css("z-index", "999");
        } else if(tutorialIndex === 8){
            $(guide[2]).css("z-index", "999");
            $(guide[0]).css("z-index", "-999");
            const testItems = $("#test_list > div");
            for(let i = 0; i < testItems.length; i++){
                const $item = $(testItems[i]);
                const conditionAttribute = idToObject[$item.attr("id")]["attributeValues"][indexOfNumericValue];//1 is because question is numeric
                if(Number(conditionAttribute) > Number(criticalValue)){
                    $item.css("background-color", "green");
                }else{
                    $item.css("background-color", "yellow");
                }
            }
        } else if(tutorialIndex === 9){
            const testItems = $("#test_list > div");
            for(let i = 0; i < testItems.length; i++){
                const $item = $(testItems[i]);
                const $tr = $($item).find("table > tbody > tr");
                const label = idToObject[$item.attr("id")]["attributeValues"][2];
                $tr.append("<td> " + "<img src = '../icons/" + labelToImage[label] + "' width = '60'></td>")
            }
            const accuracyEntries = calculateAccuracyOfList();
            tutorial[9] = "Gerçek değerler bu şekildeydi. Modeliniz " + accuracyEntries[0] + " tanesini doğru, " + accuracyEntries[1] + " tanesini yanlış bildi. " +
                "Başarı oranınız %" + accuracyEntries[2]
        } else if (tutorialIndex === 10){
            $("#restart").css("display", "block")
        }

        if( tutorialIndex < tutorial.length) {
            $("#overlay_text").html(tutorial[tutorialIndex]);
            $(guide[bringForthIndex]).css("z-index", "999")
        }else{
            $("#overlay").css("display","none");
            $("#splitter").bootstrapSlider("disable");
            isTutorial = false
        }
        tutorialIndex++;
    });

    const turkishRuleDict = {1: 'de', 2: 'de', 3: 'te', 4:'te', 5: 'te', 6: 'da', 7: 'de', 9: 'da', 10: 'da', 11: 'de', 12: 'de', 13: 'te', 14: 'te', 15: 'te'};
    //When slider is dragged below function is called
    function splitterAction(event) {
        criticalValue = event.value;
        //Special case for being in tutorial
        if (isTutorial) {
            $("#overlay_button").css("display", "block");
            $(guide[0]).css("z-index", 999);
            tutorial[6] = "Eğer kritik noktanızı " + criticalValue + " olarak belirlerseniz artık modeliniz çapı " + criticalValue +
                "'" + turkishRuleDict[criticalValue] + "n büyük herşeyi karpuz kabul edecek";
        } else{
            $("#test_model").css("display", "block")
        }
        $(".tooltip.tooltip-main").css("opacity", "0.7");

        //mainItems are traversed and based on the diamete value of the individual div and criticalValue background is set
        const mainItems = $("#main_list > div");
        for (let i = 0; i < mainItems.length; i++) {
            const $item = $(mainItems[i]);
            const conditionAttribute = idToObject[$item.attr("id")]["attributeValues"][indexOfNumericValue];//1 is because quiestion is numeric
            if (Number(conditionAttribute) > Number(criticalValue)) {
                $item.css("background-color", "green");
            } else {
                $item.css("background-color", "yellow");
            }
        }
    }
    $splitter.on("slide", splitterAction);
    $splitter.on("click", splitterAction);

    //Data is put into main_list and create a idToObject
    data.forEach((entry, i) => {
        const obje = { attributeValues : entry};
        const table = document.createElement("table");
        const tr = table.insertRow();
        tr.style.verticalAlign = "middle";

        cell = tr.insertCell();
        cell.style.fontSize = "25px";
        cell.style.verticalAlign = "middle";
        cell.innerHTML = entry[1];

        const cellImg = tr.insertCell();
        const entryLabel = entry[entry.length - 1];
        if(entryLabel !== "Elma") {
            cellImg.innerHTML = "<img src = '../icons/" + labelToImage[entryLabel] + "' width = '60'>"
        } else {
            cellImg.innerHTML = "<img src = '../icons/" + labelToImage[entryLabel][entry[0]] + "' width = '60'>"
        }
        const $newNode = $("<div>").attr("id", "entry_" + i).addClass("col-sm-1 a1").append($(table));
        idToObject[$newNode.attr("id")] = obje;
        $("#main_list").append($newNode);
    });
    $("#restart").click(()=>{
        $("#restart").css("display","none");
        $("#main_list").css("display", "flex");
        $("#test_list").css("display", "none");
        $("#main_list > div").css("background-color", "rgba(221,221,221,0.54)");
        $("#test_list > div").css("background-color", "rgba(221,221,221,0.54)");
        //$splitter.bootstrapSlider('value', 1);
        $splitter.bootstrapSlider("enable");
        $accuracy.css("display","none");
        $("#tezgahName").html("Mustafa'nın Tezgahı")
    });
    //When test button is clicked testing process starts
    $("#test_model").click(()=>{
        const testItems = $("#test_list > div");
        for(let i = 0; i < testItems.length; i++){
            const $item = $(testItems[i]);
            const conditionAttribute = idToObject[$item.attr("id")]["attributeValues"][indexOfNumericValue];//1 is because quiestion is numeric
            if(Number(conditionAttribute) > Number(criticalValue)){
                $item.css("background-color", "green");
            }else{
                $item.css("background-color", "yellow");
            }
        }

        //Necesaary layout management is done
        const accuracyEntries = calculateAccuracyOfList();
        $accuracy.css("opacity", "1");
        $accuracy.html("Modeliniz " + accuracyEntries[0] + " tanesini doğru, " + accuracyEntries[1] + " tanesini yanlış bildi. " +
            "Başarı oranınız %" + accuracyEntries[2]);
        $("#test_model").css("display", "none");
        $("#restart").css("display", "block");
        $accuracy.css("display","block");
        $("#splitter").bootstrapSlider("disable");
        $("#main_list").css("display", "none");
        $("#test_list").css("display", "flex");
        $("#tezgahName").html("Ahmet'in Tezgahı")
    });
    $(guide[bringForthIndex]).css("z-index", "999")
});
